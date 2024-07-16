import anvil.server
from anvil.tables import app_tables
from functools import wraps, partial
import anvil.tables.query as q


def run_callable():
    """
    Make sure a special secret is defined when calling any callable from the Anvil Squared dependency.

    This avoids any unintended server calls of callables in this app
    when using this app as a dependency.
    """
    if anvil.server.context.client.type:
        try:
            _ = anvil.secrets.get_secret('SQUARED')
        except anvil.secrets.SecretError as e:
            print_timestamp(str(e.args[0]))


def print_timestamp(input_str, verbose=True):
    if verbose:
        import datetime as dt
        import pytz
        eastern_tz = pytz.timezone('US/Eastern')
        current_time = dt.datetime.now(eastern_tz)
        formatted_time = current_time.strftime('%H:%M:%S.%f')
        print(f"{input_str} : {formatted_time}")


def proceed_or_abort_scheduled(taskid):
    """Abort any duplicate scheduled tasks."""
    task_name = anvil.server.get_background_task(taskid).get_task_name()

    existing_tasks = app_tables.tasks.get(task_name=task_name)

    if existing_tasks and existing_tasks['task_id']:
        try:
            existing_running_tasks = anvil.server.get_background_task(existing_tasks['task_id'])
            if existing_running_tasks.is_running():
                print("\n This scheduled task is already running. Abort.")
                return False
            else:
                existing_tasks['task_id'] = taskid
        except anvil.server.BackgroundTaskNotFound:
            pass
    elif not existing_tasks:
        existing_tasks = app_tables.tasks.add_row(task_id=taskid, task_name=task_name)
    # print(existing_tasks)
    # print(taskid)
    # print(existing_tasks['task_id'])
    existing_tasks['task_id'] = taskid
    existing_tasks['task_name'] = task_name
    return True


def proceed_or_abort(row, taskid, func_name=None):
    """
    Abort any duplicate background tasks.

    func_name is provided separately as sometimes background tasks
    call other background tasks as functions, which makes func_name
    distinct from the background task.
    """
    print_timestamp(f'proceed_or_abort : {func_name}')

    if not row['bk_tasks']:
        return proceed_or_wait(row, taskid, func_name)
        
    bk_tasks = [i for i in row['bk_tasks'] if i['task_name'] == func_name]
    if len(bk_tasks) > 0:
        bk_task = bk_tasks[0]
    else:
        return proceed_or_wait(row, taskid, func_name)
    
    if bk_task:
        try:
            task = anvil.server.get_background_task(bk_task['task_id'])
        except anvil.server.BackgroundTaskNotFound:
            return proceed_or_wait(row, taskid, func_name)
        if task.is_running():
            print(f'proceed_or_abort: aborting background task {func_name}')
            return False
    # This background task name is not running. So you can run it.
    return proceed_or_wait(row, taskid, func_name)

    

def proceed_or_wait(row, taskid, func_name=None, extra_keys=None):
    """Helper function to queue up duplicate background tasks to run sequentially."""
    import time
    print_timestamp('proceed_or_wait: ' + str(taskid) + ': ' + func_name)
    task_name = anvil.server.get_background_task(taskid).get_task_name()
    task_dict = {'task_id': taskid, 'task_name': task_name}
    
    if extra_keys:
        for key, val in extra_keys.items():
            task_dict[key] = val

    if not row['bk_tasks']:
        # Add this task in the queue and start it.
        row['bk_tasks'] = [task_dict]
        print_timestamp(f"\nA new bk task {taskid} was added: {row['bk_tasks']}")
        return row

    if taskid in [i['task_id'] for i in row['bk_tasks']]:
        print_timestamp(f"\nYou called this bk task {func_name} as a function within another bk task: {taskid}. Proceed.")
        return row

    print_timestamp(f"\n{func_name} ({taskid}) Possibly waiting on some background tasks: {row['bk_tasks']}")

    # Add this task to the queue
    row['bk_tasks'] = row['bk_tasks'] + [task_dict]
    print_timestamp(f"\nA new bk task {taskid} was added: {row['bk_tasks']}")

    # While there is a queue and the current taskid is not at bat yet
    while row['bk_tasks'] and taskid != row['bk_tasks'][0]['task_id']:
        # print(f"\nCurrently running task: {running_task}")
        try:
            task = anvil.server.get_background_task(row['bk_tasks'][0]['task_id'])
            if not task.is_running():
                print_timestamp(f"\nTask {row['bk_tasks'][0]} is no longer running")
                # Remove task and update db.
                row['bk_tasks'] = row['bk_tasks'][1:]  # TODO: might cause an error
                print_timestamp(f"\nRemoval check: {row['bk_tasks']}")
        except anvil.server.BackgroundTaskNotFound:
            row['bk_tasks'] = row['bk_tasks'][1:]
            print_timestamp(f"\nRemoval check: {row['bk_tasks']}")

        time.sleep(1)

    print_timestamp(f"\nNow running {taskid}")
    return row


def user_bk_running(table_name, bk_name):
    """Check if a particular background task is running on this user."""
    user = anvil.users.get_user(allow_remembered=True)
    print_timestamp('user_bk_running: ' + user['email'] + ' bk_name: ' + bk_name)

    row = getattr(app_tables, table_name).get(user=user)
    
    if not row['bk_tasks']:
        return False
    for i in row['bk_tasks']:
        if i['task_name'] == bk_name:
            print_timestamp('Found bk task')
            try:
                task = anvil.server.get_background_task(i['task_id'])
                if task.is_running():  # Ignore errors
                    return True
            except anvil.server.BackgroundTaskNotFound:
                pass
    return False


# ------------------
# Multi tenant stuff
# ------------------
def verify_tenant(tenant_id, user, tenant=None, usertenant=None):
    """Verify a user is in this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    usertenant = usertenant or app_tables.usertenant.get(user=user, tenant=tenant)

    if usertenant['tenant'] == tenant:
        return tenant

    raise Exception('User does not belong to this tenant.')


def get_usertenant(tenant_id, user, tenant=None):
    """Get a usermap. A user with no tenant will be added to this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    
    if not app_tables.usertenant.get(user=user, tenant=tenant):
        new_roles = get_new_user_roles(None, tenant)
        usertenant = app_tables.usertenant.add_row(user=user, tenant=tenant, roles=new_roles)
    else:
        usertenant = app_tables.usertenant.get(user=user, tenant=tenant)
    return usertenant


def get_new_user_roles(tenant_id, tenant=None):
    """Assign a brand new user a role in this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    new_roles = app_tables.roles.search(
        tenant=tenant,
        name=q.any_of(*tenant['new_roles']),
        can_edit=q.not_(True)
    )
    return list(new_roles)


def get_user_roles(tenant_id, user, usertenant=None, tenant=None):
    """Get names of roles for a user in a tenant."""
    tenant = tenant or verify_tenant(tenant_id, user, usertenant=usertenant)
    usertenant = usertenant or app_tables.usertenant.get(user=user, tenant=tenant)

    roles = []
    if usertenant['roles']:
        for role in usertenant['roles']:
            roles.append(role['name'])
    return list(set(roles))


def get_permissions(tenant_id, user, tenant=None, usertenant=None):
    """Get the permissions of a user in a particular tenant."""
    tenant = tenant or verify_tenant(tenant_id, user, usertenant=usertenant)
    usertenant = usertenant or app_tables.usertenant.get(user=user, tenant=tenant)
        
    user_permissions = []
    if usertenant['roles']:
        for role in usertenant['roles']:
            if role['permissions']:
                for permission in role['permissions']:
                    user_permissions.append(permission['name'])

    return list(set(user_permissions))


def validate_user(tenant_id, user, usertenant=None, permissions=None, tenant=None):
    usertenant = usertenant or get_usertenant(tenant_id, user, tenant=tenant)
    tenant = tenant or verify_tenant(tenant_id, user, usertenant=usertenant)
    permissions = permissions or get_permissions(tenant_id, user, usertenant=usertenant, tenant=tenant)
    return tenant, usertenant, permissions


def upsert_role(usertenant, role_name):
    role = app_tables.roles.get(tenant=usertenant['tenant'], name=role_name)
    if not usertenant['roles']:
        usertenant['roles'] = [role]
    elif role not in usertenant['roles']:
        usertenant['roles'] = usertenant['roles'] + [role]
    return usertenant


def populate_permissions(role_dict, perm_list=None):
    """Populate the permissions table."""
    print_timestamp('populate_permissions')

    if not perm_list:
        perm_list = []
        for key, val in role_dict.items():
            perm_list = perm_list + val
        perm_list = list(set(perm_list))
    
    for perm in perm_list:
        if not app_tables.permissions.get(name=perm):
            app_tables.permissions.add_row(name=perm)


def populate_roles(tenant, role_dict):
    """Some basic roles."""
    print_timestamp('populate_roles')
    
    for key, val in role_dict.items():
        perm_rows = app_tables.permissions.search(name=q.any_of(*val))
        if len(perm_rows) == 0:
            populate_permissions(role_dict)
            perm_rows = app_tables.permissions.search(name=q.any_of(*val))
            
        is_it_there = app_tables.roles.get(name=key, tenant=tenant)
        if not is_it_there:
            app_tables.roles.add_row(name=key, tenant=tenant, permissions=list(perm_rows), can_edit=False)
    return app_tables.roles.search(tenant=tenant)


def create_tenant_single_squared(user, admin_role_name, role_dict):
    """Create a tenant."""
    if len(app_tables.tenants.search()) != 0:
        raise anvil.server.InternalError('Only one tenant can exist in this instance.')

    tenant = app_tables.tenants.add_row()
    _ = populate_roles(tenant, role_dict)
    admin_role = app_tables.roles.get(tenant=tenant, name=admin_role_name)
    
    _ = app_tables.usertenant.add_row(tenant=tenant, user=user, roles=[admin_role])
    
    return tenant
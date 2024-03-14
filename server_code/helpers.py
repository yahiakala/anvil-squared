import anvil.server
from anvil.tables import app_tables
from functools import wraps, partial


def run_callable():
    """
    Make sure a special secret is defined when calling any callable from Anvil Squared.

    This avoids any unintended server calls of callables in this app
    when using this app as a dependency.
    """
    if anvil.server.context.client.type:
        try:
            _ = anvil.secrets.get_secret('SQUARED')
        except anvil.secrets.SecretError as e:
            print_timestamp(str(e.args[0]))


@anvil.server.callable
def ping():
    print_timestamp("ping")
    return "pong"


def print_timestamp(input_str, verbose=True):
    if verbose:
        import datetime as dt
        import pytz
        eastern_tz = pytz.timezone('US/Eastern')
        current_time = dt.datetime.now(eastern_tz)
        formatted_time = current_time.strftime('%H:%M:%S.%f')
        print(f"{input_str} : {formatted_time}")


def proceed_or_abort(taskid):
    """Abort any duplicate scheduled tasks."""
    task_name = anvil.server.get_background_task(taskid).get_task_name()

    existing_tasks = app_tables.tasks.get(task_name=task_name)

    if existing_tasks and existing_tasks['task_id']:
        try:
            existing_running_tasks = anvil.server.get_background_task(existing_tasks['task_id'])
            if existing_running_tasks.is_running():
                print(f"\n This scheduled task is already running. Abort.")
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


def proceed_or_wait(row, taskid, func_name=None):
    """Helper function to queue up background tasks to run sequentially."""
    # TODO: abort if the same task on the same row is already running.
    import time
    print_timestamp('proceed_or_wait: ' + str(taskid) + ': ' + func_name)
    task_name = anvil.server.get_background_task(taskid).get_task_name()

    if not row['bk_tasks']:
        # Add this task in the queue and start it.
        row['bk_tasks'] = [{'task_id': taskid, 'task_name': task_name}]
        print_timestamp(f"\nA new bk task {taskid} was added: {row['bk_tasks']}")
        return row

    if taskid in [i['task_id'] for i in row['bk_tasks']]:
        print_timestamp(f"\nYou called this bk task {func_name} as a function within another bk task: {taskid}. Proceed.")
        return row

    print_timestamp(f"\n{func_name} ({taskid}) Possibly waiting on some background tasks: {row['bk_tasks']}")

    # Add this task to the queue
    row['bk_tasks'] = row['bk_tasks'] + [{'task_id': taskid, 'task_name': task_name}]
    print_timestamp(f"\nA new bk task {taskid} was added: {row['bk_tasks']}")

    # While there is a queue and the current taskid is not at bat yet
    while row['bk_tasks'] and taskid != row['bk_tasks'][0]['task_id']:
        # print(f"\nCurrently running task: {running_task}")
        task = anvil.server.get_background_task(row['bk_tasks'][0]['task_id'])
        if not task.is_running():
            print_timestamp(f"\nTask {row['bk_tasks'][0]} is no longer running")
            # Remove task and update db.
            row['bk_tasks'] = row['bk_tasks'][1:]  # TODO: might cause an error
            print_timestamp(f"\nRemoval check: {row['bk_tasks']}")

        time.sleep(1)

    print_timestamp(f"\nNow running {taskid}")
    return row


def permission_required(permissions):
    """
    Creates a decorator for callable functions.

    Not seen by autocomplete.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return anvil.server.callable(require_user=partial(check_user_auth, permissions=permissions))(wrapper)
    return decorator


def check_user_auth(user, permissions):
    """Checks user auth from the auth columns in the user row."""
    # TODO: replace false returns with raising value errors
    print_timestamp('Checking user auth: ', permissions)
    if user is None:
        return False
        
    if isinstance(permissions, str):
        required_permissions = set([permissions])
    else:
        required_permissions = set(permissions)

    try:
        user_permissions = set(
            [
                permission
                for permission in required_permissions
                if user[permission] == True
            ]
        )
    except Exception:
        return False

    # ALL permissions option
    # if not required_permissions.issubset(user_permissions):
    #     return False

    # ANY permissions option
    if not len(user_permissions) > 0:
        return False
        
    return True


def user_table_auth(permissions):
    """
    Decorator that ensures the callable is seen by autocomplete.
    Checks for boolean columns in the Users table with the permission names.
    
    Use this as a decorator below @anvil.server.callable
    """
    def auth_required_decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            user = anvil.users.get_user()
            if not user:
                raise ValueError("No user logged in.")
            
            #  Handle the fact that permissions might be a string or a list
            if isinstance(permissions, str):
                required_permissions = set([permissions])
            else:
                required_permissions = set(permissions)
            
            try:
                user_permissions = set(
                    [
                        permission
                        for permission in required_permissions
                        if user[permission] == True
                    ]
                )
            except Exception:
                raise ValueError("Permission does not exist.")
                
            if len(user_permissions) == 0:
                raise ValueError("Permission required.") 
            else:
                return func(*args, **kwargs)
        return wrapped
    return auth_required_decorator


def sep_table_auth(permissions):
    """
    Checks user auth in separate 'Permissions' table.
    
    Use this as a decorator below @anvil.server.callable
    """
    pass


def user_simple_auth(permissions):
    """
    Checks user auth in a simple object column called 'permissions'
    
    Use this as a decorator below @anvil.server.callable
    """
    def auth_required_decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            user = anvil.users.get_user()
            if not user:
                raise ValueError("No user logged in.")
            
            #  Handle the fact that permissions might be a string or a list
            if isinstance(permissions, str):
                required_permissions = set([permissions])
            else:
                required_permissions = set(permissions)
            
            try:
                user_permissions = set(
                    [
                        permission
                        for permission in required_permissions
                        if permission in user['permissions'].keys()
                    ]
                )
            except Exception:
                raise ValueError("Permission required.")
                
            if len(user_permissions) == 0:
                raise ValueError("Permission required.") 
            else:
                return func(*args, **kwargs)
        return wrapped
    return auth_required_decorator


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
            task = anvil.server.get_background_task(i['task_id'])
            if task.is_completed():
                print_timestamp('Task is complete')
                return False
            else:
                return True
    return False
"""Functions for usertenant app architecture."""
import anvil.users
from anvil.tables import app_tables


from .helpers import populate_roles, validate_user


def create_tenant_single():
    """Create a tenant."""
    user = anvil.users.get_user(allow_remembered=True)
    if len(app_tables.tenants.search()) != 0:
        return None

    tenant = app_tables.tenants.add_row(name="Main", new_roles=["Member"])
    _ = populate_roles(tenant)
    admin_role = app_tables.roles.get(tenant=tenant, name="Admin")
    _ = app_tables.usertenant.add_row(tenant=tenant, user=user, roles=[admin_role])
    return get_tenant_single(user, tenant)


def create_tenant_single_squared(user, admin_role_name, role_dict):
    """Create a tenant."""
    if len(app_tables.tenants.search()) != 0:
        raise anvil.server.InternalError('Only one tenant can exist in this instance.')

    tenant = app_tables.tenants.add_row(name='Default')
    _ = populate_roles(tenant, role_dict)
    admin_role = app_tables.roles.get(tenant=tenant, name=admin_role_name)
    
    _ = app_tables.usertenant.add_row(tenant=tenant, user=user, roles=[admin_role])
    
    return tenant


def verify_tenant(tenant_id, user, tenant=None, usertenant=None):
    """Verify a user is in this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    usertenant = usertenant or app_tables.usertenant.get(user=user, tenant=tenant)

    if usertenant['tenant'] == tenant:
        return tenant

    raise Exception('User does not belong to this tenant.')


def validate_user(tenant_id, user, usertenant=None, permissions=None, tenant=None):
    usertenant = usertenant if usertenant is not None else get_usertenant(tenant_id, user, tenant=tenant)
    tenant = tenant if tenant is not None else verify_tenant(tenant_id, user, usertenant=usertenant)
    permissions = permissions if permissions is not None else get_permissions(tenant_id, user, usertenant=usertenant, tenant=tenant)
    return tenant, usertenant, permissions


def upsert_role(usertenant, role_name):
    role = app_tables.roles.get(tenant=usertenant['tenant'], name=role_name)
    if not usertenant['roles']:
        usertenant['roles'] = [role]
    elif role not in usertenant['roles']:
        usertenant['roles'] = usertenant['roles'] + [role]
    return usertenant


def remove_role(usertenant, role_names):
    usertenant['roles'] = [i for i in usertenant['roles'] if i['name'] not in role_names]
    if len(usertenant['roles']) == 0:
        # Deal with a quirk of empty lists.
        usertenant['roles'] = None
    return usertenant


def populate_permissions(role_dict):
    """Populate the permissions table."""
    print_timestamp('populate_permissions')
    perm_list = []
    for key, val in role_dict.items():
        perm_list = perm_list + val
    
    perm_list = list(set(perm_list))
    if len(app_tables.permissions.search()) == 0:
        for perm in perm_list:
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


def usertenant_row_to_dict(row, extra_cols):
    row_dict = {
        'email': row['user']['email'],
        'last_login': row['user']['last_login'],
        'signed_up': row['user']['signed_up'],
        'permissions': get_permissions(None, row['user'], tenant=row['tenant'], usertenant=row),
        'roles': get_user_roles(None, None, row, row['tenant'])
    }
    for col, val in extra_cols.items():
        row_dict[col] = val
    return row_dict


def role_row_to_dict(role):
    if role['permissions']:
        role_perm = [j['name'] for j in role['permissions']]
    else:
        role_perm = []
    return {
        'name': role['name'],
        'permissions': role_perm,
        'can_edit': role['can_edit']
    }
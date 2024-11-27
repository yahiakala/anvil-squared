from anvil.tables import app_tables
import anvil.tables.query as q
import anvil.secrets

from ..helpers import print_timestamp


def get_usertenant(tenant_id, user, tenant=None):
    """Get a usertenant. A user with no tenant will be added to this tenant."""
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
    tenant = tenant if tenant is not None else verify_tenant(tenant_id, user, usertenant=usertenant)
    usertenant = usertenant if usertenant is not None else app_tables.usertenant.get(user=user, tenant=tenant)

    roles = []
    if usertenant['roles']:
        for role in usertenant['roles']:
            roles.append(role['name'])
    return list(set(roles))


def get_permissions(tenant_id, user, tenant=None, usertenant=None):
    """Get the permissions of a user in a particular tenant."""
    tenant = tenant if tenant is not None else verify_tenant(tenant_id, user, usertenant=usertenant)
    usertenant = usertenant if usertenant is not None else app_tables.usertenant.get(user=user, tenant=tenant)
        
    user_permissions = []
    if usertenant['roles']:
        for role in usertenant['roles']:
            if role['permissions']:
                for permission in role['permissions']:
                    user_permissions.append(permission['name'])

    return list(set(user_permissions))


def get_users_with_permission(tenant_id, permission, tenant=None):
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    perm_row = app_tables.permissions.get(name=permission)
    role_rows = app_tables.roles.search(permissions=[perm_row], tenant=tenant)
    usertenant_list = []
    for role in role_rows:
        usertenants = app_tables.usertenant.search(roles=[role], tenant=tenant)
        for usertenant in usertenants:
            if usertenant not in usertenant_list:
                usertenant_list.append(usertenant)
    for i in usertenant_list:
        print(i['user']['email'])
    return usertenant_list


def get_tenant_single(user=None, tenant=None):
    """Get the tenant in this instance."""
    user = anvil.users.get_user(allow_remembered=True)
    tenant = tenant or app_tables.tenants.get()

    if not tenant:
        return None

    tenant_dict = {"id": tenant.get_id(), "name": tenant["name"]}
    if user:
        tenant, usertenant, permissions = validate_user(
            tenant.get_id(), user, tenant=tenant
        )
        if "delete_members" in permissions:
            # TODO: do not return client writable
            return app_tables.tenants.client_writable().get()

    return tenant_dict
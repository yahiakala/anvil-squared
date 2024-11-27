import anvil.server

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


def get_user_roles(tenant_id, user, usertenant=None, tenant=None):
    """Get names of roles for a user in a tenant."""
    tenant = tenant if tenant is not None else verify_tenant(tenant_id, user, usertenant=usertenant)
    usertenant = usertenant if usertenant is not None else app_tables.usertenant.get(user=user, tenant=tenant)

    roles = []
    if usertenant['roles']:
        for role in usertenant['roles']:
            roles.append(role['name'])
    return list(set(roles))


def get_new_user_roles(tenant_id, tenant=None):
    """Assign a brand new user a role in this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    new_roles = app_tables.roles.search(
        tenant=tenant,
        name=q.any_of(*tenant['new_roles']),
        can_edit=q.not_(True)
    )
    return list(new_roles)
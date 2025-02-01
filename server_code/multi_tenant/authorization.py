import anvil.tables.query as q
import anvil.users
from anvil.tables import app_tables


def verify_tenant(tenant_id, user, tenant=None, usertenant=None):
    """Verify a user is in this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    usertenant = usertenant or app_tables.usertenant.get(user=user, tenant=tenant)

    if usertenant["tenant"] == tenant:
        return tenant

    raise Exception("User does not belong to this tenant.")


def validate_user(tenant_id, user, usertenant=None, permissions=None, tenant=None):
    usertenant = (
        usertenant
        if usertenant is not None
        else get_usertenant(tenant_id, user, tenant=tenant)
    )
    tenant = (
        tenant
        if tenant is not None
        else verify_tenant(tenant_id, user, usertenant=usertenant)
    )
    permissions = (
        permissions
        if permissions is not None
        else get_permissions(tenant_id, user, usertenant=usertenant, tenant=tenant)
    )
    return tenant, usertenant, permissions


def get_plan_permissions(tenant):
    """Get the permissions allowed by a tenant's subscription plan.
    Returns all permissions if no plans table exists or if table exists but has no records.
    """
    try:
        plan_list = [i["name"] for i in tenant["plans"] or []]  # Err col
        plans = app_tables.plans.search()  # Err table

        if len(plan_list) > 0:
            account_permissions = []
            for plan in tenant["plans"]:
                if plan["permissions"]:
                    for permission in plan["permissions"]:
                        account_permissions.append(permission["name"])
            return list(set(account_permissions))
        elif len(plans) > 0:
            return []
        else:
            return get_all_permissions()
    except (anvil.tables.TableError, AttributeError) as e:
        if "No such column" in str(e) or "No such app table" in str(e):
            return get_all_permissions()
        raise


def get_permissions(tenant_id, user, tenant=None, usertenant=None):
    """Get the permissions of a user in a particular tenant."""
    tenant = (
        tenant
        if tenant is not None
        else verify_tenant(tenant_id, user, usertenant=usertenant)
    )
    usertenant = (
        usertenant
        if usertenant is not None
        else app_tables.usertenant.get(user=user, tenant=tenant)
    )

    user_permissions = []
    if usertenant["roles"]:
        for role in usertenant["roles"]:
            if role["permissions"]:
                for permission in role["permissions"]:
                    user_permissions.append(permission["name"])

    user_permissions_list = list(set(user_permissions))
    plan_permissions = get_plan_permissions(tenant)

    return [i for i in user_permissions_list if i in plan_permissions]


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
        print(i["user"]["email"])
    return usertenant_list


def get_user_roles(tenant_id, user, usertenant=None, tenant=None):
    """Get names of roles for a user in a tenant."""
    tenant = (
        tenant
        if tenant is not None
        else verify_tenant(tenant_id, user, usertenant=usertenant)
    )
    usertenant = (
        usertenant
        if usertenant is not None
        else app_tables.usertenant.get(user=user, tenant=tenant)
    )

    roles = []
    if usertenant["roles"]:
        for role in usertenant["roles"]:
            roles.append(role["name"])
    return list(set(roles))


def get_new_user_roles(tenant_id, tenant=None):
    """Assign a brand new user a role in this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    new_roles = app_tables.roles.search(
        tenant=tenant, name=q.any_of(*tenant["new_roles"]), can_edit=q.not_(True)
    )
    return list(new_roles)


def get_usertenant(tenant_id, user, tenant=None):
    """Get a usertenant. A user with no tenant will be added to this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)

    if not app_tables.usertenant.get(user=user, tenant=tenant):
        new_roles = get_new_user_roles(None, tenant)
        usertenant = app_tables.usertenant.add_row(
            user=user, tenant=tenant, roles=new_roles
        )
    else:
        usertenant = app_tables.usertenant.get(user=user, tenant=tenant)
    return usertenant


def get_all_permissions():
    return [i["name"] for i in app_tables.permissions.search()]


def impersonate_user(tenant_id, email):
    user = anvil.users.get_user(allow_remembered=True)
    tenant, usertenant, permissions = validate_user(tenant_id, user)

    member = app_tables.users.get(email=email)
    _, membertenant, _ = validate_user(tenant_id, member)

    if "dev" in permissions:
        anvil.users.force_login(member)
        return member
    else:
        return user


@anvil.server.callable(require_user=True)
def impersonate_user_squared(tenant_id, email):
    from ..helpers import run_callable

    run_callable()
    return impersonate_user(tenant_id, email)

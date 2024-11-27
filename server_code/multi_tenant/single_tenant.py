import anvil.server
from anvil.tables import app-tables

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
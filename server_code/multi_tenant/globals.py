from anvil.tables import app_tables
import anvil.tables.query as q
import anvil.secrets

from .tasks import verify_tenant, validate_user
from .authorization import get_new_user_roles


def get_usertenant(tenant_id, user, tenant=None):
    """Get a usertenant. A user with no tenant will be added to this tenant."""
    tenant = tenant or app_tables.tenants.get_by_id(tenant_id)
    
    if not app_tables.usertenant.get(user=user, tenant=tenant):
        new_roles = get_new_user_roles(None, tenant)
        usertenant = app_tables.usertenant.add_row(user=user, tenant=tenant, roles=new_roles)
    else:
        usertenant = app_tables.usertenant.get(user=user, tenant=tenant)
    return usertenant



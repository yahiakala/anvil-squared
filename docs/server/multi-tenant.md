# Multi-Tenant System

The multi-tenant system provides a robust framework for managing multiple tenants (organizations) within your Anvil application, including user management, role-based access control (RBAC), and permissions.

## Core Concepts

### Tenants
- Represents separate organizations or workspaces
- Each tenant has its own set of users, roles, and permissions
- Can define default roles for new users

### Users
- Can belong to multiple tenants
- Have specific roles within each tenant
- Permissions are derived from their roles

### Roles
- Collections of permissions
- Assigned to users within a tenant context
- Can be configured as editable or non-editable

### Permissions
- Granular access controls
- Assigned to roles
- Used to control feature access and functionality

## Data Tables

The system relies on these Anvil Data Tables:

- `tenants`: Stores tenant information
- `users`: Stores user information
- `usertenant`: Links users to tenants with their roles
- `roles`: Defines available roles
- `permissions`: Stores available permissions

## Core Functions

### Tenant Verification

```python
def verify_tenant(tenant_id, user, tenant=None, usertenant=None)
```
Verifies if a user belongs to a specific tenant.

**Parameters:**

- `tenant_id`: The ID of the tenant to verify
- `user`: The user object to verify
- `tenant`: (Optional) Pre-fetched tenant object
- `usertenant`: (Optional) Pre-fetched usertenant object

**Returns:**

- The tenant object if verification succeeds
- Raises an exception if verification fails

### User Validation

```python
def validate_user(tenant_id, user, usertenant=None, permissions=None, tenant=None)
```
Validates a user's access and retrieves their context within a tenant.

**Parameters:**

- `tenant_id`: The tenant ID
- `user`: The user object
- `usertenant`: (Optional) Pre-fetched usertenant object
- `permissions`: (Optional) Pre-fetched permissions list
- `tenant`: (Optional) Pre-fetched tenant object

**Returns:**

- Tuple of (tenant, usertenant, permissions)

### Permission Management

```python
def get_permissions(tenant_id, user, tenant=None, usertenant=None)
```
Retrieves all permissions for a user within a tenant.

```python
def get_users_with_permission(tenant_id, permission, tenant=None)
```
Finds all users who have a specific permission in a tenant.

### Role Management

```python
def get_user_roles(tenant_id, user, usertenant=None, tenant=None)
```
Gets the names of all roles assigned to a user in a tenant.

```python
def get_new_user_roles(tenant_id, tenant=None)
```
Retrieves the default roles for new users in a tenant.

## Usage Examples

### Basic Tenant Verification
```python
@anvil.server.callable
def secure_function(tenant_id):
    user = anvil.users.get_user()
    try:
        tenant = verify_tenant(tenant_id, user)
        # Proceed with tenant-specific operations
        return True
    except Exception as e:
        return False
```

### Permission-Based Access Control
```python
@anvil.server.callable
def admin_function(tenant_id):
    user = anvil.users.get_user()
    tenant, usertenant, permissions = validate_user(tenant_id, user)

    if 'admin' in permissions:
        # Perform admin operations
        return True
    else:
        raise Exception("Unauthorized access")
```

### Managing New Users
```python
@anvil.server.callable
def setup_new_user(tenant_id, user):
    # Get default roles for new user
    new_roles = get_new_user_roles(tenant_id)

    # Create user-tenant association
    usertenant = get_usertenant(tenant_id, user)

    return usertenant
```

## Advanced Features

### User Impersonation
```python
@anvil.server.callable
def impersonate_user_squared(tenant_id, email)
```
Allows users with 'dev' permission to impersonate other users within the same tenant.

## Best Practices

1. **Always Validate Users**
   ```python
   @anvil.server.callable
   def secure_function(tenant_id):
       user = anvil.users.get_user()
       tenant, usertenant, permissions = validate_user(tenant_id, user)
       # Proceed with validated context
   ```

2. **Cache Validation Results**
   ```python
   # Reuse tenant and usertenant objects
   tenant = verify_tenant(tenant_id, user)
   permissions = get_permissions(tenant_id, user, tenant=tenant)
   roles = get_user_roles(tenant_id, user, tenant=tenant)
   ```

3. **Handle Permissions Gracefully**
   ```python
   def check_permission(required_permission, permissions):
       if required_permission not in permissions:
           raise Exception(f"Missing required permission: {required_permission}")
   ```

## Security Considerations

1. Always use `validate_user()` before performing tenant-specific operations
2. Never trust client-side role or permission checks
3. Implement proper error handling for unauthorized access
4. Use the built-in Anvil user authentication system
5. Regularly audit user permissions and roles

## Error Handling

```python
try:
    tenant, usertenant, permissions = validate_user(tenant_id, user)
except Exception as e:
    # Handle unauthorized access
    anvil.users.logout()
    anvil.users.login_with_form()
```

## Performance Tips

1. Cache validation results when making multiple checks
2. Use optional parameters to avoid redundant database queries
3. Batch permission checks when possible
4. Use server-side caching for frequently accessed data

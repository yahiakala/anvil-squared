# Authentication System

Anvil Squared provides a comprehensive authentication system with support for email-based authentication, Multi-Factor Authentication (MFA), and password security features.

## Core Features

- Email-based signup and signin
- Email confirmation system
- Multi-Factor Authentication (MFA)
- Password security checks using "Have I Been Pwned" API
- Password failure tracking
- Secure password hashing using bcrypt

## Authentication Functions

### Email Authentication

#### Sign In
```python
@anvil.server.callable
def signin_with_email_squared(email, password)
```

Signs in a user with email and password. Handles various authentication scenarios:

- Password validation
- MFA requirement checking
- Email confirmation verification
- Password failure tracking

**Exceptions:**

- `AuthenticationFailed`: Invalid credentials
- `MFARequired`: User has MFA enabled
- `EmailNotConfirmed`: Email needs confirmation
- `TooManyPasswordFailures`: Exceeded password attempt limit

#### Sign Up
```python
@anvil.server.callable
def signup_with_email_squared(email, password, app_name)
```

Creates a new user account with email verification.

**Features:**

- Password strength validation
- Duplicate email checking
- Automatic email confirmation sending
- Password security verification

**Exceptions:**

- `UserExists`: Email already registered
- `PasswordNotAcceptable`: Password too weak or too short

### Multi-Factor Authentication

#### Add MFA Method
```python
@anvil.server.callable(require_user=True)
def add_mfa_method_squared(password, mfa_method)
```

Adds a new MFA method to a user's account.

**Parameters:**

- `password`: Current password for verification
- `mfa_method`: Dictionary containing MFA method details

**Returns:**
- Updated user object

#### Delete MFA Method
```python
@anvil.server.callable(require_user=True)
def delete_mfa_method_squared(password, id)
```

Removes an MFA method from a user's account.

**Parameters:**

- `password`: Current password for verification
- `id`: ID of the MFA method to remove

**Returns:**
- Updated user object

## Helper Functions

### Password Security

```python
def is_password_pwned(password)
```

Checks if a password has been compromised using the "Have I Been Pwned" API.

- Uses k-anonymity to safely check passwords
- Returns True if password is found in breached databases

### Email Confirmation

```python
def send_confirmation_email(email, confirmation_key, from_name="App", from_email=None)
```

Sends email confirmation links to new users.

**Features:**

- Customizable sender name and email
- Secure confirmation key generation
- URL-safe encoding of parameters

### User Creation

```python
def create_new_user(email, password, confirm_email=False, require_mfa=False,
                    mfa_method=None, remember=False)
```

Creates a new user with specified settings.

**Parameters:**

- `email`: User's email address
- `password`: User's password (will be hashed)
- `confirm_email`: Whether to require email confirmation
- `require_mfa`: Whether to enable MFA
- `mfa_method`: Initial MFA method if required
- `remember`: Whether to keep user logged in

## Usage Examples

### Basic Sign Up and Sign In
```python
# Sign up a new user
try:
    user = anvil.server.call('signup_with_email_squared',
                            'user@example.com',
                            'secure_password',
                            'MyApp')
except anvil.users.UserExists:
    print("User already exists")
except anvil.users.PasswordNotAcceptable:
    print("Password too weak")

# Sign in
try:
    user = anvil.server.call('signin_with_email_squared',
                            'user@example.com',
                            'secure_password')
except anvil.users.AuthenticationFailed:
    print("Invalid credentials")
```

### Adding MFA
```python
# Add an authenticator app as MFA method
mfa_method = {
    "id": "authenticator",
    "type": "totp",
    "secret": generate_totp_secret()
}

try:
    user = anvil.server.call('add_mfa_method_squared',
                            'current_password',
                            mfa_method)
except anvil.users.AuthenticationFailed:
    print("Invalid password")
```

## Data Model

The authentication system uses the following table structure:

### Users Table
```python
users:
    email: string
    enabled: boolean
    password_hash: string
    confirmed_email: boolean
    email_confirmation_key: string
    mfa: list[dict]  # List of MFA methods
    n_password_failures: number
```

## Error Handling

The system uses custom exception classes for different scenarios:

```python
anvil.users.AuthenticationFailed
anvil.users.MFARequired
anvil.users.EmailNotConfirmed
anvil.users.TooManyPasswordFailures
anvil.users.UserExists
anvil.users.PasswordNotAcceptable
```

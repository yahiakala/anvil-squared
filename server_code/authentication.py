import anvil.email
import anvil.server
import anvil.users
from anvil.tables import app_tables

from .helpers import run_callable


def check_password(email, password):
    import bcrypt
    user = app_tables.users.get(email=email)

    if bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        ):
        return
    else:
        user["n_password_failures"] += 1
        raise anvil.users.AuthenticationFailed("Email or password is incorrect.")


def signin_with_email(email, password):
    """Try to log user in without MFA. Return exception if user has MFA configured."""
    import bcrypt

    user = app_tables.users.get(email=email)
    if user:
        if not user["password_hash"]:
            raise anvil.users.AuthenticationFailed(
                "No password exists - please login via Google or reset your password."
            )
        elif (
            user["n_password_failures"] is not None
            and user["n_password_failures"] >= 10
        ):
            raise anvil.users.TooManyPasswordFailures(
                "You have reached your limit of password attempts. Please reset your password."
            )
        elif user["mfa"] is not None:
            raise anvil.users.MFARequired("User needs to enter MFA credentials.")
        elif not user["confirmed_email"]:
            raise anvil.users.EmailNotConfirmed(
                "Please confirm your email before logging in."
            )
        elif bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        ):
            anvil.users.force_login(user, remember=True)
            user["n_password_failures"] = 0
            return user
        else:
            user["n_password_failures"] += 1
            raise anvil.users.AuthenticationFailed("Email or password is incorrect.")
    else:
        raise anvil.users.AuthenticationFailed("Email or password is incorrect.")


def signup_with_email(email, password, app_name="App", app_email=None):
    """Signup a new user. Require them to confirm email before logging in."""
    if app_tables.users.get(email=email):
        raise anvil.users.UserExists("User already exists")
    if is_password_pwned(password) or len(password) < 8:
        raise anvil.users.PasswordNotAcceptable(
            "Please use a stronger password of at least 8 characters with a combination of numbers, letters, and symbols."
        )
    user = create_new_user(
        email,
        password,
        confirm_email=True,
        require_mfa=False,
        mfa_method=None,
        remember=False,
    )
    response = send_confirmation_email(
        email, user["email_confirmation_key"], from_name=app_name, from_email=app_email
    )
    print(response)
    return user


def is_password_pwned(password):
    """Check if a password has been leaked using the "Have I Been Pwned" API."""
    import hashlib

    # Compute the SHA-1 hash of the password
    sha1sum = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    first5_chars = sha1sum[:5]
    url = f"https://api.pwnedpasswords.com/range/{first5_chars}"
    response = anvil.http.request(url, method="GET", headers={"User-Agent": "Anvil"})
    response_text = response.get_bytes().decode("utf-8")

    # Parse the API response
    hashes = (line.split(":") for line in response_text.splitlines())

    # Check if the rest of our hash is in the response
    tail = sha1sum[5:]
    for hash_tail, count in hashes:
        if hash_tail == tail:
            return True
    return False


def generate_confirmation_key(length=10):
    """Generate a secure random byte string of adequate length."""
    import base64
    import secrets

    # The length needs to be adjusted because base64 encoding increases the size
    # Here, we aim for approximately the same number of URL-safe characters as the desired length
    random_bytes = secrets.token_bytes(length)
    # Encode the bytes in base64 and ensure URL safety (replace '+' with '-', '/' with '_')
    # Also, strip off the '==' padding for a cleaner URL part
    confirmation_key = (
        base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")
    )
    # Return the confirmation key with the desired length
    return confirmation_key


def create_new_user(
    email,
    password,
    confirm_email=False,
    require_mfa=False,
    mfa_method=None,
    remember=False,
):
    """Create a new user."""
    import bcrypt

    # Hash the password with bcrypt
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    if confirm_email:
        confirmation_key = generate_confirmation_key()
    else:
        confirmation_key = None

    if require_mfa:
        mfa = [mfa_method]
    else:
        mfa = None

    new_user_row = app_tables.users.add_row(
        email=email,
        enabled=True,
        password_hash=password_hash,
        confirmed_email=False,
        email_confirmation_key=confirmation_key,
        mfa=mfa,
        n_password_failures=0,
    )

    if remember and not confirm_email:
        new_user_row = anvil.users.force_login(new_user_row, remember=True)

    return new_user_row


def generate_confirmation_url(email, confirmation_key):
    """Generate confirmation email."""
    import urllib.parse

    # URL-encode the email and confirmation key
    encoded_email = urllib.parse.quote(email)
    encoded_confirmation_key = urllib.parse.quote(confirmation_key)
    # Format the confirmation URL
    confirm_url = f"{anvil.server.get_app_origin()}/_/email-confirm/{encoded_email}/{encoded_confirmation_key}"
    return confirm_url


def send_confirmation_email(email, confirmation_key, from_name="App", from_email=None):
    """Send custom email signup confirmation email to user."""
    # Check if we need to send a confirmation email
    # Generate the confirmation URL
    confirm_url = generate_confirmation_url(email, confirmation_key)

    # Define the email properties
    subject = "Please confirm your email address"
    body = f"""Hello,

Please click on the link below to confirm your email address:

{confirm_url}

Thank you."""

    # Send the email
    anvil.email.send(
        to=email,
        subject=subject,
        text=body,
        from_address=from_email or "accounts",
        from_name=from_name + " Accounts",
    )
    return f"Confirmation email sent to {email} from {from_email}."


def add_mfa_method(password, mfa_method):
    """Add an mfa method."""
    import bcrypt

    user = anvil.users.get_user(allow_remembered=True)
    if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        if user["mfa"]:
            check_mfa = [i for i in user["mfa"] if i["id"] == mfa_method["id"]]
            if len(check_mfa) == 0:
                user["mfa"] = user["mfa"] + [mfa_method]
        else:
            user["mfa"] = [mfa_method]
    else:
        raise anvil.users.AuthenticationFailed("Incorrect password")
    return user


def delete_mfa_method(password, id):
    """Delete mfa method if the password is correct."""
    import bcrypt

    user = anvil.users.get_user(allow_remembered=True)
    if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        user["mfa"] = [i for i in user["mfa"] if i["id"] != id]
        if len(user["mfa"]) == 0:
            user["mfa"] = None
    else:
        raise anvil.users.AuthenticationFailed("Incorrect password.")
    return user


# ---------
# Callables
# ---------

@anvil.server.callable
def check_password_squared(email, password):
    run_callable()
    return check_password(email, password)


@anvil.server.callable
def signin_with_email_squared(email, password):
    run_callable()
    return signin_with_email(email, password)


@anvil.server.callable
def signup_with_email_squared(email, password, app_name):
    run_callable()
    return signup_with_email(email, password, app_name)


@anvil.server.callable(require_user=True)
def add_mfa_method_squared(password, mfa_method):
    run_callable()
    return add_mfa_method(password, mfa_method)


@anvil.server.callable(require_user=True)
def delete_mfa_method_squared(password, id):
    run_callable()
    return delete_mfa_method(password, id)

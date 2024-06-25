import anvil.server
import anvil.users
import datetime as dt
import anvil.js


def print_timestamp(input_str):
    print(input_str, " : ", dt.datetime.now().strftime("%H:%M:%S.%f"))


def signup_with_email(tb_email, tb_password, tb_password_repeat, app_name, callable_name, lbl_error):
    """Signup with email with a custom server function and email confirmation."""
    lbl_error.visible = False
    proceed = signup_with_email_checker(tb_email.text, tb_password.text, tb_password_repeat.text, lbl_error)
    user = None
    if proceed:
        try:
            user = anvil.server.call(callable_name, tb_email.text, tb_password.text, app_name=app_name)
        except anvil.users.MFARequired:
            mfa_method, _ = anvil.users.mfa._configure_mfa(tb_email.text, None, False, [("Cancel", None)], "Sign up")
            user = anvil.server.call("anvil.private.users.signup_with_email", tb_email.text, tb_password.text, mfa_method=mfa_method, remember=True)
        except anvil.users.UserExists as e:
            lbl_error.text = str(e.args[0])
            lbl_error.visible = True
        except anvil.users.PasswordNotAcceptable as e:
            lbl_error.text = str(e.args[0])
            lbl_error.visible = True

    if user:
        lbl_error.text = (
            "We've sent a confirmation email to " + tb_email.text + ". Open your inbox and click the link to complete your signup."
        )
        lbl_error.visible = True
        tb_email.text = ''
        tb_password.text = ''
        tb_password_repeat.text = ''
    return user


def signup_with_email_checker(email, password, password_repeat, lbl_error):
    """Validate the signup form submission."""
    if len(email) < 5 or "@" not in email or "." not in email:
        lbl_error.text = "Enter an email address"
    elif password == '' or password is None:
        lbl_error.text = 'Please enter a password.'
    elif password_repeat != password:
        lbl_error.text = 'Passwords do not match.'
    else:
        lbl_error.visible = False
        return True

    lbl_error.visible = True
    return False


def signin_with_email(tb_email, tb_password, callable_name, lbl_error):
    """Signin with email with a custom server function."""
    lbl_error.visible = False
    user = None
    try:
        user = anvil.server.call(callable_name, tb_email.text, tb_password.text)
    except anvil.users.MFARequired as e:
        r = anvil.users.mfa.mfa_login_with_form(tb_email.text, tb_password.text)
        if r == 'reset_mfa':
            anvil.users.mfa.send_mfa_reset_email(tb_email.text)
            lbl_error.text = "Requested 2-factor authentication reset for " + tb_email.text + ". Check your email."
            lbl_error.visible = True
        elif r is None:
            lbl_error.text = "Cancelled login."
            lbl_error.visible = True
        else:
            user = anvil.users.login_with_email(tb_email.text, tb_password.text, mfa=r, remember=True)
    except anvil.users.AuthenticationFailed as e:
        lbl_error.text = e.args[0]
        lbl_error.visible = True
    except anvil.users.EmailNotConfirmed as e:
        lbl_error.text = "You haven't confirmed your email address. Please check your email and click the confirmation link, or reset your password."
        lbl_error.visible = True
    except anvil.users.TooManyPasswordFailures as e:
        lbl_error.text = e.args[0]
        lbl_error.visible = True

    return user


def reset_password(tb_email, lbl_error):
    """Reset a user's password."""
    if not tb_email.text:
        lbl_error.text = 'Please enter a valid email.'
        lbl_error.visible = True
    else:
        try:
            anvil.users.send_password_reset_email(tb_email.text)
            lbl_error.text = f'Please check your email ({tb_email.text}) for a password reset link.'
            lbl_error.visible = True
        except anvil.users.AuthenticationFailed:
            lbl_error.text = 'No user with this matching email was found.'
            lbl_error.visible = True


class GlobalCache:
    def __init__(self, global_dict):
        self._global_dict = global_dict

    def __getattr__(self, name):
        if name in self._global_dict:
            if name == 'user':
                self._global_dict[name] = self._global_dict[name] or anvil.users.get_user()
                print_timestamp('Global: user')
            elif name == 'is_mobile':
                self._global_dict[name] = self._global_dict[name] or anvil.js.window.navigator.userAgent.lower().find("mobi") > -1
                print_timestamp('Global: is_mobile')
            else:
                print_timestamp(f'Global before: {name}')
                if self._global_dict[name] is None:  # Only check None condition.
                    self._global_dict[name] = anvil.server.call('get_' + name)
                print_timestamp(f'Global after: {name}')
            return self._global_dict[name]
        raise AttributeError(f"Attribute {name} not found")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            # This allows initialization and internal attributes to be set.
            super().__setattr__(name, value)
        else:
            if value is None:
                # If setting an attribute to None, remove it to force repopulation on next access.
                self._global_dict.pop(name, None)
            else:
                # For all other assignments, update the global dictionary normally.
                self._global_dict[name] = value

    def clear_global_attributes(self):
        for name in list(self._global_dict.keys()):
            self._global_dict[name] = None

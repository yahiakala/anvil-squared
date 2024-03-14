import anvil.server
import anvil.users


def print_timestamp(input_str):
    print(input_str, " : ", dt.datetime.now().strftime("%H:%M:%S.%f"))


def signup_with_email(tb_email, tb_password, tb_password_repeat, app_name, callable_name, lbl_error=None):
    """Custom signup flow."""
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


def signup_with_email_checker(email, password, password_repeat, lbl_error=None):
    """This method is called when the TextBox loses focus."""
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

def signup_with_email(email, password, app_name, lbl_error):
    proceed = tb_password_repeat_lost_focus()
    user = None
    if proceed:
        try:
            user = anvil.server.call('signup_with_email_squared', email, password, app_name=app_name)
        except anvil.users.UserExists as e:
            lbl_error.text = str(e.args[0])
            lbl_error.visible = True
        except anvil.users.PasswordNotAcceptable as e:
            lbl_error.text = str(e.args[0])
            lbl_error.visible = True

    if user:
        self.tb_email.text = ''
        self.tb_password.text = ''
        self.tb_password_repeat.text = ''
        self.lbl_error.text = (
            "We've sent a confirmation email to " + email + ". Open your inbox and click the link to complete your signup."
        )
        self.lbl_error.visible = True


def signup_with_email_checker(email, password, password_repeat, lbl_error):
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
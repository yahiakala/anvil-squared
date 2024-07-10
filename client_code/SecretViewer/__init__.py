from ._anvil_designer import SecretViewerTemplate
from anvil import *
from anvil.js.window import navigator
import secrets
import string


class SecretViewer(SecretViewerTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.tb_secret.text = 'wefwef'
        # Any code you write here will run before the form opens.

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, value):
        self._secret = value

    def btn_view_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.disable_buttons()
        if self.tb_secret.hide_text:
            self.tb_secret.hide_text = False
            self.btn_view.icon = 'fa:eye-slash'
        else:
            self.tb_secret.hide_text = True
            self.btn_view.icon = 'fa:eye'
        self.raise_event('view')
        self.enable_buttons()

    def btn_edit_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.disable_buttons()
        self.tb_secret.hide_text = False
        self.btn_view.icon = 'fa:eye-slash'
        self.tb_secret.enabled = True
        self.tb_secret.text = self._secret
        self.raise_event('edit')
        self.enable_buttons()

    def btn_reset_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.disable_buttons()
        self.raise_event('reset')  # This needs to generate a new key.
        self.tb_secret.hide_text = False
        self.btn_view.icon = 'fa:eye-slash'
        self.tb_secret.enabled = True
        self.tb_secret.text = self._secret
        self.enable_buttons()
        

    def btn_copy_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.disable_buttons()
        navigator.clipboard.writeText(self._secret)
        self.raise_event('copy')
        self.enable_buttons()

    def disable_buttons(self):
        self.btn_copy.enabled = False
        self.btn_edit.enabled = False
        self.btn_reset.enabled = False
        self.btn_view.enabled = False

    def enable_buttons(self):
        self.btn_copy.enabled = True
        self.btn_edit.enabled = True
        self.btn_reset.enabled = True
        self.btn_view.enabled = True


def generate_secure_key(length=20):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
from anvil import *

from .. import client_unittest
from ._anvil_designer import DemoTemplate

msg_hist = [
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
]


class Demo(DemoTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.msg_hist = msg_hist
        self.init_components(**properties)
        self.client_tests_1.test_modules = [client_unittest]
        self.client_tests_1.card_roles = [None, None, None]
        self.client_tests_1.icon_size = 30
        self.client_tests_1.btn_role = None

        # Any code you write here will run before the form opens.

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

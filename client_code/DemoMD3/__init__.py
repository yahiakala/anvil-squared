from ._anvil_designer import DemoMD3Template
from anvil import *
from .. import client_unittest

msg_hist = [
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."}
]


class DemoMD3(DemoMD3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.msg_hist = msg_hist
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.client_tests_1.test_modules = [client_unittest]
        self.client_tests_1.card_roles = ['outlined-card', 'tonal-card', 'elevated-card']
        self.client_tests_1.icon_size = 30
        self.client_tests_1.btn_role = 'filled-button'
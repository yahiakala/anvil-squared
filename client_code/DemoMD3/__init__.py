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

features = [
    ['Feature 1', 'Feature 2', 'Feature 3'],
    ['Feature 4', 'Feature 5', 'Feature 6'],
    ['Feature 7', 'Feature 8', 'Feature 9']
]
pricing_tiers = [
    {'title': 'Price 1', 'old_price': '10', 'price': '9', 'url': 'example.com', 'includes': 'This includes:', 'cp_role': 'outlined-card', 'features': features[0]},
    {'title': 'Price 2', 'old_price': '10', 'price': '9', 'url': 'example.com', 'includes': 'This includes:', 'cp_role': 'outlined-card', 'features': features[1]},
    {'title': 'Price 3', 'old_price': '10', 'price': '9', 'url': 'example.com', 'includes': 'This includes:', 'cp_role': 'outlined-card', 'features': features[2]}
]
btn_role = ''
title_role = ''
check_icon = ''

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
        self.pricing_table_1.items = pricing_tiers

    def chat_copy_1_thumbs_up_click(self, **event_args):
        alert('thumbs up! ' + event_args['message'])

    def chat_copy_1_thumbs_down_click(self, **event_args):
        alert('thumbs down! ' + event_args['message'])

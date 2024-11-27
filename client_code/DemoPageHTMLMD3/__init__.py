from anvil import *

from ._anvil_designer import DemoPageHTMLMD3Template

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


class DemoPageHTMLMD3(DemoPageHTMLMD3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.msg_hist = msg_hist
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

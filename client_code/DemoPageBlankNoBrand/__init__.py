from anvil import *

from ._anvil_designer import DemoPageBlankNoBrandTemplate

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


class DemoPageBlankNoBrand(DemoPageBlankNoBrandTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.msg_hist = msg_hist
        self.init_components(**properties)
        # This has some theme color stuff in the background on the scroll bounce.

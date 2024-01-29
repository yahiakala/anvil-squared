from ._anvil_designer import DemoPageBlankTemplate
from anvil import *

msg_hist = [
            {'from': 'bot', 'text': 'Hi, how can I help you?', 'show_thumbs': True},
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


class DemoPageBlank(DemoPageBlankTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.msg_hist = msg_hist
        self.init_components(**properties)
        # self.chatbox_1.scroll_bottom()

        # Any code you write here will run before the form opens.

    def chatbox_1_thumbs_up_click(self, **event_args):
        alert('thumbs up! ' + event_args['message'])

    def chatbox_1_thumbs_down_click(self, **event_args):
        alert('thumbs down! ' + event_args['message'])

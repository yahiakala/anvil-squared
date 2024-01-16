from ._anvil_designer import Chatbox_copyTemplate
from anvil import *
from anvil_extras import routing


@routing.redirect(path="chatbox", priority=0, condition=None)
class Chatbox_copy(Chatbox_copyTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Example data
        self.message_history = [
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."}
        ]
        self.rp_chatbubbles.items = self.message_history

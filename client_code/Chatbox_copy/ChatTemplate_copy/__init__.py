from ._anvil_designer import ChatTemplate_copyTemplate
from anvil import *

class ChatTemplate_copy(ChatTemplate_copyTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.primary = app.theme_colors['Primary']
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

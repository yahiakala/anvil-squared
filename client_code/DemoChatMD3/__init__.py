from ._anvil_designer import DemoChatMD3Template
from anvil import *

class DemoChatMD3(DemoChatMD3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

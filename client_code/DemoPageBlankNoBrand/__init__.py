from ._anvil_designer import DemoPageBlankNoBrandTemplate
from anvil import *

class DemoPageBlankNoBrand(DemoPageBlankNoBrandTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # This has some theme color stuff in the background on the scroll bounce.

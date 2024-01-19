from ._anvil_designer import DemoHTMLMD3Template
from anvil import *

class DemoHTMLMD3(DemoHTMLMD3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

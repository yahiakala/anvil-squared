from ._anvil_designer import DemoMSCTemplate
from anvil import *


class DemoMSC(DemoMSCTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

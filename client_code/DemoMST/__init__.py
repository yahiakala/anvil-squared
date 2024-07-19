from ._anvil_designer import DemoMSTTemplate
from anvil import *


class DemoMST(DemoMSTTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

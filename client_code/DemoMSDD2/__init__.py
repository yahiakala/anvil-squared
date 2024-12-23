from anvil import *

from ._anvil_designer import DemoMSDD2Template


class DemoMSDD2(DemoMSDD2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.msdd2_1.items = ["option 1", "option 2", "option 3"]
        self.msdd2_2.items = ["option 1", "option 2", "option 3"]
        self.msdd2_3.items = ["option 1", "option 2", "option 3"]
        self.msdd2_4.items = ["option 1", "option 2", "option 3"]

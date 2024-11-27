from anvil import *

from ._anvil_designer import DemoChoicesTemplate


class DemoChoices(DemoChoicesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.drop_down_1.items = ["Cheese 1", "Cheese 2"]

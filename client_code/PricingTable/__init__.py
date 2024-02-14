from ._anvil_designer import PricingTableTemplate
from anvil import *

class PricingTable(PricingTableTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

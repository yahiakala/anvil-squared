from ._anvil_designer import PriceCardTemplate
from anvil import *

class PriceCard(PriceCardTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.cp_price.role = self.item['cp_role']

        self.rp_features.items = self.item['features']

    def btn_signup_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.link_hidden.raise_event('click')

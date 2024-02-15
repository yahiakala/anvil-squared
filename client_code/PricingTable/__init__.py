from ._anvil_designer import PricingTableTemplate
from anvil import *
from .PriceCard import PriceCard

class PricingTable(PricingTableTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def form_show(self, **event_args):
        for i in self.items:
            self.fp_pricing.add_component(PriceCard(item=i))

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value
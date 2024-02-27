from ._anvil_designer import PricingTableTemplate
from anvil import *
from .PriceCard import PriceCard

class PricingTable(PricingTableTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def form_show(self, **event_args):
        max_len = 0
        max_len = max([max(max_len, len(i['features'])) for i in self.items])
        for i in self.items:
            # print(i)
            if len(i['features']) < max_len:
                filler_features = ['Blank' for j in range(max_len - len(i['features']))]
                i['features'] += filler_features
        
        for i in self.items:
            self.fp_pricing.add_component(PriceCard(item=i))

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def brand_message(self):
        return self.rt_poweredby.content

    @brand_message.setter
    def brand_message(self, value):
        self.rt_poweredby.content = value

    @property
    def show_branding(self):
        return self.rt_poweredby.visible

    @show_branding.setter
    def show_branding(self, value):
        self.rt_poweredby.visible = value

    @property
    def visible(self):
        return self.fp_pricing.visible

    @visible.setter
    def visible(self, value):
        self.fp_pricing.visible = value
        self.rt_poweredby.visible = value
from ._anvil_designer import FilterRowTemplate
from anvil import *


class FilterRow(FilterRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.lbl_name.text = self.item['name']
        self.msc2.items = self.item['items']
        self.msc2.selected = self.item['selected']

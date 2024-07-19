from ._anvil_designer import FilterRowTemplate
from anvil import *


class FilterRow(FilterRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.lbl_name.text = self.item['name']
        self.msc2.items = self.item['items']
        self.msc2.selected = self.item['selected']
        self.selected = self.item['selected']
        self.add_event_handler('x-clear-filter', self.clear_filter)
    
    def msc2_change(self, **event_args):
        self.selected = self.msc2.selected

    def clear_filter(self, **event_args):
        self.msc2.selected = []
        self.selected = []

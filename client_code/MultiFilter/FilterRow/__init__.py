from ._anvil_designer import FilterRowTemplate
from anvil import *


class FilterRow(FilterRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.lbl_name.text = self.item['name']
        self.msc2.items = self.item['items']
        if 'selected_values' in self.item:
            self.msc2.selected_values = self.item['selected_values']
            self.selected_values = self.item['selected_values']
        else:
            self.selected_values = []
        self.add_event_handler('x-clear-filter', self.clear_filter)
    
    def msc2_change(self, **event_args):
        self.selected_values = self.msc2.selected_values

    def clear_filter(self, **event_args):
        self.msc2.selected_values = []
        self.selected_values = []

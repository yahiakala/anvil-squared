from ._anvil_designer import MultiFilterTemplate
from anvil import *


class MultiFilter(MultiFilterTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
    
    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        self.rp_filters.items = self.item

    def btn_clear_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.rp_filters.raise_event_on_children('x-clear-filter')

    def btn_confirm_click(self, **event_args):
        """This method is called when the button is clicked"""
        filter_rows = self.rp_filters.get_components()
        filter_list = []
        for filter_row in filter_rows:
            if len(filter_row.selected) > 0:
                filter_list.append(
                    {
                        'name': filter_row.name,
                        'selected': filter_row.selected
                    }
                )
        self.raise_event(
            "x-close-alert",
            value=filter_list,
        )

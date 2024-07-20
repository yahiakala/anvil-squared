from ._anvil_designer import RowTemplate1Template
from anvil import *


class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def btn_select_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.item['selected']:
            self.parent.raise_event('x-remove-item', item=self.item)
        else:
            self.parent.raise_event("x-add-item", item=self.item)

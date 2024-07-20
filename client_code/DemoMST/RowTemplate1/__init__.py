from ._anvil_designer import RowTemplate1Template
from anvil import *


class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        self.init_components(**properties)

    def update_button(self, **event_args):
        if self.item['selected']:
            self.btn_select.role = 'secondary-button-selected'
            self.btn_select.text = 'Selected'
        else:
            self.btn_select.role = 'secondary-button'
            self.btn_select.text = 'Select'

    def btn_select_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.item['selected']:
            self.parent.raise_event('x-remove-item', item=self.item)
            self.item['selected'] = False
        else:
            self.parent.raise_event("x-add-item", item=self.item)
            self.item['selected'] = True
        self.update_button()

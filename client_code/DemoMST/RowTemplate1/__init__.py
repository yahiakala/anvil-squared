from ._anvil_designer import RowTemplate1Template
from anvil import *
from .. import DemoMST


class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        self.init_components(**properties)

    def form_show(self, **event_args):
        if self.item:
            self.selected = self.item in self.parent.tag
            self.update_button()
        elif self.item:
            self.selected = False
            self.update_button()

    def update_button(self, **event_args):
        if self.selected:
            self.btn_select.role = 'secondary-button-selected'
            self.btn_select.text = 'Selected'
        else:
            self.btn_select.role = 'secondary-button'
            self.btn_select.text = 'Select'

    def btn_select_click(self, **event_args):
        """This method is called when the button is clicked"""
        try:
            if self.selected:
                self.parent.raise_event('x-remove-item', item=self.item)
                self.selected = False
            else:
                self.parent.raise_event("x-add-item", item=self.item)
                self.selected = True
        except AttributeError:
            pass
        self.update_button()

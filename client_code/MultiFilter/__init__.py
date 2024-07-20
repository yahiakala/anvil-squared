from ._anvil_designer import MultiFilterTemplate
from anvil import *


class MultiFilter(MultiFilterTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters = value
        self.rp_filters.items = value

    @property
    def is_popup(self):
        return self._is_popup

    @is_popup.setter
    def is_popup(self, value):
        self._is_popup = value

    def btn_clear_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.rp_filters.raise_event_on_children('x-clear-filter')

    def btn_confirm_click(self, **event_args):
        """This method is called when the button is clicked"""
        filter_rows = self.rp_filters.get_components()
        filter_list = []
        for filter_row in filter_rows:
            if len(filter_row.selected_values) > 0:
                filter_list.append(
                    {
                        'name': filter_row.item['name'],
                        'selected_values': filter_row.selected_values
                    }
                )
        self._filters = filter_list
        self.raise_event('change')
        if self.is_popup:
            self.raise_event(
                "x-close-alert",
                value=self._filters,
            )
        else:
            self.visible = False

    def btn_cancel_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.raise_event('change')
        if self.is_popup:
            self.raise_event(
                'x-close-alert',
                value=self._filters
            )
        else:
            self.visible = False

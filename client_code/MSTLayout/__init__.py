from ._anvil_designer import MSTLayoutTemplate
from anvil import *
from ..MultiFilter import MultiFilter


class MSTLayout(MSTLayoutTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self._selected = []
        self._filters = []

    @property
    def filters(self):
        return self._filters 

    @filters.setter
    def filters(self, value):
        self._filters = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.raise_event("change_selected")

    def add_item(self, item, **event_args):
        """User clicks to select an item."""
        self._selected = self._selected + [item]

    def remove_item(self, item, **event_args):
        """User clicks to unselect an item."""
        self._selected = [i for i in self._selected if i != item]

    # FILTERS
    # -------
    def btn_filter_click(self, **event_args):
        """This method is called when the button is clicked"""
        filters = alert(
            MultiFilter(filters=self._filters),
            role="view-alert",
            dismissible=False,
            buttons=None,
        )
        if filters:
            self._filters = filters
            self.apply_filters()

    def apply_filters(self):
        if self.tb_search.text is not None and len(self.tb_search.text) > 0:
            filtered_data = [
                i
                for i in self._items
                if self.tb_search.text.lower() in self.get_dict_vals(i)
            ]
        else:
            filtered_data = [i for i in self._items]

        for filter in self._filters:
            filtered_data = [
                i for i in filtered_data
                if i[filter['name']] in filter[filter['selected']]
            ]

        self._repeating_panel.items = filtered_data
        self.pagination_1.refresh_pagination()

    def tb_search_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.apply_filters()

    def get_dict_vals(self, input_dict):
        output_list = []
        for _, val in input_dict.items():
            output_list.append(str(val))
        return ', '.append(output_list)

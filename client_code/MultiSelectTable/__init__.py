from ._anvil_designer import MultiSelectTableTemplate
from anvil import *
from ..MultiFilter import MultiFilter


class MultiSelectTable(MultiSelectTableTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self._selected = []
        self._filters = []

    @property
    def data_grid(self):
        return self._data_grid

    @data_grid.setter
    def data_grid(self, value):
        self.clear()
        self._data_grid = value
        self.pagination_1.data_grid = self._data_grid
        
        self.add_component(self.cp_top)
        self.add_component(self._data_grid)
        self.add_component(self.cp_bottom)

    @property
    def repeating_panel(self):
        return self._repeating_panel

    @repeating_panel.setter
    def repeating_panel(self, value):
        self._repeating_panel = value
        self.pagination_1.repeating_panel = self._repeating_panel
        self._items = value.items
        self._repeating_panel.add_event_handler("x-add-item", self.add_item)
        self._repeating_panel.add_event_handler("x-remove-item", self.remove_item)

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
        self.raise_event("change")

    def add_item(self, item, **event_args):
        """User clicks to select an item."""
        self._selected = self._selected + [item]
        self.raise_event('change')

    def remove_item(self, item, **event_args):
        """User clicks to unselect an item."""
        self._selected = [i for i in self._selected if i != item]
        self.raise_event('change')

    # FILTERS
    # -------
    def btn_filter_click(self, **event_args):
        """This method is called when the button is clicked"""
        popup_filters = [
            {
                'name': i['name'],
                'items': i['items'],
                'selected': i['selected']
            }
            for i in self._filters
        ]
        filters = alert(
            MultiFilter(item=popup_filters),
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

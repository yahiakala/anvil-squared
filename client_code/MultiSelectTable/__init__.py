from anvil import *

from ..MultiFilter import MultiFilter
from ._anvil_designer import MultiSelectTableTemplate


class MultiSelectTable(MultiSelectTableTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self._selected = []
        self._filters = []
        # self.mf.visible = False
        # self.mf.set_event_handler('change', self.apply_filters)

    @property
    def data_grid(self):
        return self._data_grid

    @data_grid.setter
    def data_grid(self, value):
        # print('data_grid')
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
        # self.filters = self.set_filters(value.items)
        # print(self.filters)
        self._repeating_panel.add_event_handler("x-add-item", self.add_item)
        self._repeating_panel.add_event_handler("x-remove-item", self.remove_item)

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        print("setting filters")
        print(value)
        self._filters = value
        self.mf.filters = value

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.raise_event("change")

    def set_filters(self, list_of_dicts):
        unique_values = {}
        for d in list_of_dicts:
            for key, value in d.items():
                if key not in unique_values:
                    unique_values[key] = set()
                unique_values[key].add(value)

        result_list = []
        for key, val in unique_values.items():
            result_list.append({"name": key, "items": list(val)})
        # unique_values = {key: list(values) for key, values in unique_values.items()}
        # result_list = [{"name": key, "items": values} for key, values in unique_values.items()]
        # print(result_list)
        return result_list

    def add_item(self, item, **event_args):
        """User clicks to select an item."""
        self._selected = self._selected + [item]
        self.raise_event("change")

    def remove_item(self, item, **event_args):
        """User clicks to unselect an item."""
        self._selected = [i for i in self._selected if i != item]
        self.raise_event("change")

    # FILTERS
    # -------
    def btn_filter_click(self, **event_args):
        """This method is called when the button is clicked"""
        # print('btn_filter_click')
        # print(self.filters)
        # filters = alert(
        #     MultiFilter(filters=self._filters, is_popup=True),
        #     role="view-alert",
        #     dismissible=False,
        #     buttons=None,
        # )
        # if filters:
        #     self._filters = filters
        #     self.apply_filters()
        self.mf.visible = True

    def apply_filters(self, **event_args):
        # if self.tb_search.text is not None and len(self.tb_search.text) > 0:
        #     filtered_data = [
        #         i
        #         for i in self._items
        #         if self.tb_search.text.lower() in self.get_dict_vals(i)
        #     ]
        # else:
        #     filtered_data = [i for i in self._items]
        filtered_data = [i for i in self._items]
        self._filters = self.mf.filters
        # print(self._filters)

        for filter in self._filters:
            filtered_data = [
                i
                for i in filtered_data
                if i[filter["name"]] in filter["selected_values"]
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
        return ", ".append(output_list)

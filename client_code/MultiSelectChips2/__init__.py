from ._anvil_designer import MultiSelectChips2Template
from anvil import *
from ..Chip import Chip


class MultiSelectChips2(MultiSelectChips2Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.fp_right.add_event_handler("x-remove", self.remove_item)
        self._selected = []

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        if len(value) > 0:
            if isinstance(value[0], str):
                self._items = [
                    {
                        'key': i,
                        'value': i,
                        'description': i
                    }
                    for i in value
                ]
            else:
                self._items = value
            self.selected = []

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        """Should be list of dicts."""
        self._selected = value
        if value:
            self._selectable = [i for i in self._items if i['value'] not in self.selected_values]
        else:
            self._selectable = self._items
        self.update_chips()

    @property
    def selected_values(self):
        return [i['value'] for i in self._selected]

    @selected_values.setter
    def selected_values(self, value):
        self.selected = [i for i in self._items if i['value'] in value]
        

    def update_chips(self, **event_args):
        self.dd_items.items = [(i["key"], i["value"]) for i in self._selectable]
        self.dd_items.selected_value = None

        self.fp_right.clear()
        for item in self._selected:
            self.fp_right.add_component(
                Chip(item={"name": item["key"], 'value': item['value'], "description": item["description"]})
            )

    def remove_item(self, remove, **event_args):
        self.selected = [i for i in self._selected if i['value'] != remove['value']]
        self.raise_event('change')

    def dd_items_change(self, **event_args):
        """This method is called when an item is selected"""
        self.selected = self._selected + [
            i for i in self._items if i["value"] == self.dd_items.selected_value
        ]
        self.raise_event('change')
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
        self._items = value
        self.selected = []

    @property
    def selected(self):
        if len(self._selected) > 0:
            return [i['value'] for i in self._selected]
        else:
            return []

    @selected.setter
    def selected(self, value):
        self._selected = value
        if value:
            self._selectable = [i for i in self._items if i not in self._selected]
        else:
            self._selectable = self._items
        self.update_chips()

    def update_chips(self, **event_args):
        self.dd_items.items = [(i["key"], i["value"]) for i in self._selectable]
        self.dd_items.selected_value = None

        self.fp_right.clear()
        for prompt in self._selected:
            self.fp_right.add_component(
                Chip(item={"name": prompt["key"], "description": prompt["description"]})
            )

    def remove_item(self, remove, **event_args):
        self.selected = [i for i in self._selected if i["key"] != remove['name']]
        self.raise_event('change')

    def dd_items_change(self, **event_args):
        """This method is called when an item is selected"""
        self.selected = self._selected + [
            i for i in self.items if i["value"] == self.dd_items.selected_value
        ]
        self.raise_event('change')
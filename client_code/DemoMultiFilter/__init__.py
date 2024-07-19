from ._anvil_designer import DemoMultiFilterTemplate
from anvil import *
from ..MultiFilter import MultiFilter


class DemoMultiFilter(DemoMultiFilterTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        item = [
            {'name': 'Filter 1', 'items': ['Item 1', 'Item 2', 'Item 3'], 'selected': ['Item 1']},
            {'name': 'Filter 2', 'items': ['Item 1', 'Item 2', 'Item 3'], 'selected': ['Item 2']},
            {'name': 'Filter 3', 'items': ['Item 1', 'Item 2', 'Item 3'], 'selected': ['Item 1']},
            {'name': 'Filter 4', 'items': ['Item 1', 'Item 2', 'Item 3'], 'selected': ['Item 2']}
        ]
        self.mf = MultiFilter(item=item)
        self.add_component(self.mf)

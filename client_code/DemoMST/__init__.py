from ._anvil_designer import DemoMSTTemplate
from anvil import *
from ..MultiSelectTable import MultiSelectTable


class DemoMST(DemoMSTTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        items = [
            {'name': 'Alice', 'address': '1 Road Street', 'selected': True},
            {'name': 'Bob', 'address': '2 City Town', 'selected': False}
        ]
        self.repeating_panel_1.items = items
        self.data_grid_1.remove_from_parent()
        self.mst = MultiSelectTable(data_grid=self.data_grid_1, repeating_panel=self.repeating_panel_1)
        self.add_component(self.mst)
        

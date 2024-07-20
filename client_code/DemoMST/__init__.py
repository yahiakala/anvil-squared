from ._anvil_designer import DemoMSTTemplate
from anvil import *
from ..MultiSelectTable import MultiSelectTable


class DemoMST(DemoMSTTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        items = [
            {'name': 'Alice', 'address': '1 Road Street'},
            {'name': 'Bob', 'address': '2 City Town'},
            {'name': 'Meng', 'address': '2 City Town'},
            {'name': 'Gao', 'address': '2 City Town'},
            {'name': 'Kit', 'address': '2 City Town'},
            {'name': 'Cat', 'address': '2 City Town'},
            {'name': 'Bill', 'address': '2 City Town'},
            {'name': 'Almond', 'address': '2 City Town'},
            {'name': 'Mister', 'address': '2 City Town'},
            {'name': 'Mail', 'address': '2 City Town'},
            {'name': 'Mike', 'address': '2 City Town'},
            {'name': 'Mark', 'address': '2 City Town'},
            {'name': 'Meek', 'address': '2 City Town'},
            {'name': 'Branson', 'address': '2 City Town'}
        ]
        self.repeating_panel_1.items = items
        self.data_grid_1.remove_from_parent()
        self.mst = MultiSelectTable(data_grid=self.data_grid_1, repeating_panel=self.repeating_panel_1)
        self.mst.filters = [
            {
                'name': 'name',
                'items': ['Alice', 'Bob', 'Meng', 'Gao', 'Kit', 'Cat', 'Bill', 'Almond', 'Mister', 'Mail', 'Mike', 'Mark', 'Meek', 'Branson']
            },
            {
                'name': 'address',
                'items': ['1 Road Street', '2 City Town']
            }
        ]
        self.mst.set_event_handler('change', self.update_label)
        self.column_panel_1.add_component(self.mst)

    def update_label(self, **event_args):
        self.lbl_selected.text = self.mst.selected
        # alert(self.mst.selected)

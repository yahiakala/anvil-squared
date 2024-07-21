from ._anvil_designer import DemoMSTTemplate
from anvil import *
import anvil.js


class DemoMST(DemoMSTTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.items = [
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
        self.repeating_panel_1.items = self.items
        self.pagination_1.data_grid = self.data_grid_1
        self.pagination_1.repeating_panel = self.repeating_panel_1
        self.pagination_1.refresh_pagination()

        self.pagination2_1.data_grid = self.data_grid_1
        self.pagination2_1.repeating_panel = self.repeating_panel_1
        self.pagination2_1.refresh_pagination()
        self.msdd_name.items = ['Alice', 'Bob', 'Meng', 'Gao', 'Kit', 'Cat', 'Bill', 'Almond', 'Mister', 'Mail', 'Mike', 'Mark', 'Meek', 'Branson']
        self.msdd_addresses.items = ['1 Road Street', '2 City Town']
        self.filters = {
            'name': [],
            'address': []
        }
        self._selected = []
        self.repeating_panel_1.tag = []
        self.repeating_panel_1.add_event_handler('x-remove-item', self.remove_item)
        self.repeating_panel_1.add_event_handler('x-add-item', self.add_item)

        header_dom = anvil.js.get_dom_node(self.drp_header)
        header_dom.style.borderBottom = '1px solid black'

    def remove_item(self, item, **event_args):
        self._selected = [i for i in self._selected if i != item]
        self.repeating_panel_1.tag = self._selected
        self.lbl_selected.text = self._selected

    def add_item(self, item, **event_args):
        self._selected = self._selected + [item]
        self.repeating_panel_1.tag = self._selected
        self.lbl_selected.text = self._selected

    def msdd_name_closed(self, **event_args):
        self.filters['name'] = self.msdd_name.selected
        update_placeholder(self.msdd_name, 'Name')
        self.apply_filters()

    def msdd_addresses_closed(self, **event_args):
        self.filters['address'] = self.msdd_addresses.selected
        update_placeholder(self.msdd_addresses, 'Address')
        self.apply_filters()

    def apply_filters(self, **event_args):
        if self.tb_search.text is not None and len(self.tb_search.text) > 0:
            filtered_data = [
                i for i in self.items
                if self.tb_search.text.lower() in self.get_dict_vals(i).lower()
            ]
        else:
            filtered_data = [i for i in self.items]
            
        for key, val in self.filters.items():
            if len(val) > 0:
                filtered_data = [
                    i for i in filtered_data
                    if i[key] in val
                ]

        self.repeating_panel_1.items = filtered_data
        self.pagination_1.refresh_pagination()
        self.pagination2_1.refresh_pagination()

    def get_dict_vals(self, input_dict):
        output_list = []
        for _, val in input_dict.items():
            output_list.append(str(val))
        return ', '.join(output_list)

    def tb_search_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.apply_filters()


def update_placeholder(msdd, title):
    if len(msdd.selected) == 0:
        msdd.placeholder = title
        msdd.role = None
    else:
        msdd.placeholder = title + ' (' + str(len(msdd.selected)) + ')'
        msdd.role = 'squared-msdd'

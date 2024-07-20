from ._anvil_designer import DemoMultiFilterTemplate
from anvil import *
from ..MultiFilter import MultiFilter


class DemoMultiFilter(DemoMultiFilterTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        item = [
            {'name': 'Filter 1', 'items': ['Item 1', 'Item 2', 'Item 3'], 'selected_values': ['Item 1']},
            {'name': 'Filter 2', 'items': ['Item 1', 'Item 2', 'Item 3'], 'selected_values': ['Item 2']},
            {'name': 'Filter 3', 'items': ['Item 1', 'Item 2', 'Item 3'], 'selected_values': ['Item 1']},
            {'name': 'Filter 4', 'items': ['Item 1', 'Item 2', 'Item 3'], 'selected_values': ['Item 2']}
        ]
        self.mf = MultiFilter(filters=item)
        self.multi_filter_1.filters = item
        # self.mf.set_event_handler('change', self.show_change)
        # self.add_component(self.mf)

    def btn_filter_popup_click(self, **event_args):
        """This method is called when the button is clicked"""
        return_filters = alert(self.mf, buttons=None, is_popup=True)
        alert(return_filters)

    def multi_filter_1_change(self, **event_args):
        alert(self.multi_filter_1.filters)

    def btn_inline_filter_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.multi_filter_1.visible = True

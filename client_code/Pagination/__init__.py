from ._anvil_designer import PaginationTemplate
from anvil import *
from .. import tablemod
import anvil.server
from ..utils import print_timestamp


class Pagination(PaginationTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    @property
    def data_grid(self):
        return self._data_grid

    @data_grid.setter
    def data_grid(self, value):
        self._data_grid = value

    @property
    def repeating_panel(self):
        return self._repeating_panel

    @repeating_panel.setter
    def repeating_panel(self, value):
        self._repeating_panel = value

    def refresh_pagination(self):
        tablemod.refresh_pagination(self)

    def btn_next_arrow_click(self, **event_args):
        """This method is called when the button is clicked"""
        # items = self._repeating_panel.items
        # self._repeating_panel.items = [None] * self._data_grid.rows_per_page
        # curr_page = self._data_grid.get_page()
        with anvil.server.no_loading_indicator:
            tablemod.btn_next_arrow_click(self)

    def btn_prev_arrow_click(self, **event_args):
        """This method is called when the button is clicked"""
        print_timestamp('home_prev_arrow_click')
        self.dg_1.previous_page()
        self.refresh_pagination()

    def btn_first_click(self, **event_args):
        """This method is called when the button is clicked"""
        print_timestamp('home_first_click')
        self.dg_1.jump_to_first_page()
        self.refresh_pagination()

    def btn_last_click(self, **event_args):
        """This method is called when the button is clicked"""
        print_timestamp('home_last_click')
        self.dg_1.jump_to_last_page()
        self.refresh_pagination()

    def btn_prev_click(self, **event_args):
        """This method is called when the button is clicked"""
        print_timestamp('home_prev_click')
        self.dg_1.previous_page()
        self.refresh_pagination()

    def btn_next_click(self, **event_args):
        """This method is called when the button is clicked"""
        print_timestamp('home_next_click')
        self.dg_1.next_page()
        self.refresh_pagination()
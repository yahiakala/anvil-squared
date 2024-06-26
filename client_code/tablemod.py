import math
from .utils import print_timestamp


def refresh_pagination(self):
    print_timestamp('refresh_pagination')
    num_pages = math.ceil(len(self.repeating_panel.items) / self.data_grid.rows_per_page)
    curr_page = self.data_grid.get_page() + 1
    self.btn_curr_page.text = str(curr_page)
    self.btn_last.text = str(num_pages)

    # Left Half
    self.btn_dots_1.visible = True
    self.btn_dots_1.text = '...'
    if curr_page > 4:
        pass
    elif curr_page == 4:
        self.btn_dots_1.text = '2'
    else:
        self.btn_dots_1.visible = False

    self.btn_prev_arrow.enabled = True
    if curr_page > 2:
        self.btn_prev.text = str(curr_page - 1)
        self.btn_prev.visible = True
        self.btn_first.visible = True
    elif curr_page == 2:
        self.btn_prev.visible = False
        self.btn_first.visible = True
    else:
        self.btn_prev.visible = False
        self.btn_first.visible = False
        self.btn_prev_arrow.enabled = False

    # Right Half
    self.btn_dots_2.visible = True
    self.btn_dots_2.text = '...'
    if curr_page < num_pages - 3:
        pass
    elif curr_page == num_pages - 3:
        self.btn_dots_2.text = str(num_pages - 1)
    else:
        self.btn_dots_2.visible = False

    self.btn_next_arrow.enabled = True
    if curr_page < num_pages - 1:
        self.btn_next.text = str(curr_page + 1)
        self.btn_next.visible = True
        self.btn_last.visible = True
    elif curr_page == num_pages - 1:
        self.btn_next.visible = False
        self.btn_last.visible = True
    else:
        self.btn_next.visible = False
        self.btn_last.visible = False
        self.btn_next.visible = False
        self.btn_next_arrow.enabled = False

def btn_next_arrow_click(self, **event_args):
    """This method is called when the button is clicked"""
    print_timestamp('home_next_arrow_click')
    self.data_grid.next_page()
    self.refresh_pagination()

def btn_prev_arrow_click(self, **event_args):
    """This method is called when the button is clicked"""
    print_timestamp('home_prev_arrow_click')
    self.data_grid.previous_page()
    self.refresh_pagination()

def btn_first_click(self, **event_args):
    """This method is called when the button is clicked"""
    print_timestamp('home_first_click')
    self.data_grid.jump_to_first_page()
    self.refresh_pagination()

def btn_last_click(self, **event_args):
    """This method is called when the button is clicked"""
    print_timestamp('home_last_click')
    self.data_grid.jump_to_last_page()
    self.refresh_pagination()

def btn_prev_click(self, **event_args):
    """This method is called when the button is clicked"""
    print_timestamp('home_prev_click')
    self.data_grid.previous_page()
    self.refresh_pagination()

def btn_next_click(self, **event_args):
    """This method is called when the button is clicked"""
    print_timestamp('home_next_click')
    self.data_grid.next_page()
    self.refresh_pagination()

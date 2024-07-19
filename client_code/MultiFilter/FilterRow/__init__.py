from ._anvil_designer import FilterRowTemplate
from anvil import *


class FilterRow(FilterRowTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

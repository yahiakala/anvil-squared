from ._anvil_designer import RowTemplate2Template
from anvil import *


class RowTemplate2(RowTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

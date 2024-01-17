from ._anvil_designer import Router3Template
from anvil import *
from anvil_extras import routing


@routing.template(path="temp3", priority=1, condition=None)
class Router3(Router3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

from ._anvil_designer import RouteForm2Template
from anvil import *
from anvil_extras import routing


@routing.route('form2', url_keys=['id'])
class RouteForm2(RouteForm2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

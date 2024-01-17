from ._anvil_designer import RouteHomeFormTemplate
from anvil import *
from anvil_extras import routing


@routing.route('')
class RouteHomeForm(RouteHomeFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

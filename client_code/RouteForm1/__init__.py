from ._anvil_designer import RouteForm1Template
from anvil import *
from anvil_extras import routing


@routing.route('form1', url_keys=['id'])
class RouteForm1(RouteForm1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        key1 = self.url_dict['id']
        alert(key1)

        # Any code you write here will run before the form opens.

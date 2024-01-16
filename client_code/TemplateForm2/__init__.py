from ._anvil_designer import TemplateForm2Template
from anvil import *
from anvil_extras import routing


@routing.template(path="temp2", priority=1, condition=None)
class TemplateForm2(TemplateForm2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

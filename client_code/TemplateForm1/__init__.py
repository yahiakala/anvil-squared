from ._anvil_designer import TemplateForm1Template
from anvil import *
from anvil_extras import routing


@routing.template(path="", priority=0, condition=None)
class TemplateForm1(TemplateForm1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

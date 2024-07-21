from ._anvil_designer import ChoicesjstestTemplate
from anvil import *
from anvil.js.window import Choices
# import anvil.js

class Choicesjstest(ChoicesjstestTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # choices = anvil.js.window.Choices
        # dropdown_element = anvil.js.get_dom_node(self.dd)
        dropdown_element = self.dom_nodes['my-dropdown']
        self.choices = Choices(dropdown_element, {
            'choices': [{'value': '1', 'label': 'Choice 1'},
                        {'value': '2', 'label': 'Choice 2'},
                        {'value': '3', 'label': 'Choice 3'}],
            'removeItemButton': True
        })
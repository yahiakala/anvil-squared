from ._anvil_designer import ChoicesjstestTemplate
from anvil import *
from anvil.js.window import Choices
import anvil.js

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
        
    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        self.call_js('setupChangeListener', self.choices, 'handle_change')

    def get_selected_items(self):
        selected_items = self.call_js('getSelectedChoices', self.choices)
        print("Selected items:", selected_items)
        return selected_items

    def btn_choices_click(self, **event_args):
        """This method is called when the button is clicked"""
        alert(self.get_selected_items())
    
    def handle_change(self, selected_items):
        alert("New selection:", selected_items)  # this shows nothing
        alert(self.get_selected_items())  # this works



from ._anvil_designer import ChoicesjstestTemplate
from anvil import *
from anvil.js.window import Choices

class Choicesjstest(ChoicesjstestTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

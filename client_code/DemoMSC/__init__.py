from ._anvil_designer import DemoMSCTemplate
from anvil import *


class DemoMSC(DemoMSCTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        chipitems = [
            {'key': 'something1', 'value': 'something1 value', 'description': 'something1 description'},
            {'key': 'something2', 'value': 'something2 value', 'description': 'something2 description'},
            {'key': 'something3', 'value': 'something3 value', 'description': 'something3 description'},
            {'key': 'something4', 'value': 'something4 value', 'description': 'something4 description'},
        ]
        # chipitems2 = ['something1', 'something2', 'something3']
        self.msc2.items = chipitems

    def msc2_change(self, **event_args):
        alert(self.msc2.selected)
        # alert(self.msc2._selectable)

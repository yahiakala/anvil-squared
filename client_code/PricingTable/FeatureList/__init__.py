from anvil import *

from ._anvil_designer import FeatureListTemplate


class FeatureList(FeatureListTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def form_show(self, **event_args):
        if self.item == "Blank":
            self.lbl_feature.foreground = self.parent.parent.parent.parent.item[
                "background_color"
            ]

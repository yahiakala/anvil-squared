from ._anvil_designer import LoadIconTemplate
import anvil
from anvil import HtmlPanel as _HtmlPanel


class LoadIcon(LoadIconTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.link_1.role = 'bot-message'
        self.link_1.add_component(
                anvil.Image(
                    source='_/theme/loading.gif',
                    role='load-message',
                    width=48,
                    display_mode='fill_width'
                ),
                slot='img'
            )
    visible = _HtmlPanel.visible
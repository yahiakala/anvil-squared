from ._anvil_designer import ChatTemplate
from anvil import HtmlPanel as _HtmlPanel
from anvil.js import get_dom_node as _get_dom_node
from ..utils._component_helpers import _html_injector, _spacing_property


_html_injector.script(
    """
    function setChatHeight(height, component) {
        // Find all elements with the class "anvil-role-fixed-repeating-panel"

        var html_element = component.v._anvil.element // jQuery Object
        html_element.css("height", height + "px");
        html_element.animate({ scrollTop: html_element.prop("scrollHeight") }, 500); // ms
    }
    function scrollBottom(component) {
        var html_element = component.v._anvil.element
        html_element.animate({scrollTop: html_element.prop("scrollHeight")}, 100);
    }
    """
)

_html_injector.cdn('_/theme/chatstyling.css')

msg_hist = [
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'user', 'text': "What button?"},
            {'from': 'bot', 'text': "You know, the button!"},
            {'from': 'user', 'text': "That's not helpful."},
            {'from': 'bot', 'text': "Loading.", 'img': True}
]

_defaults = {
    "message_history": msg_hist,
    "show_branding": True,
    "brand_message": """Powered by <a href="https://Chatbeaver.ca">Placeholder</a>""",
    "height": 300
}


class Chat(ChatTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.

        self.tb_input.set_event_handler(
            "pressed_enter", lambda **e: self.raise_event("send_message")
        )
        self.btn_send.set_event_handler(
            "click", lambda **e: self.raise_event("send_message")
        )
        self.btn_flag.set_event_handler(
            "click", lambda **e: self.raise_event("flag_click")
        )
        properties = _defaults | properties
        self._height = _defaults['height']
        self.init_components(**properties)

    def form_show(self, **event_args):
        """This method is called when the HTML panel is shown on the screen"""
        print('showing form')
        self.call_js('setChatHeight', self._height, self.rp_chatbubbles)


    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
    
    @property
    def message_history(self):
        return self.rp_chatbubbles.items

    @message_history.setter
    def message_history(self, value):
        self.rp_chatbubbles.items = value

    @property
    def brand_message(self):
        return self.rt_poweredby.content

    @brand_message.setter
    def brand_message(self, value):
        self.rt_poweredby.content = value

    @property
    def show_branding(self):
        return self.rt_poweredby.visible

    @show_branding.setter
    def show_branding(self, value):
        if value:
            self.fp_input.role = 'round-flow-panel'
        else:
            self.fp_input.role = 'solo-flow-panel'
        self.rt_poweredby.visible = value

    @property
    def input_text(self):
        return self.tb_input.text

    @input_text.setter
    def input_text(self, value):
        self.tb_input.text = value

    def scroll_bottom(self):
        self.call_js('scrollBottom', self.rp_chatbubbles)
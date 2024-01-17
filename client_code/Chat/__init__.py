from ._anvil_designer import ChatTemplate
from anvil import HtmlPanel as _HtmlPanel
from anvil.js import get_dom_node as _get_dom_node

# from ..utils._component_helpers import _html_injector, _spacing_property

# _html_injector.css(
#     """
#     .footer {
#     position: fixed;
#     left: 0;
#     bottom: 0;
#     width: 100%;
#     /*font-size: 20px;*/
#     /*font-weight: 500;*/
#     /*background-color:  #fafafa;*/
#     /*color: #fafafa;*/
#     /*min-height: 40px; */
#     text-align: center;
#     padding: 0 10px 0 10px;
#     z-index: 1;
# }

# .footer > .footer-slot > .placeholder { outline: 1px dotted; padding-left: 16px; padding-right: 16px; margin-top: 12px; display:none; }
# .anvil-highlight .footer > .footer-slot > .placeholder { display:block; }

# .content{
#     /*  adjusted for the footer  */
#     /*margin-bottom: 70px;*/
# }

# .footer a, .footer a.anvil-component {
#     /*padding: 5px;*/
#     /*   margin: 8px 0 0; */
#     border-radius: 20px;
# }
# footer a, .footer .anvil-component {
#     display: block;
#     /*color: #fafafa;*/
#     line-height: 30px;
#     min-width: 30px;
#     min-height: 30px;
#     margin: 0 0;
# }
# .footer a:hover, .footer a:active {
#     color: #eee; text-decoration: none;
#     background-color: %color:Primary 700%;
# }
# .footer a .link-text {
#     padding: 0 4px;
# }

# /* Chat Bubbles */
# .anvil-role-message, .anvil-role-bot-message {
#     padding: 0px 10px 0px 10px;
#     border-radius: 10px;
# }

# /* New 'naked' role for text areas, text boxes, drop downs and date pickers */
# textarea.anvil-component.anvil-role-naked, input.anvil-component.anvil-role-naked,
# .anvil-component.anvil-role-naked select, .anvil-datepicker.anvil-role-naked input,
# textarea.anvil-component.anvil-role-naked:hover, textarea.anvil-component.anvil-role-naked:focus,
# input.anvil-component.anvil-role-naked:hover, input.anvil-component.anvil-role-naked:focus,
# .anvil-component.anvil-role-naked select:hover, .anvil-component.anvil-role-naked select:focus,
# .anvil-datepicker.anvil-role-naked input:hover, .anvil-datepicker.anvil-role-naked input:focus {
#     background-color: transparent;
#     border: none;
#     border-radius: none;
#     color: %color:On Surface%;
#     box-shadow: none;
#     outline: none;
#     border-bottom: none;
#     padding: 5px 2px 0px 2px;
# }

# /* Custom Flow Panel */
# .anvil-role-round-flow-panel {
#     padding: 0px 0px 0px 15px;
#     border-radius: 5px;
#     border: 1px solid #bcbcc3;
#     margin-bottom: 0 !important;
# }

# .anvil-role-solo-flow-panel {
#     padding: 0px 0px 0px 15px;
#     border-radius: 5px;
#     border: 1px solid #bcbcc3;
#     margin: 1px 1px 10px 1px !important;
# }


# .anvil-role-richtext-powered, input.anvil-component.anvil-role-richtext-powered > * {
#     padding-bottom: 0;
#     padding-top: 0;
# }
#     """
# )

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
        self.init_components(**properties)

    def form_show(self, **event_args):
        """This method is called when the HTML panel is shown on the screen"""
        self.call_js('setChatHeight')
        # pass
        
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
        self.btn_flag.scroll_into_view()

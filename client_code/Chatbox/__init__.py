from ._anvil_designer import ChatboxTemplate

from anvil import HtmlPanel as _HtmlPanel
from anvil.js import get_dom_node as _get_dom_node

from ..utils._component_helpers import _html_injector, _spacing_property

_html_injector.css(
    """
    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    /*font-size: 20px;*/
    /*font-weight: 500;*/
    /*background-color:  #fafafa;*/
    /*color: #fafafa;*/
    /*min-height: 40px; */
    text-align: center;
    padding: 0 10px 0 10px;
    z-index: 1;
}

.footer > .footer-slot > .placeholder { outline: 1px dotted; padding-left: 16px; padding-right: 16px; margin-top: 12px; display:none; }
.anvil-highlight .footer > .footer-slot > .placeholder { display:block; }

.content{
    /*  adjusted for the footer  */
    /*margin-bottom: 70px;*/
}

.footer a, .footer a.anvil-component {
    /*padding: 5px;*/
    /*   margin: 8px 0 0; */
    border-radius: 20px;
}
footer a, .footer .anvil-component {
    display: block;
    /*color: #fafafa;*/
    line-height: 30px;
    min-width: 30px;
    min-height: 30px;
    margin: 0 0;
}
.footer a:hover, .footer a:active {
    color: #eee; text-decoration: none;
    background-color: %color:Primary 700%;
}
.footer a .link-text {
    padding: 0 4px;
}

/* Chat Bubbles */
.anvil-role-message, .anvil-role-bot-message {
    padding: 0px 10px 0px 10px;
    border-radius: 10px;
}

/* New 'naked' role for text areas, text boxes, drop downs and date pickers */
textarea.anvil-component.anvil-role-naked, input.anvil-component.anvil-role-naked, 
.anvil-component.anvil-role-naked select, .anvil-datepicker.anvil-role-naked input,
textarea.anvil-component.anvil-role-naked:hover, textarea.anvil-component.anvil-role-naked:focus, 
input.anvil-component.anvil-role-naked:hover, input.anvil-component.anvil-role-naked:focus,
.anvil-component.anvil-role-naked select:hover, .anvil-component.anvil-role-naked select:focus,
.anvil-datepicker.anvil-role-naked input:hover, .anvil-datepicker.anvil-role-naked input:focus {
    background-color: transparent;
    border: none;
    border-radius: none;
    color: %color:On Surface%;
    box-shadow: none;
    outline: none;
    border-bottom: none;
    padding: 5px 2px 0px 2px;
}

/* Custom Flow Panel */
.anvil-role-round-flow-panel {
    padding: 0px 0px 0px 15px; 
    border-radius: 5px; 
    border: 1px solid #bcbcc3;
    margin-bottom: 0 !important;
}

.anvil-role-richtext-powered, input.anvil-component.anvil-role-richtext-powered > * {
    padding-bottom: 0;
    padding-top: 0;
}
    """
)

class Chatbox(ChatboxTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Example data
        self.message_history = [
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."}
        ]
        self.rp_chatbubbles.items = self.message_history

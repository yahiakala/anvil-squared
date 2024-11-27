from ._anvil_designer import ChatPageTemplate

msg_hist = [
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
    {"from": "bot", "text": "Hi, how can I help you?"},
    {"from": "user", "text": "How do I do this thing?"},
    {"from": "bot", "text": "Well that's easy. Just push the button."},
]

_defaults = {
    # "message_history": msg_hist,
    "show_branding": True,
    "brand_message": """Powered by <a href="https://Chatbeaver.ca">Placeholder</a>""",
}


class ChatPage(ChatPageTemplate):
    def __init__(self, **properties):
        self.tb_input.set_event_handler(
            "pressed_enter", lambda **e: self.raise_event("send_message")
        )
        self.btn_send.set_event_handler(
            "click", lambda **e: self.raise_event("send_message")
        )
        self.btn_flag.set_event_handler(
            "click", lambda **e: self.raise_event("flag_click")
        )
        self.rp_chatbubbles.add_event_handler(
            "x-thumbs-up", lambda **e: self.raise_event("thumbs_up_click", **e)
        )
        self.rp_chatbubbles.add_event_handler(
            "x-thumbs-down", lambda **e: self.raise_event("thumbs_down_click", **e)
        )
        properties = _defaults | properties
        self.init_components(**properties)

    def form_show(self, **event_args):
        """This method is called when the HTML panel is shown on the screen"""
        self.scroll_bottom()

    def scroll_bottom(self):
        if self.btn_flag.visible:
            # print('button is visible')
            self.btn_flag.scroll_into_view()
        else:
            # print(self.rp_chatbubbles.get_components()[-1])
            self.rp_chatbubbles.get_components()[-1].scroll_into_view()

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
            self.fp_input.role = "round-flow-panel"
        else:
            self.fp_input.role = "solo-flow-panel"
        self.rt_poweredby.visible = value

    @property
    def input_text(self):
        return self.tb_input.text

    @input_text.setter
    def input_text(self, value):
        self.tb_input.text = value

    @property
    def show_flag(self):
        return self.btn_flag.visible

    @show_flag.setter
    def show_flag(self, value):
        self.btn_flag.visible = value

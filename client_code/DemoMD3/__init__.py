from ._anvil_designer import DemoMD3Template
from anvil import *
from .. import client_unittest

msg_hist = [
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."},
            {'from': 'bot', 'text': 'Hi, how can I help you?'},
            {'from': 'user', 'text': 'How do I do this thing?'},
            {'from': 'bot', 'text': "Well that's easy. Just push the button."}
]

features = [
    ['Feature 1', 'Feature 2', 'Feature 3'],
    ['Feature 4', 'Feature 5', 'Feature 6'],
    ['Feature 7', 'Feature 8', 'Feature 9', 'Feature 10']
]

cardconfig1 = {
    'background_color': 'white',
    'border_radius': '10px',
    'border_color': 'black',
    'enlarge': False,
    'billed_annually': True,
    'text_color': 'black',
    'text_font': 'arial',
    'text_size': 14,
    'title_text': 'Price 1',
    'title_text_size': 30,
    'old_price': 'CA$10',
    'price': 'CA$9',
    'price_text_size': 36,
    'includes': 'This includes:',
    'features': features[0],
    'feature_icon': 'fa:check-circle',
    'btn_text': 'Subscribe',
    'btn_text_size': 14,
    'btn_border_radius': '10px',
    'btn_text_color': 'white',
    'btn_background_color': 'var(--primary)',
    'btn_border_color': 'var(--primary)',
    'btn_position': 'middle',
    'btn_url': 'https://example.com',
    'suptitle_text': None,
    'suptitle_text_size': 30,
    'suptitle_color': 'white',
    'suptitle_background_color': 'var(--onsurfacevariant)',
    'suptitle_border_radius': '10px',
    'suptitle_border_color': 'black'
}

cardconfig2 = cardconfig1.copy()
cardconfig2['suptitle_text'] = 'Most Popular'
cardconfig2['features'] = features[1]
cardconfig2['background_color'] = 'var(--surfacevariant)'
cardconfig3 = cardconfig1.copy()
cardconfig3['features'] = features[2]

cardconfig4 = cardconfig1.copy()
cardconfig4['billed_annually'] = False
cardconfig4['old_price'] = None
cardconfig5 = cardconfig4.copy()
cardconfig5['suptitle_text'] = 'Best Value'
cardconfig5['features'] = features[1]
cardconfig5['background_color'] = 'var(--surfacevariant)'
cardconfig6 = cardconfig4.copy()
cardconfig6['features'] = features[2]

pricing_tiers = [cardconfig1, cardconfig2, cardconfig3]
pricing_tier2 = [cardconfig4, cardconfig5, cardconfig6]
pricing_branding = """Powered by <a href="https://dreamprice.ca">DreamPrice</a>"""


class DemoMD3(DemoMD3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.msg_hist = msg_hist
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.client_tests_1.test_modules = [client_unittest]
        self.client_tests_1.card_roles = ['outlined-card', 'tonal-card', 'elevated-card']
        self.client_tests_1.icon_size = 30
        self.client_tests_1.btn_role = 'filled-button'
        self.pricing_table_1.items = pricing_tiers
        self.pricing_table_1.brand_message = pricing_branding

        self.pricing_table_2.items = pricing_tier2
        self.pricing_table_2.brand_message = pricing_branding

    def chat_copy_1_thumbs_up_click(self, **event_args):
        alert('thumbs up! ' + event_args['message'])

    def chat_copy_1_thumbs_down_click(self, **event_args):
        alert('thumbs down! ' + event_args['message'])

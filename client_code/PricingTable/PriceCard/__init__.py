from ._anvil_designer import PriceCardTemplate
from anvil import *
import anvil.js

class PriceCard(PriceCardTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        self.optional_attr(self.cp_price, 'role', 'cp_role')
        self.cp_price.background = self.item['background']
        # self.optional_attr(self.cp_price, 'background', 'background')
        self.optional_attr(self.cp_price, 'border', 'border')

    def form_show(self, **event_args):
        cp_dom = anvil.js.get_dom_node(self.cp_price)
        cp_dom.style.width = '300px'
        # cp_dom.style.height = '600px'

        self.lbl_suptitle.role = 'squared-highlighted-text'
        self.optional_attr(self.lbl_suptitle, 'text', 'sup_text')
        # self.optional_attr(self.lbl_suptitle, 'role', 'sup_role')
        self.optional_attr(self.lbl_suptitle, 'background', 'sup_background')
        self.optional_attr(self.lbl_suptitle, 'foreground', 'sup_foreground')
        self.optional_attr(self.lbl_suptitle, 'border', 'sup_border')
        # self.lbl_suptitle.border = '1px solid black'
        # self.lbl_suptitle.foreground = 'red'

        if self.lbl_suptitle.text:
            self.sp_1.visible = True
            self.sp_2.visible = True
        else:
            self.lbl_suptitle.text = 'Back'
            self.lbl_suptitle.background = self.item['background']
            self.lbl_suptitle.foreground = self.item['background']

        self.lbl_suptitle_copy.text = 'Back'
        self.lbl_suptitle_copy.background = self.item['background']
        self.lbl_suptitle_copy.foreground = self.item['background']

        self.optional_attr(self.btn_signup, 'role', 'btn_role')
        self.optional_attr(self.btn_signup, 'background', 'btn_background')
        self.optional_attr(self.btn_signup, 'border', 'btn_border')
        self.optional_attr(self.btn_signup, 'text', 'btn_text')

        self.lbl_oldprice.role = 'anvil-squared-strikethrough'
        self.rp_features.items = self.item['features']

    def btn_signup_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.link_hidden.raise_event('click')

    def optional_attr(self, target_obj, attr_name, item_key):
        if item_key in self.item:
            setattr(target_obj, 'visible', True)
            setattr(target_obj, attr_name, self.item[item_key])
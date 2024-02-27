from ._anvil_designer import PriceCardTemplate
from anvil import *
import anvil.js


class PriceCard(PriceCardTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.optional_attr(self.cp_price, 'background', 'background_color')
        if self.item['border_color']:
            self.item['border'] = '1px solid ' + self.item['border_color']
        self.optional_attr(self.cp_price, 'border', 'border')

        self.optional_attr(self.lbl_title, 'foreground', 'text_color')
        # TODO: do for rest of text fields
        self.optional_attr(self.lbl_title, 'font', 'text_font')
        # TODO: do for rest of text fields
        self.optional_attr(self.lbl_mo, 'font_size', 'text_size')
        # TODO: do for rest of text fields

        if 'billed_annually' in self.item and self.item['billed_annually']:
            self.lbl_billedannually.visible = True

        self.optional_attr(self.lbl_title, 'font_size', 'title_text_size')
        self.optional_attr(self.lbl_price, 'font_size', 'price_text_size')


        
        self.btn_signup.role = 'filled-button'  # Just to get the hover behavior
        self.optional_attr(self.btn_signup, 'text', 'btn_text')
        self.optional_attr(self.btn_signup, 'foreground', 'btn_text_color')
        self.optional_attr(self.btn_signup, 'font_size', 'btn_text_size')
        self.optional_attr(self.btn_signup, 'background', 'btn_background_color')

        self.btn_signup_bottom.role = 'filled-button'  # Just to get the hover behavior
        self.optional_attr(self.btn_signup_bottom, 'text', 'btn_text')
        self.optional_attr(self.btn_signup_bottom, 'foreground', 'btn_text_color')
        self.optional_attr(self.btn_signup_bottom, 'font_size', 'btn_text_size')
        self.optional_attr(self.btn_signup_bottom, 'background', 'btn_background_color')
        
        if 'btn_position' in self.item and self.item['btn_position'] == 'bottom':
            self.btn_signup_bottom.visible = True
            self.btn_signup.visible = False
        else:
            self.btn_signup_bottom.visible = False

        if self.item['enlarge']:
            self.sp_1.visible = True
            self.sp_2.visible = True

        if self.item['shrink']:
            self.lbl_suptitle.visible = False
            self.lbl_suptitle_copy.visible = False

        if 'align' in self.item and self.item['align'] == False:
            if 'suptitle_text' in self.item and self.item['suptitle_text']:
                self.lbl_suptitle.visible = True
            else:
                self.lbl_suptitle.visible = False
            self.lbl_suptitle_copy.visible = False
            # self.item['features'] = [i for i in self.item['features'] if i != 'Blank']

            
        # Supertitle
        if self.item['suptitle_text']:
            self.lbl_suptitle.text = self.item['suptitle_text']
            self.optional_attr(self.lbl_suptitle, 'background', 'suptitle_background_color')
            self.optional_attr(self.lbl_suptitle, 'foreground', 'suptitle_color')
            if self.item['suptitle_border_color']:
                self.item['suptitle_border'] = '1px solid ' + self.item['suptitle_border_color']
            self.optional_attr(self.lbl_suptitle, 'border', 'suptitle_border')
        else:
            self.lbl_suptitle.text = 'Back'
            self.lbl_suptitle.background = self.item['background_color']
            self.lbl_suptitle.foreground = self.item['background_color']
            self.lbl_suptitle.border = '1px solid ' + self.item['background_color']

        # Placeholder for spacing
        self.lbl_suptitle_copy.text = 'Back'
        self.lbl_suptitle_copy.background = self.item['background_color']
        self.lbl_suptitle_copy.foreground = self.item['background_color']

        self.rp_features.items = self.item['features']

    def form_show(self, **event_args):
        cp_dom = anvil.js.get_dom_node(self.cp_price)
        cp_dom.style.width = '300px'
        cp_dom.style.padding = '15px'
        self.optional_attr(cp_dom.style, 'borderRadius', 'border_radius')

        lbl_oldprice_dom = anvil.js.get_dom_node(self.lbl_oldprice)
        lbl_oldprice_text = lbl_oldprice_dom.querySelector('.label-text')
        lbl_oldprice_text.style.textDecorationLine = 'line-through'
        lbl_oldprice_text.style.textDecoration = 'line-through'

        lbl_suptitle_dom = anvil.js.get_dom_node(self.lbl_suptitle)
        lbl_suptitle_dom.style.padding = '0px 10px 0px 10px'
        self.optional_attr(lbl_suptitle_dom.style, 'borderRadius', 'suptitle_border_radius')

        
        if 'btn_position' in self.item and self.item['btn_position'] == 'bottom':
            btn_signup_dom = anvil.js.get_dom_node(self.btn_signup_bottom)
        else:
            btn_signup_dom = anvil.js.get_dom_node(self.btn_signup)

        btn_signup_btn = btn_signup_dom.querySelector('.btn')
        self.optional_attr(btn_signup_btn.style, 'borderRadius', 'btn_border_radius')
        if self.item['btn_border_color']:
            self.item['btn_border'] = '1px solid ' + self.item['btn_border_color']
        self.optional_attr(btn_signup_btn.style, 'border', 'btn_border')

    def btn_signup_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.js.window.location.href = self.item['btn_url']

    def optional_attr(self, target_obj, attr_name, item_key, default_value=None):
        if item_key in self.item:
            setattr(target_obj, 'visible', True)
            setattr(target_obj, attr_name, self.item[item_key])
        elif default_value:
            setattr(target_obj, attr_name, default_value)
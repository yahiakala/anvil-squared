from ._anvil_designer import ChatTemplateTemplate
import anvil


class ChatTemplate(ChatTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.primary = app.theme_colors['Primary']
        self.init_components(**properties)

        if 'img' in self.item and self.item['img']:
            self.link_loading.visible = True
            self.link_loading.add_component(
                anvil.Image(
                    source='_/theme/loading.gif',
                    role='load-message',
                    width=28,
                    height=14
                ),
                slot='img'
            )
            
        if self.item['from'] == 'bot' and 'sources' in self.item:
            self.fp_sources.visible = True
            self.src_labels = []
            for i in range(len(self.item['sources'])):
                self.src_labels.append(
                    anvil.Link(
                        text=str(i + 1) + '. ' + self.item['sources'][i]['title'],
                        url=self.item['sources'][i]['url'],
                        foreground='black',
                        role='src-link',
                        border='solid 1px black'
                    )
                )
                self.fp_source_links.add_component(self.src_labels[i])
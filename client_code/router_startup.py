from anvil_extras import routing
import anvil
from .Chatbox import Chatbox
from .Form1 import Form1
from .Form2 import Form2
from .HomeForm import HomeForm

from .TemplateForm1 import TemplateForm1
from .TemplateForm2 import TemplateForm2
from .TemplateForm3 import TemplateForm3

hash, pattern, dict = routing.get_url_components()

# Loads the template form
routing.set_url_hash(pattern)

routing.launch()
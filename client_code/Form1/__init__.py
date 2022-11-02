from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.num_entry = ""

    # Any code you write here will run before the form opens.


  def click_3(self, **event_args):
    self.num_entry = self.num_entry + "3"
    if int(self.num_entry) > 51:
      self.num_entry_color = ['#ff0000']
    else:
      self.num_entry_color = ['#000000']

  
    











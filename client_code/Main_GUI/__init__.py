from ._anvil_designer import Main_GUITemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime as dt

class Main_GUI(Main_GUITemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

    self.num_entry = ""

    self.button_1.tag = "1"
    self.button_2.tag = "2"
    self.button_3.tag = "3"
    self.button_4.tag = "4"
    self.button_5.tag = "5"
    self.button_6.tag = "6"
    self.button_7.tag = "7"
    self.button_8.tag = "8"
    self.button_9.tag = "9"
    self.button_0.tag = "0"
    self.label_1.text = "Passagerare " + dt.datetime.now().strftime("%d/%m")




  def numBtn(self, **event_args):
    self.num_entry = self.num_entry + event_args['sender'].tag
    self.text_box_1.text = self.num_entry
    print(self.num_entry)
    #print(dt.datetime.now())
    self.time = dt.datetime.now()

  def clearBtn(self, **event_args):
    self.num_entry = ""
    self.text_box_1.text = self.num_entry


  
    











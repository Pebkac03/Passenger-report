from ._anvil_designer import Main_GUI_TouchscreenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime as dt
from anvil_extras.storage import local_storage

class Main_GUI_Touchscreen(Main_GUI_TouchscreenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    if 'unsaved' in local_storage:
      print(local_storage['unsaved'])

    self.num_entry = ""
    self.trips_td = [
      {
        'Time': r['Time'].strftime("%H:%M"),
        'Direction': r['Direction'],
        'Passengers': str(r['Passengers'])
      }
      for r in app_tables.table_1.search(Date=dt.date.today())
    ]
    self.trips_td_list = [" ".join(d.values()) for d in self.trips_td]
    self.trips_td_list_reverse = self.trips_td_list.reverse()
    self.trips_td_str = "\n".join(self.trips_td_list_reverse)


    ##Tags
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
    self.button_enter_1.tag = "Tjärö - Järnavik"
    self.button_enter_2.tag = "Järnavik - Tjärö"

    self.label_1.text = "Passagerare " + dt.datetime.now().strftime("%d/%m")
    self.text_area_1.text = self.trips_td_str

    self.sim_offline = False



  def numBtn(self, **event_args):
    self.num_entry = self.num_entry + event_args['sender'].tag
    self.text_box_1.text = self.num_entry
    print(self.num_entry)
    #print(dt.datetime.now())
    self.time = dt.datetime.now()
    print(event_args)

  def clearBtn(self, **event_args):
    self.num_entry = ""
    self.text_box_1.text = self.num_entry

  def enterBtn(self, **event_args):
    now = dt.datetime.now()
    if 'unsaved' in local_storage:
      to_save = local_storage['unsaved']

      #Line 72 adds to_save['time'] as a simple object instead of a datetime object
      to_save.append({"Time": now.isoformat(), "Direction": event_args['sender'].tag, "Passengers": int(self.num_entry), "Date": dt.date.today().isoformat()})
    else:
      to_save = [{"Time": now.isoformat(), "Direction": event_args['sender'].tag, "Passengers": int(self.num_entry), "Date": dt.date.today().isoformat()}]

    if self.sim_offline:
      print("server is offline")
      local_storage['unsaved'] = to_save
    else:
      try:
        anvil.server.call_s('save', to_save)
        del local_storage['unsaved']
      except anvil.server.AppOfflineError:
        print("Server is offline")
        local_storage['unsaved'] = to_save
    

      
    
    ##app_tables.table_1.add_row(Time=now, Direction=event_args['sender'].tag, Passengers=int(self.num_entry), Date=dt.date.today())
    self.trips_td_list.insert(0, now.strftime("%H:%M") + " " + event_args['sender'].tag + " " + self.num_entry)
    self.trips_td_str = "\n".join(self.trips_td_list)
    self.text_area_1.text = self.trips_td_str
    
    self.clearBtn()

  def delBtn(self, **event_args):
    if 'unsaved' in local_storage:
      local_storage['unsaved'].pop()
      self.trips_td_list.pop()

  def simOffline_true(self, **event_args):
    self.sim_offline = True


  def simOffline_false(self, **event_args):
    self.sim_offline = False





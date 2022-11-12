from ._anvil_designer import Main_GUI_TouchscreenTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime as dt
from anvil_extras.storage import local_storage
import time

class Main_GUI_Touchscreen(Main_GUI_TouchscreenTemplate):
  def onlineUpdate(self, **event_args):
    try:
      self.trips_td = [
        {
          'Time': r['Time'].strftime("%H:%M"),
          'Direction': r['Direction'],
          'Passengers': str(r['Passengers'])
        }
        for r in app_tables.table_1.search(tables.order_by("Time", ascending=False), Date=dt.date.today())
      ]
    except anvil.server.AppOfflineError:
      pass
    else:
      self.trips_td_list = [" ".join(d.values()) for d in self.trips_td]
      self.trips_td_list.reverse()
      self.trips_td_str = "\n".join(self.trips_td_list)
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    if 'unsaved' in local_storage:
      print(local_storage['unsaved'])

    self.first_onlinecall_made = False
    self.num_entry = ""
    if 'unsaved' in local_storage:
      try:
        anvil.server.call_s('save', local_storage['unsaved'])
      except anvil.server.AppOfflineError:
        self.trips_td = [
          {
            'Time': r['Time'].fromisoformat().strftime("%H:%M"),
            'Direction': r['Direction'],
            'Passengers': str(r['Passengers'])
          }
          for r in app_tables.table_1.search(tables.order_by("Time", ascending=False), Date=dt.date.today())
        ]
        self.trips_td_list = [" ".join(d.values()) for d in self.trips_td]
        self.trips_td_list.reverse()
        self.trips_td_str = "\n".join(self.trips_td_list)
      else:
        self.first_onlinecall_made = True
    else:
      try:
        self.onlineupdate()
      except anvil.server.AppOfflineError:
        self.trips_td_str = ""
      else:
        self.first_onlinecall_made = True






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
    if local_storage['delete_count'] > 0:
      anvil.server.call_s('delete', local_storage['delete_count'])
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
      except anvil.server.AppOfflineError:
        print("Server is offline")
        local_storage['unsaved'] = to_save
        self.trips_td_list.insert(0, now.strftime("%H:%M") + " " + event_args['sender'].tag + " " + self.num_entry)
      else:
        del local_storage['unsaved']
        self.first_onlinecall_made = True
        self.onlineUpdate()
      finally
        for n, value in enumerate(self.trips_td_list[:-1]):
          ##loop through to see if entries for two days are in list, checks if a more recent hour value is lesser than the previous one
          if int(self.trips_td_list[n][0:2]) < int(self.trips_td_list[n + 1][0:2]):
            ##for loop to remove everything after self.trips_td_list[n]
            del self.trips_td_list[n + 1:]
            break
        self.trips_td_str = "\n".join(self.trips_td_list)
        self.text_area_1.text = self.trips_td_str
        self.clearBtn()





  def delBtn(self, **event_args):
    if 'unsaved' in local_storage:
      local_storage['unsaved'].pop()
      self.trips_td_list.pop()
    else:
      trips_td = self.trips_td
      self.onlineUpdate()
      if self.trips_td == trips_td:
        try:
          anvil.server.call_s('delete')
        except anvil.server.AppOfflineError:
          self.text_box_1.text("Failed, couldn't fetch most recent data")
          time.sleep(3)
          self.text_box_1.text("")
        else:
          self.onlineUpdate()
      else:
        if anvil.server.is_app_online():
          self.text_box_1.text("Cancelled, list not up to date")
          time.sleep(3)
          self.text_box_1.text("")
        else:
          self.text_box_1.text("Failed, couldn't fetch most recent data")
          time.sleep(3)
          self.text_box_1.text("")


  def simOffline_true(self, **event_args):
    self.sim_offline = True


  def simOffline_false(self, **event_args):
    self.sim_offline = False





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

    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
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

        self.trips_td_full = list()
        self.trips_td = list()
        self.trips_td_list = list()
        self.trips_td_str = str()

        if 'unsaved' in local_storage:
            try:
                anvil.server.call_s('save', local_storage['unsaved'])
            except:
                pass
            finally:
                self.update()

    # Called in case client can't save to server
    def offlineSave(self, to_add):
        # saves to local_storage['trips'] in same format as to server.
        if 'trips' in local_storage:
            local_storage['trips'].append(to_add)
        else:
            local_storage['trips'] = to_add
        # filters local_storage['trips'] to only trips from the current day
        filtered = filter(lambda c: c['Date'] == dt.date.today(), local_storage['trips'])
        local_storage['trips'] = filtered

        # Caches unsaved entries in local_storage['unsaved']
        if 'unsaved' in local_storage:
            local_storage['unsaved'].append(to_add)
        else:
            local_storage['unsaved'] = to_add

    # Updates client display and local storage
    def update(self, **event_args):
        # fetches all trips from current day from server
        try:
            self.trips_td_full = [
                {
                    'Time': r['Time'].isoformat(),
                    'Direction': r['Direction'],
                    'Passengers': str(r['Passengers']),
                    'Date': r['Date'].isoformat()
                }
                for r in app_tables.table_1.search(tables.order_by("Time", ascending=False),
                                                   Date=dt.date.today())
            ]

        # falls back to fetching from local_storage['trips'] instead of server
        except anvil.server.AppOfflineError:
            self.trips_td_full = local_storage['trips']

        # updates local_storage['trips'] to mirror server
        else:
            local_storage['trips'] = self.trips_td_full

        # parses trips to string in display-format and updates display
        finally:
            self.trips_td = []
            for n, value in enumerate(self.trips_td_full):
                self.trips_td.append({"Time": dt.datetime.fromisoformat(value['Time']).strftime("%H:%M"),
                                      "Direction": value['Direction'], "Passengers": value['Passengers']})
            self.trips_td_list = [" ".join(d.values()) for d in self.trips_td]
            self.trips_td_str = "\n".join(self.trips_td_list)
            self.text_area_1.text = self.trips_td_str

    def numBtn(self, **event_args):
        self.text_box_1.text += event_args['sender'].tag

    def clearBtn(self, **event_args):
        self.text_box_1.text = ""

    def enterBtn(self, **event_args):
        if self.text_box_1 is not "":
            now = dt.datetime.now()
            to_save = [
                {"Time": now.isoformat(), "Direction": event_args['sender'].tag,
                 "Passengers": int(self.text_box_1.text),
                 "Date": dt.date.today().isoformat()}]
            try:
                anvil.server.call_s('save', to_save)
            except anvil.server.AppOfflineError:
                self.offlineSave(to_save)
            else:
                del local_storage['unsaved']
            finally:
                self.update()
                self.num_entry = ""
                self.text_box_1.text = ""


# Needs to be changed
def delBtn(self, **event_args):
    if 'unsaved' in local_storage:
        local_storage['unsaved'].pop()
        self.trips_td_list.pop()
    else:
        trips_td = self.trips_td
        self.update()
        if self.trips_td == trips_td:
            try:
                anvil.server.call_s('delete')
            except anvil.server.AppOfflineError:
                self.text_box_1.text("Failed, couldn't fetch most recent data")
                time.sleep(3)
                self.text_box_1.text("")
            else:
                self.update()
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

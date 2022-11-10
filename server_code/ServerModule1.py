import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime as dt

@anvil.server.callable
def save(to_save):
  for n in to_save:
    print(type(n['Time']))
    row = app_tables.table_1.add_row()
    row['Time'] = dt.datetime.fromisoformat(n['Time'])
    row['Direction'] = n['Direction']
    row['Passengers'] = n['Passengers']
    row['Date'] = n['Date']
  

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

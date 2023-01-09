import canmatrix
import json

# Load the DBC file into a CanMatrix object
dbc_file = 'ms_dash.dbc'
db = canmatrix.load_dbc(dbc_file)

# Convert the CanMatrix object to a dictionary
db_dict = db.as_dict()

# Write the dictionary to a JSON file
with open('db.json', 'w') as f:
    json.dump(db_dict, f)

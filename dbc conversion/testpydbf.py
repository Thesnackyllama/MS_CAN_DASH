import json

# Open the file
with open('ms_dash.dbc', 'r') as f:
    # Read the contents of the file
    file_contents = f.read()

# Convert the file contents to a JSON string
json_str = json.dumps(file_contents)

# Print the JSON string
print(json_str)

with open('m.json', 'w') as f:
    f.write(json_str)
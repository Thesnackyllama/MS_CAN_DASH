import json

# Open the JSON file
with open('msdash.json', 'r') as f:
  # Parse the JSON data directly from the file
  parsed_data = json.load(f)

# Access the data as a Python object
#print(parsed_data['name'])

p = parsed_data['params']

dash = p[4]
ddd = dash['canId']
print(ddd)



#for params in parsed_data:
#    if params[0]:
#        print(params['name'])
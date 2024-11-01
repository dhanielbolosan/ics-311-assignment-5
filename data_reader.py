import json

def load_islands_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data
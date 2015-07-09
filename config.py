import json
import os

def get_config(config_file='config.json'):
    if os.path.isfile(config_file):
        with open(config_file) as data_file:
            data = json.load(data_file)
        return data
    else:
        print("Config File not Found")
        exit()

def save_config(data, config_file='config.json'):
    with open(config_file, 'w') as opfile:
        json.dump(data, opfile)

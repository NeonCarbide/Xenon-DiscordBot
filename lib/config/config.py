from json import load

file = open('./data/config/config.json')
config = load(file)

def get_value(self):
    return config[self]
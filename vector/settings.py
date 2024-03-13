import json


def get(key):
    with open('settings.json') as f:
        d = json.load(f)
        return d[key]


def set(key, value):
    with open('settings.json') as f:
        d = json.load(f)
    d[key] = value
    with open('settings.json', 'w') as f:
        json.dump(d, f)

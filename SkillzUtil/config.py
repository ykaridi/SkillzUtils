import json
import os

baseURL = "https://piratez.skillz-edu.org/"
buffer_size=5
config_location = os.path.join(os.path.expanduser("~"), ".SkillzUtil.conf")
soft_timeout = 30
hard_timeout = 180
user = ""
password = ""
connection_type = ""
authenticate = False
tournament_number = 0
headless = True


def fetch_config():
    try:
        with open(config_location, "r") as config_file:
            j = json.loads(config_file.read())
            attrs = globals()
            for k, v in j.items():
                attrs[k] = v
            return j
    except:
        return {}


def append_to_config(k,v):
    try:
        j = fetch_config()
        j[k] = v
        write_to_config(j)
    finally:
        pass


def write_to_config(dict):
    try:
        with open(config_location, "w") as config_file:
            config_file.write(json.dumps(dict))
        return fetch_config()
    finally:
        pass


fetch_config()

import json
import os

baseURL = "https://piratez.skillz-edu.org/"
config_location = os.path.join(os.path.expanduser("~"), ".SkillzUtil.conf")
soft_timeout = 30
hard_timeout = 180
email = ""
passwrd = ""
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
        with open(config_location, "w") as config_file:
            config_file.write(json.dumps(j))
        return fetch_config()
    finally:
        pass


fetch_config()

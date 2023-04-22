import os
from configparser import ConfigParser

CONFIG_PATH = 'conf.ini'

default_config = {
    "API": {
        "api_key": ""
    },
    "CHROMEDRIVER": {
        "path": os.path.join('chromedriver', 'chromedriver.exe')
    },
    "CONFIG": {
        "send_message_interval": 20,
    },

    # "GUI": {
    #     "window_title": "My App",
    #     "window_size": "800x600"
    # },
    # "DATA": {
    #     "csv_delimiter": ","
    # }
}

config = ConfigParser()
config.read_dict(default_config)


def save():
    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)


def load():
    config.read(CONFIG_PATH)
    return config


def get_api_key():
    if not config.has_section("API"):
        config.add_section("API")
    return config.get("API", 'api_key')


def set_api_key(api_key):
    if not config.has_section("API"):
        config.add_section("API")
    return config.set("API", "api_key", api_key)


def get_chromedriver_path():
    if not config.has_section("CHROMEDRIVER"):
        config.add_section("CHROMEDRIVER")
    return config.get("CHROMEDRIVER", 'path')


def get_send_message_interval():
    if not config.has_section("CONFIG"):
        config.add_section("CONFIG")
    return config.get("CONFIG", 'send_message_interval')


def set_send_message_interval(value):
    if not config.has_section("CONFIG"):
        config.add_section("CONFIG")
    return config.set("CONFIG", "send_message_interval", value)

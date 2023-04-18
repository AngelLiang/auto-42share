import os
from configparser import ConfigParser

CONFIG_PATH = 'conf.ini'

default_config = {
    "API": {
        "api_key": ""
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


def save():
    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)


def load():
    if not os.path.exists(CONFIG_PATH):
        # 将默认配置应用于现有配置
        config.read_dict(default_config)
        save()
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

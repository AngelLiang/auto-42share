from configparser import ConfigParser


class Config:
    CHROMEDRIVER_PATH = ''


config = Config()

conf = ConfigParser()


def read_config():
    conf.read('conf.ini')
    for key, value in conf.items():
        setattr(config, key, value)


def write_config():
    pass

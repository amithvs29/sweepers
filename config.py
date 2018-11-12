import configparser
import logging


class Config(object):
    def __init__(self, filename):
        logging.info('Loading configuration from ' + filename)
        self.my_config_parser = configparser.SafeConfigParser()
        self.my_config_parser.read(filename)

    def __getitem__(self, section):
        return dict(self.my_config_parser.items(section))

    def get(self, item, section='DEFAULT'):
        return self.my_config_parser.get(section, item)

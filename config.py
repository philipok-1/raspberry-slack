"""Config parser to handle slack config files"""

import ConfigParser
import logging
import utils
import sys, os

logger = utils.loggerMaster('slack.config')

def read_config(file):

    logger.info("Reading config file...")
    config=ConfigParser.SafeConfigParser()
    if not os.path.isfile(file):
        logger.error("config file not found")
        sys.exit("config file not found")
    config.read(file)

    dictionary={}

    for section in config.sections():
        dictionary.update(dict(config.items(section)))

    logger.info("testing module logging")

    return dictionary

if __name__==("__main__"):

    print("This is a module")
    sys.exit("Exiting")

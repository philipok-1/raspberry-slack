import logging
import sys
import re
import subprocess
import time
import random
import signal
import requests
import json


def loggerMaster(name, logfile='slack.log', logLevel='NOTSET'):

    """master function to create loggers"""

    numeric_level = getattr(logging, logLevel.upper(), 10)

    logger = logging.getLogger(str(name))
    logger.setLevel(level=logLevel)
    fh = logging.FileHandler(logfile, mode="w")
    fh.setLevel(level=logLevel)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level=logLevel)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.handlers
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.propagate=False

    return logger

logger = loggerMaster('slack.utils')

def signal_term_handler(signal, frame):

    logger.warning("Script terminated by kill command")
    sys.exit(0)

def set_signal():

    signal.signal(signal.SIGTERM, signal_term_handler)

class ConnectionDrop():

    """simple class to log connection errors"""

    def __init__(self, host, reason):

        self.timestamp = time.time()
        self.reason = str(reason)
        logger.error("Recorded: " + self.reason + " at " + str(self.timestamp))
        host.errors.append(self)


def get_temp():

    """returns the internal cpu temperature of a raspberry pi"""

    temp = subprocess.check_output(
        ["/opt/vc/bin/vcgencmd measure_temp"], shell=True)
    out = re.search(r'\d+\.\d+', temp)

    return str(out.group(0))


def post_message(token, username, text, emoji, channel='#general'):

    """sends a chat.postMessage to the specified channel.  data payload is a simple list, attachments must be json-encoded"""

    url="https://slack.com/api/chat.postMessage"
    #optional attachments:

    #attachments=json.dumps([{'pretext':'pretext', 'color':'warning', 'text':'text-test'}])

    payload = [
      ('channel', str(channel)),
      ('text', str(text)),
      ('token', str(token)),
      ('username', str(username)),
      ('icon_emoji', str(emoji)),
      #('attachments', attachments)
    ]

    req=requests.post(url, data=payload)
    logger.debug(str(req.text))

    return

def send_webhook(url, text, username, emoji=":robot:"):

    """sends a webhook into the specified channel.  payload is json format"""

    attachments=[{'color':'#00000', 'text':''}]

    payload = {'text':str(text), 'username':str(username), 'icon_emoji': str(emoji), 'attachments':attachments}

    req=requests.post(url, json=payload)
    logger.debug(str(req.text))

    return


def main():
    print "This is a module designed to be used with RaspiSlack"
    return 0

if __name__ == "__main__":

    main()

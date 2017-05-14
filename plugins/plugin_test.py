import re
import sys
import utils

logger=utils.loggerMaster("slack.plugin_test")

def plugin_main(message, host):

    logger.debug("testing plugin")
    if re.match(r'.*(shut).*', message, re.IGNORECASE):

        host.say("Shutting down")
        sys.exit("shutting down")
        pass

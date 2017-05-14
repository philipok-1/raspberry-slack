import re
import sys
import utils
import subprocess

logger=utils.loggerMaster("slack.plugin_sys")

def plugin_main(message, host):


    if re.match(r'.*(reboot).*', message, re.IGNORECASE):
        host.say("Rebooting...")
        subprocess.call("sudo reboot", shell=True)

    elif re.match(r'.*(shut).*', message, re.IGNORECASE):
        host.say("Shutting down...")
        logger.warning("shutting down via command")
        sys.exit("Bye")

    pass

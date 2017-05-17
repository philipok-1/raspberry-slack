import re

import utils, psutil

logger=utils.loggerMaster("slack.plugin_status")

def plugin_main(message, host):

    logger.debug("testing plugin")

    if re.match(r'.*(status).*', message, re.IGNORECASE):

        cpu_pct = psutil.cpu_percent(interval=1, percpu=False)
        temp = utils.get_temp()
        host.say("Hi, my CPU is at %s%%.  My temperature is %s.  I've been running Slack for %d seconds since last interrupt.  Total run time %d seconds" %
        (cpu_pct, temp, host.run_time, host.run_time_total))

    elif re.match(r'.*(IP).*', message, re.IGNORECASE):

        ip=psutil.net_if_addrs()['wlan0'][0][1]
        host.say("My IP address is "+str(ip))


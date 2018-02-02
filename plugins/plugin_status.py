import re

import utils, psutil
import subprocess
import router
import json

logger=utils.loggerMaster("slack.plugin_status")

def plugin_main(message, host):

    logger.debug("testing plugin")

    if re.match(r'.*(status).*', message, re.IGNORECASE):

        cpu_pct = psutil.cpu_percent(interval=1, percpu=False)
        temp = utils.get_temp()
        host.say("Hi, my CPU is at %s%%.  My temperature is %s.  I've been running Slack for %d seconds since last interrupt.  Total run time %d seconds" %
        (cpu_pct, temp, host.run_time, host.run_time_total))
        uptime=subprocess.check_output('uptime', shell=True)
        uptime=uptime.split('1 user')
        host.say("Uptime:  "+str(uptime[0]))

    elif re.match(r'.*(router).*', message, re.IGNORECASE):

        devices=host.config['known_devices']
        devices = devices.replace("'", "\"")
        known_devices=json.loads(devices)        
        ip=psutil.net_if_addrs()['wlan0'][0][1]
        host.say("My IP address is "+str(ip))
        host.say("Devices on router: "+str(router.scan_router('http://192.168.1.254', known_devices, rename=True)))

        


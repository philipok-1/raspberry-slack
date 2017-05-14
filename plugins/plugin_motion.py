import re

import utils, config, subprocess

logger=utils.loggerMaster("slack.plugin_motion")

def plugin_main(message, host):

    logger.debug("testing plugin")
    
    if re.match(r'.*(snapshot).*', message, re.IGNORECASE):

        configs=host.config
        WEBCAM_IP=configs['webcam_ip']
        MOTION_FOLDER=configs['motion_folder']

        subprocess.call(
                            'curl -s -o /dev/null http://' +
                            WEBCAM_IP +
                            ':8080/0/action/snapshot',
                            shell=True)

        subprocess.call(
                            "curl -F file=@" +
                            MOTION_FOLDER +
                            "lastsnap.jpg -F channels=#" +
                            host.channel_name +
                            " -F token=" +
                            host.token +
                            " https://slack.com/api/files.upload",
                            shell=True)


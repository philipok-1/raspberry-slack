# Raspberry Slack

### A set of python modules to control a Raspberry Pi via Slack

An easy to use Python script to run a bot from an RPI.  It allows you to send direct messages to a bot running on an RPI (or indeed any Linux system).  There are three plugins that the script uses to parse user messages:

* plugin_status: responds to 'status' with a readout of temperature, CPU % and running time
* plugin_motion: use on an RPI running Motion - responds to 'snapshot' with a picture from the webcam.
* plugin_sys: reponds to 'reboot' or 'shut down' and either reboots or shuts down

I plan to add more!

Script only works on Python 2.7 due to the underlying slackclient library

To use:

1. Create a bot within Slack and invite it into the #general channel

[Instructions for creating a bot can be found here](https://my.slack.com/services/new/bot)

2. Clone this repository  onto your Pi:

```BASH

$ git clone https://github.com/philipok-1/raspberry-slack
```

3.  Fill in the slack_config.conf file with appropriate API keys, usernames and webhook urls (if using). if you are using Motion you need to add local webcam IP address and the image capture location

4.  Run the Raspberry-Slack.py script from your pi (probably with sudo)

5.  send a DM on the slack channel - @rpi "send me a snapshot".  the bot will also recognise messages sent to @everyone so you can get mutiple PIS to report in

With acknowledgments to: 

[The Slack python client](https://github.com/slackapi/python-slackclient) for the main library

[youknowone](https://github.com/youknowone/slairck) for code on autoping and catching socket errors

[Never Fear](http://neverfear.org/profile/ben) for a Stack suggestion on plugin architecture

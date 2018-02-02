#!/usr/bin/env python

"""Slack bot class to control a webcam and post snapshots to Slack ."""

import re
import time
import json
import random
import datetime as dt
import subprocess
import websocket
import sys
import logging
import socket
import signal

from slackclient import SlackClient
import psutil

import utils
import lexicon as lex

sys.path.append('./plugins/')

# logging module

logger = utils.loggerMaster('slack.bot')

class SlackBot():

    """master slack client that remains alive for the duration of the script.  subsidiary connections to SlackClient are made on each connection drop or error"""

    def __init__(self, config):

        self.config=config
        self.token = self.config['api_key']
        self.slack_client = None        
        self.name = self.config['bot_name']
        self.slack_user_id = None
        self.direct_message_channels=None
        self.channel_id = None
        self.channel_name = None
        self.master=self.config['master']

        self.plugins=self.config.get('plugins', 'plugins').split('\n')
        logger.info("Plugins installed: "+str(self.plugins))

        self.last_ping = 0
        self.reconnects = 0
        self.error_count = 0
        self.run_time = 0
        self.run_time_total = 0
        self.first_time = True
        self.auth_check = True
        self.errors = []
        self.ping_frequency=15

    def test_connection(self, verbose=True):
        """tests whether the device is connected to the internet"""

        connected = False
        retries = 0
        while connected == False:
            if verbose:
                logger.info("Testing internet connection...")

            try:
                socket.create_connection(("www.google.com", 80))
                if verbose:
                    logger.info("internet working")
                connected = True
                return True

            except (socket.gaierror, socket.error):
                logger.error(
                    "Internet connection down - retrying " +
                    str(retries))
                error = utils.ConnectionDrop(self, "internet down")
                retries += 1
                time.sleep((1 + retries))

    def generate_client(self):
        """creates an instance of SlackClient for each connection"""

        if self.test_connection():
            self.reconnects += 1
            logger.info("Generating slack_client")

            # check token is valid

            self.slack_client = SlackClient(self.token)

            if self.auth_check:
                self.auth_check = False
                if self.slack_client.api_call(
                        "auth.test", token=self.token).get('ok') == False:
                    logger.error("key not recognised")
                    sys.exit("Invalid key.. exiting")

            logger.info("Token valid - SlackClient generated " +
                        str(self.slack_client))
            logger.info("Connecting to RTM...")

            #test RTM connection

            try:
                self.slack_client.rtm_connect()
                logger.info("Connected to RTM")
                self.run_time = 0

            except Exception as e:
                logger.error("Error in RTM connection: " + str(e))
                logger.warning("Exiting script...")
                sys.exit(1)

            logger.info("Getting user & channel IDs")

            #get list of users, channels and direct message channels
            
            channel_list = self.slack_client.api_call("channels.list")

            self.direct_message_channels=self.slack_client.api_call("im.list")
            
            user_list = self.slack_client.api_call("users.list")

            for channel in channel_list.get('channels'):
                if channel.get('is_member'):
                    self.channel_id = str(channel.get('id'))
                    self.channel_name = str(channel.get('name'))

            for user in user_list.get('members'):
                if user.get('name') == self.name:
                    self.slack_user_id = user.get('id')

            logger.info("Bot ID:  " +
                        str(self.slack_user_id) +
                        " Channel ID: " +
                        str(self.channel_id) +
                        "/ " +
                        str(self.channel_name))

    def say(self, text_message):
        """simple function to post a message to the bot's channel"""

        try:
            self.slack_client.api_call(
                "chat.postMessage",
                channel=self.channel_id,
                text=str(text_message),
                as_user=True)

        except (websocket.WebSocketConnectionClosedException, socket.error) as e:

            error = utils.ConnectionDrop(self, "chat connection error")

    def autoping(self):
        """pings the slack server as set by the Bot"""

        now = int(time.time())
        if now > self.last_ping + self.ping_frequency:
            self.slack_client.server.ping()
            self.last_ping = now

    def load_plugin(self, name):
        """loads the plugin for the process method"""

        plugin=__import__("plugin_%s" % name)
        return plugin

    def call_plugin(self, name, message):

       plugin= self.load_plugin(name)
       plugin.plugin_main(message, self)

    def process(self):
        """checks for connection errors, reads the RTM firehose and parses messages"""

        self.run_time += 1
        self.run_time_total += 1

        try:
            messages = self.slack_client.rtm_read()
            self.error_count = 0

            if self.first_time:
                self.say("Bot ID:"+str(self.slack_user_id)+" is awake")
                self.first_time=False

            if self.errors:
                drop_period = int(time.time()) - self.errors[0].timestamp
                self.say(
                    "I was offline for " +
                    str(drop_period) +
                    " secs.  " + str(len(self.errors)) + "errors.")
                logger.debug("Offline for " + str(drop_period) + " secs")
                self.errors = []

        except websocket.WebSocketConnectionClosedException:

            error = utils.ConnectionDrop(self, "websocket drop")
            self.generate_client()
            return

        except socket.error:

            error = utils.ConnectionDrop(self, "Socket error")
            time.sleep(5)
            self.error_count += 1

            if self.error_count > 5:
                self.generate_client()
            return

        #checks the message stream

        for message in messages:
            #print (message)

            if message['type'] == 'presence_change':
                if message['presence'] == 'active':
                    time.sleep(.5)
                    self.say(lex.response('greetings')+" "+str(self.master))

            if 'text' in message:
                if message['text'].startswith(
                        "<@%s>" %
                        self.slack_user_id) or 'text' in message and message['text'].startswith(
                        "<!%s>" %
                        'everyone'):

            #if user issues a command, run through through all plugins

                    message_text = message['text']
                    for plugin in self.plugins:
                        self.call_plugin(plugin, message_text)

        self.autoping()


if __name__ == ('__main__'):

    print ("This is a module")

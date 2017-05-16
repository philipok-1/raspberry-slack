import logging
import sys
import re
import time
import random
import utils

logger = utils.loggerMaster('slack.lexicon')

def response(type):

    phrases={'greetings':[", welcome back", "hi there", "good to see you again", "hello again", "hi"],

    'farewells':['bye', 'see you later', 'farewell', 'see you soon']

    }


    try:

        length=len(phrases[type])
        return phrases[type][(random.randint(0,length-1))]
    except KeyError:
        logger.error('lexicon read error')
        return ('There is an error in the lexicon file you idiot')


def main():
    print "This is a module designed to be used with RaspiSlack"

if __name__ == "__main__":

    main()

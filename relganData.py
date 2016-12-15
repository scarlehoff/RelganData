#!/usr/bin/env python

import json
import request

from configurationData import TOKEN # Unique identifier

URL   = "https://api.telegram.org/bot{}/".format(TOKEN)

# Some methods copied from
# https://www.codementor.io/garethdwyer/tutorials/building-a-telegram-bot-using-python-part-1-goi5fncay

def get_url(url):

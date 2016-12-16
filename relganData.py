#!/usr/bin/env python

import json
import requests
import urllib

from configurationData import TOKEN # Unique identifier

URL   = "https://api.telegram.org/bot{}/".format(TOKEN)

# Some methods copied from
# https://www.codementor.io/garethdwyer/tutorials/building-a-telegram-bot-using-python-part-1-goi5fncay

def get_url(url):
    # returns the response of a given url
    response = requests.get(url)
    content  = response.content.decode("utf-8")
    return content

def get_json_from_url(url):
    # given some url, returns json content
    content =  get_url(url)
    js      =  json.loads(content)
    return js

def get_updates(offset=None):
    # Returns a json with the last messages the bot has received
    # If an offset is provided, we won't ask telegram for any previous messages 
    # we use longpolling to keep the connection open N seconds
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js  = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    # Parse the json and returns the message and the chat_id
    num_updates =  len(updates["result"])
    last_update =  num_updates - 1
    text        =  updates["result"][last_update]["message"]["text"]
    chat_id     =  updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    # Send a message given some id
    text =  urllib.parse.quote_plus(text)
    url  =  URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def get_last_update_id(updates):
    # Calculates the last upadte id
    update_ids =[]
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def process_all(updates):
    for update in updates["result"]:
        msge = update["message"]
        text = msge["text"]
        chat = msge["chat"]["id"]
        send_message(text, chat)

def main():
    import time
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            process_all(updates)
        time.sleep(0.5)
#     last_textchat = (None, None)
#         text, chat = get_last_chat_id_and_text(get_updates())
#         if (text, chat) != last_textchat:
#             send_message(text, chat)
#             last_textchat = (text, chat)
#         time.sleep(0.5)

if __name__ == '__main__':
    main()


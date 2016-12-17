#!/usr/bin/env python

#
# Relgan Telegram Bot
#

from TelegramUtil import TelegramUtil
from UpdateUtil import UpdateUtil
from sqhelper import basedatos

def main():
    # Activate the database
    db = basedatos("Relgan.dat")
    # Create Tables if the don't exist:
    try:
        db.createTableText(["personaje", "caracteristica", "poder"], "habilidad")
    except:
        pass
    try:
        db.createTableText(["nombre", "imgpath"], "poder")
    except:
        pass
    ut = TelegramUtil()
    ut = TelegramUtil()
    from time import sleep
    while True:
        updates = ut.getUpdates()
        for update in updates:
            print(update)
            lastUpdate   = UpdateUtil(update, db)
            chatId       = lastUpdate.chatId
            typeResponse = lastUpdate.processCommand()
            response     = lastUpdate.response
            if typeResponse == 1:
                ut.sendMessage(response, chatId)
            elif typeResponse == 2:
                ut.sendImage(response, chatId)
                pass


if __name__ == '__main__':
    main()

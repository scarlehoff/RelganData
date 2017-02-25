#!/usr/bin/env python3

#
# Relgan Telegram Bot
#

from TelegramUtil import TelegramUtil
from sqhelper import Basedatos
from Message import Message
from ProcessUpdate import ProcessUpdate

def main():
    # Activate the database
    db = Basedatos("Relgan.dat")
    # Create poder if the table don't exist:
    try:
        db.createTableText(["nombre", "imgpath"], "poder")
    except:
        pass
    ut = TelegramUtil()
    while True:
        try:
            updates = ut.getUpdates()
            for update in updates:
                updateParsed = Message(update)
                if updateParsed.ignore:
                    continue
                else:
                    _ = ProcessUpdate(updateParsed, db, ut)
        except Exception as e:
            print("Error: ")
            print(str(e))

if __name__ == '__main__':
    main()

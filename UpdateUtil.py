class UpdateUtil():
    def __init__(self, update, db):
        self.update   = update # dict
        self.db       = db
        self.response = "Command not recognised"
        self.command  = None
        typeMsg       = "message"
        if typeMsg not in update.keys():
            typeMsg = "edited_message"
        try:
            msg = update[typeMsg]
        except:
            print("Not message or edited_message")
            print(update)
            print("///////")
            return
        try:
            chat        = msg['chat']
            self.chatId = chat['id']
            self.type   = chat['type']
            self.username = msg['from']['username']
            if "entities" in msg.keys():
                if msg['entities'][0]['type'] == "bot_command":
                    text         = msg['text'].split(' ',1)
                    self.command = text[0]
                    self.arg     = text[-1]
                else:
                    return
        except:
            print("Something went wrong while parsing the json, unexpected dictionary")
            print(update)
            print("///////")
            return

    def __printHabilidad(self):
        args = self.arg.split(' ')
        if len(args) == 2:
            info = self.db.readTable("habilidad","personaje",args[0])
            print(info)
        else:
            return self.__printError("Necesitas mas argumentos para esto cabesa")
        return 1

    def __printPoder(self):
        return 2

    def __storeInfo(self):
        args = self.arg.split(' ')
        if args[0] == "habilidad" and len(args) == 4:
            self.db.insertDataInTable(args[1:], "habilidad")
        else:
            return self.__printError("Necesitas mas argumentos para esto cabesa")
        return 0

    def __printError(self, errorMsg):
        self.response = errorMsg
        return 1

    def processCommand(self):
        print(self.command)
        if self.command == "/habilidad":
            return self.__printHabilidad()
              # text
        elif self.command == "/poder":
            return self.__printPoder()
              # img
        elif self.command == "/store":
            return self.__storeInfo()
             # nothing
        else:
            return 1 # text

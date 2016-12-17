class UpdateUtil():
    def __init__(self, update, db):
        self.update   = update # dict
        self.db       = db
        self.response = "Command not recognised"
        self.command  = None
        self.imgInfo  = None
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
            chat          = msg['chat']
            self.chatId   = chat['id']
            self.type     = chat['type']
            self.username = msg['from']['username']
            if "entities" in msg.keys():
                if msg['entities'][0]['type'] == "bot_command":
                    text         = msg['text'].split(' ', 1)
                    self.command = text[0]
                    self.arg     = text[-1]
                else:
                    return
            elif "caption" in msg.keys():
                text         = msg['caption'].split(' ', 1)
                self.command = text[0]
                self.arg     = text[-1]
                self.imgInfo = msg['photo'][-1]
                self.fileId  = self.imgInfo['file_id']
        except:
            print("Something went wrong while parsing the json, unexpected dictionary")
            print(update)
            print("///////")
            return

    def __saveImg(self):
        if self.imgInfo:
            from TelegramUtil import TelegramUtil
            t       = TelegramUtil()
            fileUrl = t.getFilePath(self.fileId)
            from urllib import request
            filename = "img/" + self.fileId
            resource = request.urlretrieve(fileUrl, filename)
            return filename

    def __printHabilidad(self):
        args = self.arg.split(' ')
        if len(args) == 2:
            info = self.db.readTable("habilidad",["personaje","caracteristica"],args,"poder")
            if len(info) > 0:
                self.response = "The answer is: "
                for i in info: self.response += i[0]
            else:
                self.response = "Could not find this value in the database, I'm so so sorry"
        else: 
            return self.__printError("Necesitas mas argumentos para esto cabesa")
        return 1

    def __printPoder(self):
        imgpath = self.db.readTable("poder", "nombre", self.arg, "imgpath")
        if len(imgpath) > 0:
            for i in imgpath:
                self.response = i[0] #if there's more than one, send the last one!
        else:
            return self.__printError("Can't find it")
        return 2

    def __storeInfo(self):
        args = self.arg.split(' ')
        if args[0] == "habilidad" and len(args) == 4:
            self.db.insertDataInTable(args[1:], "habilidad")
        elif args[0] == "poder":
            # guardamos la imagen una carpeta img/algo
            imgPath = self.__saveImg()
            self.db.insertDataInTable([self.arg, imgPath], "poder")
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

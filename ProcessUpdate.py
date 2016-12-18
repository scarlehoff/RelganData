class ProcessUpdate:
    def __init__(self, update, db, telegram):
        self.update   = update   # Message Class
        self.db       = db       # basedatos Class
        self.telegram = telegram # TelegramUtil Clss
        self.response = None
        self.__debugFunction() # print debug
        if self.update.isCommand:
            command = self.update.command
        else:
            self.__sendHelp()
            return
        habilidad = "habilidad"
        poder     = "poder"
        store     = "store"
        if command == "habilidad":
            self.__printHabilidad()
        elif command == "poder":
            self.__printPoder()
        elif command == "store":
            self.__storeInfo()
        else:
            self.__printError("Command not recognised")

    # Wrappers for the Telegram class
    def __sendMessage(self, text):
        self.telegram.sendMessage(text, self.update.chatId)
    def __sendImage(self, imgPath):
        self.telegram.sendImage(imgPath, self.update.chatId)

    # Actual function
    def __debugFunction(self):
        # Just prints a bunch of stuff 
        print("> > Message received:")
        print("     From: " + self.update.username)
        print("     Is it a group?: " + str(self.update.isGroup))
        print("     Content: " + self.update.command + " " + self.update.text)
        print("     Does it have a file?: " + str(self.update.isFile))
        print("     The whole thing is: " + str(self.update.json))
    def __sendHelp(self):
        helpmsg = "This is the help message, it is useless because my Master is very lazy, sorry"
        self.__sendMessage(helpmsg)
        
    def __saveImg(self):
        fileUrl  = self.telegram.getFilePath(self.update.fileId)
        from urllib import request
        filename = "img/" + self.update.fileId
        resource = request.urlretrieve(fileUrl, filename)
        return filename

    def __printHabilidad(self):
        args = self.update.text.split(' ') # should be "personaje caracteristica"
        if len(args) == 2:
            info = self.db.readTable("habilidad",["personaje","caracteristica"],args,"poder")
            if len(info) > 0:
                response = "The answer is: "
                for i in info: response += i[0]
            else:
                self.__printError("Could not find this value in the database, I'm so so sorry")
                return
        else: 
            self.__printError("Illo, es /habilidad personaje caracteristica, no me lies")
            return
        self.__sendMessage(response)

    def __printPoder(self):
        imgpaths = self.db.readTable("poder", "nombre", self.update.text, "imgpath")
        if len(imgpaths) > 0:
            for i in imgpaths:
                imagePath = i[0] #if there's more than one, send the last one!
        else:
           self.__printError("Can't find it")
           return
        self.__sendImage(imagePath)

    def __storeInfo(self):
        args = self.update.text.split(' ')
        if args[0] == "habilidad" and len(args) == 4:
            self.db.insertDataInTable(args[1:], "habilidad")
        elif args[0] == "poder":
            if self.update.isFile:
                imgPath = self.__saveImg()
                imgName = self.update.text.split(' ', 1)[-1]
                self.db.insertDataInTable([imgName, imgPath], "poder")
            else:
                self.__printError("Necesito una imagen para el poder tiiio!")
                return
        else:
            self.__printError("Necesitas mas argumentos para esto cabesa")
            return
        self.__sendMessage("Oido cocina!")

    def __printError(self, errorMsg):
        self.__sendMessage("Error: " + errorMsg)
        

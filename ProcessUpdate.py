class ProcessUpdate:
    def __init__(self, update, db, telegram):
        self.update   = update   # Message Class
        self.db       = db       # basedatos Class
        self.telegram = telegram # TelegramUtil Clss
        self.response = None
        self.mapPath  = "img/mapImg"
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
        elif command == "map" or command == "mapa":
            self.__mapProcess(True)
        elif command == "masaje":
            self.__sendMessage("a ver, túmbate en esa camilla")
        elif command == "r" or command == "roll":
            self.__rollDice()
        elif command == "start":
            self.__sendMessage("Welcome!")
        elif command == "battlestat" or command == "status":
            self.__battleStatus()
        else:
            self.__printError("Command not recognised")

    # Wrappers for the Telegram class
    def __sendMessage(self, text):
        self.telegram.sendMessage(text, self.update.chatId)
    def __sendImage(self, imgPath):
        self.telegram.sendImage(imgPath, self.update.chatId)

    # Actual functionality
    def __debugFunction(self):
        # Just prints a bunch of stuff 
        print("> > Message received:")
        print("     From: " + self.update.username)
        print("     Is it a group?: " + str(self.update.isGroup))
        print("     Content: " + self.update.command + " " + self.update.text)
        print("     Does it have a file?: " + str(self.update.isFile))
        print("     The whole thing is: " + str(self.update.json))

    def __battleStatus(self):
        from Character import Character
        args = self.update.text
        if args == "all":
            dummyChar = Character("Dummy")
            dummyChar.printStatus(allStat=True)
        else:
            character = Character(self.db, args)
            if character.exists:
                text      = character.readStatus()
                textFinal = " > " + args + ":\n" + text
                self.__sendMessage(textFinal)
            else:
                self.__printError("¿Y " + args + " quién coño eh?")
                return

    def __sendHelp(self):
        helpmsg = "This is the help message, it is useless because my Master is very lazy, sorry"
        self.__sendMessage(helpmsg)
        
    def __saveImg(self, fileOut = None):
        fileUrl  = self.telegram.getFilePath(self.update.fileId)
        from urllib import request
        if fileOut:
            filename = fileOut
        else:
            filename = "img/" + self.update.fileId
        resource = request.urlretrieve(fileUrl, filename)
        return filename

    def __mapProcess(self, info = None):
        # If the message have a file, store it, else, print it
        if self.update.isFile:
            dummy = self.__saveImg(self.mapPath)
            if info: self.__sendMessage("Oido cocina!")
        else:
            self.__sendImage(self.mapPath)

    def __printHabilidad(self):
        from Character import Character
        args = self.update.text.split(' ') # should be "personaje caracteristica"
        if len(args) == 2:
            character = Character(self.db, args[0])
            # TODO: Allow for people not writing stuff correctly
            info      = character.printSkill(args[1])
            if info:
                response = "The answer is: " + info
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
        from Character import Character
        if args[0] == "habilidad" and len(args) == 4:
            charName  = args[1]
            skillName = args[2]
            value     = args[3]
            character = Character(self.db, charName)
            if not character.exists:
                self.__printError("¿Pero este señor quién es?")
                return
            error     = character.modifyEntity(skillName, value)
            if error == -1:
                self.__printError("Probablemente te has confundido al escribir " + skillName)
                return
            elif error == -2:
                self.__printError("Ya has roto algo... pero esto no ha funcionado")
                return
        elif args[0] == "map" or args[0] == "mapa":
            self.__mapProcess()
        elif args[0] == "poder":
            if self.update.isFile:
                imgPath = self.__saveImg()
                imgName = self.update.text.split(' ', 1)[-1]
                self.db.insertDataInTable([imgName, imgPath], "poder")
            else:
                self.__printError("Necesito una imagen para el poder tiiio!")
                return
        elif args[0] == "battlestat" or args[0] == "status":
            charName = args[1]
            text     = ""
            for i in args[2:]: text += i + " "
            character = Character(self.db, charName)
            if character.exists:
                character.setStatus(text)
            else:
                self.__printError("¿Pero este señor quién es?")
                return
        else:
            self.__printError("Necesitas mas argumentos para esto cabesa")
            return
        self.__sendMessage("Oido cocina!")

    def __parseDice(self):
        text  = self.update.text
        plus  = 9999
        minus = 9999
        if '+' in text:
            plus = text.index('+')
        if '-' in text:
            plus = text.index('-')
        if plus == minus:
            dice = text.split(' ', 1)[0]
            mod  = None
        elif plus > minus:
            cleanText = text.split(' ',1)[0]
            dice = cleanText.split('-', 1)[0]
            mod  = cleanTtext.split('-', 1)[1]
        elif minus > plus:
            cleanText = text.split(' ',1)[0]
            dice = cleanText.split('+', 1)[0]
            mod  = cleanText.split('+', 1)[1]
        else:
            self.__printError("Vaya, esto no me lo esperaba")
            return
        return dice, mod

    def __rollDice(self):
        texts     = self.update.text.split(' ',1)
        dice, mod = self.__parseDice() #self.update.text.split('+',1)
        if len(texts) == 2:
            text = texts[-1]
        else:
            text = ""
        # First let the dice roll!
        from random import randint
        try:
            if 'd' in dice:
                ndice  = int(dice.split('d')[0])
                nface  = int(dice.split('d')[-1])
                result = []
                for i in range(ndice):
                    result.append(randint(1,nface))
            else:
                self.__printError("Syntax error: Se escribe tal que: /r 2d20+4-5 cosas")
                return
        except:
            self.__printError("Syntax error: Se escribe tal que: /r 2d20+4-5 cosas")
            return
        # Now, sum everything and add any possible modifier!
        finalResult = 0
        finalStr    = ""
        for i in result:
            finalResult += i
            finalStr    += "(" + str(i) + ")" + " + "
        if mod:
            modifiers    = eval(mod) # spooky
            finalResult += modifiers
            finalStr    += mod
        else:
            finalStr = finalStr[:-3] 
        finalStr += " = " + str(finalResult)
        # Aaaand print
        finalMsg  = self.update.username + " rolled " + text + ":"
        finalMsg += "\n" + finalStr
        self.__sendMessage(finalMsg)

    def __printError(self, errorMsg):
        self.__sendMessage("Error: " + errorMsg)
        

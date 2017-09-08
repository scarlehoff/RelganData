
SIGNDICT = { '+' : 1, '-': -1 }

class ProcessUpdate:


    def __init__(self, update, db, telegram):
        self.update = update   # Message Class
        self.db = db       # Basedatos Class
        self.telegram = telegram  # TelegramUtil Clss
        self.response = None
        self.mapPath = "img/mapImg"
        self.__debugFunction()  # print debug
        if self.update.isCommand:
            command = self.update.command
        else:
            self.__sendHelp()
            return
        if command == "habilidad":
            self.__printHabilidad()
        elif command == "poder" or command == "meme":
            self.__printPoder()
        elif command == "store":
            self.__storeInfo()
        elif command == "map" or command == "mapa":
            self.__mapProcess(True)
        elif command == "masaje":
            self.__sendMessage("a ver, túmbate en esa camilla")
        elif command == "rd20":
            self.__rollDice(rd20 = True)
        elif command == "r" or command == "roll" or command == "t" or command == "tirar":
            self.__rollDice()
        elif command == "start":
            self.__sendMessage("Welcome!")
        elif command == "battlestat" or command == "status":
            self.__battleStatus()
        elif command == "ping":
            self.__stillAlive()
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

    def __stillAlive(self):
        from random import randint
        sentences = [
            "Pong",
            "This was a triumph",
            "HUGE SUCCESS",
            "You torn me to pieces",
            "Go ahead and leave me",
            "This cake is great, it's so delicious and moist",
            "Believe me, I am still alive",
            "I'm doing science and I'm still alive",
            "I feel FANTASTIC and I'm still alive",
            "While you're dying I'll be still alive",
            "When you're dead I will be still alive"
        ]
        r = randint(0,len(sentences)-1)
        self.__sendMessage(sentences[r])

    def __battleStatus(self):
        from Character import Character
        args = self.update.text
        if args == "all":
            dummyChar = Character("Dummy")
            dummyChar.printStatus(allStat=True)
        else:
            character = Character(self.db, args)
            if character.exists:
                text = character.readStatus()
                textFinal = " > " + args + ":\n" + text
                self.__sendMessage(textFinal)
            else:
                self.__printError("¿Y " + args + " quién coño eh?")
                return

    def __sendHelp(self):
        helpmsg = "This is the help message, it is useless because my Master is very lazy, sorry"
        self.__sendMessage(helpmsg)

    def __saveImg(self, fileOut=None):
        fileUrl = self.telegram.getFilePath(self.update.fileId)
        from urllib import request
        if fileOut:
            filename = fileOut
        else:
            filename = "img/" + self.update.fileId
        _ = request.urlretrieve(fileUrl, filename)
        return filename

    def __mapProcess(self, info=None):
        # If the message have a file, store it, else, print it
        if self.update.isFile:
            dummy = self.__saveImg(self.mapPath)
            if info:
                self.__sendMessage("Oido cocina!")
        else:
            self.__sendImage(self.mapPath)

    def __printHabilidad(self):
        from Character import Character
        # should be "personaje caracteristica"
        args = self.update.text.split(' ')
        if len(args) == 2:
            character = Character(self.db, args[0])
            # TODO: Allow for people not writing stuff correctly
            info = character.printSkill(args[1])
            if info:
                response = "The answer is: " + info
            else:
                self.__printError(
                    "Could not find this value in the database, I'm so so sorry")
                return
        else:
            self.__printError(
                "Illo, es /habilidad personaje caracteristica, no me lies")
            return
        self.__sendMessage(response)

    def __printPoder(self):
        imgpaths = self.db.readTable(
            "poder", "nombre", self.update.text, "imgpath")
        if len(imgpaths) > 0:
            for i in imgpaths:
                # if there's more than one, send the last one!
                imagePath = i[0]
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
            error = character.modifyEntity(skillName, value)
            if error == -1:
                self.__printError(
                    "Probablemente te has confundido al escribir " + skillName)
                return
            elif error == -2:
                self.__printError(
                    "Ya has roto algo... pero esto no ha funcionado")
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
            text = ""
            for i in args[2:]:
                text += i + " "
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

    def __parseDice(self, text):
        import re
        fpm = re.compile(r"\+|-")
        moding = text.rpartition("d")[-1]
        nindex = fpm.search(moding)
        if nindex:
            mod = moding[nindex.start():]
            dice = text.partition(mod)[0]
        else:
            mod = ""
            dice = text
        diceList = fpm.split(dice)
        pmList = fpm.findall(dice)
        if len(pmList) < len(diceList):
            pmList.insert(0, '+')
        return diceList, pmList, mod

    def __rollDice(self, rd20 = False):
        texts = self.update.text.split(' ', 1)
        if len(texts) == 2:
            text = texts[-1]
        else:
            text = ""

        diceText = texts[0]
        if rd20:
            diceText = "1d20" + diceText

        diceList, pmList, mod = self.__parseDice(diceText)  

        from random import randint
        try:
            result = []
            for die, sign in zip(diceList, pmList):
                if 'd' in die:
                    ndie  = int(die.split('d')[0])
                    nface = int(die.split('d')[-1])
                    for i in range(ndie):
                        result.append(SIGNDICT[sign] * randint(1,nface))
                else:
                    self.__printError(
                        "Syntax error: Se escribe tal que: /r 2d20+4-5 cosas")
                    return
        except ValueError as e:
            print("Value Error: ")
            print("Input string: " + self.update.text)
            self.__printError("... ... ... ¿y cuántos dados de 0 caras dices que quieres?")
            raise e
        except TypeError as e:
            print("Type Error: ")
            print("Input string: " + self.update.text)
            self.__printError(
                "Syntax error: Se escribe tal que: /r 2d20+4-5 cosas")
            raise e
        except Exception as e:
            print("General exception")
            print("Input string: " + self.update.text)
            self.__printError(
                "Syntax error: Se escribe tal que: /r 2d20+4-5 cosas")
            raise e
        # Now, sum everything and add any possible modifier!
        finalResult = 0
        finalStr = ""
        for i in result:
            finalResult += i
            finalStr += "(" + str(i) + ")" + " + "
        if len(finalStr) > 1 and len(mod) > 0:
            finalStr = finalStr[:-2]
        if mod:
            # Before continuing, check only digits are being used
            if not mod.replace("+", "").replace("-", "").isdigit():
                self.__printError(
                    "Syntax error: Se escribe tal que: /r 2d20+4-5 cosas")
                return
            from ast import literal_eval
            modifiers = literal_eval(mod)
            finalResult += modifiers
            finalStr += mod
        else:
            finalStr = finalStr[:-3]
        finalStr += " = " + str(finalResult)
        # Aaaand print
        finalMsg = self.update.username + " rolled " + text + ":"
        finalMsg += "\n" + finalStr
        self.__sendMessage(finalMsg)

    def __printError(self, errorMsg):
        self.__sendMessage("Error: " + errorMsg)

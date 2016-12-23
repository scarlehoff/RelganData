class Character:

    def __init__(self, database, name):
        from SkillSet import statList, skillList
        self.finalList = statList + skillList
        self.nameField = self.finalList[0]
        self.db        = database
        self.tablename = "habilidad"
        self.skillSet  = {}
        try:
            self.__newTableCharacter()
        except:
            pass
        self.name  = name
        self.exist = False

    def readEntity(self):
        # Check whether the character exists and read database if that's the case
        # return true if it exists and false otherwise
        characterQuery = self.db.readTable(self.tablename, self.nameField, self.name)
        # In principle there should be ONLY one value for each character and cannot be 
        # overwritten (only modified) so this should be safe:
        character = characterQuery[0][1:]
        for skill, value in zip(self.finalList, character):
            self.skillSet[skill] = value

    def printEntity(self):
        return self.skillSet

    def printSkill(self, skillName):
        return self.skillSet[skillName]

    def outEntity(self):
        dictOut = {}
        return dictOut

    def saveNewEntity(self, dictionary):
        # store into database
        inputList = []
        for skill in self.finalList:
            inputList.append(dictionary[skill])
        self.db.insertDataInTable(inputList, self.tablename)

    def modifyEntity(self, field, value): 
        # TODO: Check field is actually in the list of fields
        self.db.modifyRecord(self.tablename, field, value, self.nameField, self.name)
        # Update character
        self.readEntity()

    def __newTableCharacter(self):
        # TODO: Check fields in SkillSet == fields in  table
        self.db.createTableText(self.finalList, self.tablename)


if __name__ == "__main__":
    from SkillSet import statList, skillList
    from sqhelper import basedatos
    print("Testing character class: ")
    charName = input("Enter the new character name: ")
    dictIn = {}
    j      = 0
    listTo = statList + skillList
    for skill in listTo:
        dictIn[skill] = str(j)
        j += 1
    dictIn[listTo[0]] = charName
    # Create a new character and save it the database
    database  = basedatos("Relgan.dat")
    newCharacter = Character(database, charName)
    newCharacter.saveNewEntity(dictIn)
    # Read the character back from the database
    print("Reading an old character:")
    oldCharacter = Character(database, charName)
    oldCharacter.readEntity()
    dictOut = oldCharacter.printEntity()
    for skill in listTo:
        print(skill + ": " + dictOut[skill]) 
    print("Modifying some skill:")
    oldCharacter.modifyEntity(listTo[5], "Pepito")
    dictOut = oldCharacter.printEntity()
    for skill in listTo:
        print(skill + ": " + dictOut[skill]) 
    print(oldCharacter.printSkill("Engañar"))




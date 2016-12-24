class Character:

    def __init__(self, database, name):
        if __name__ == "Character":
            from SkillSet import statList, skillList, nameField
        else:
            from .SkillSet import statList, skillList, nameField
        # TODO: This should be input!
        self.finalList = statList + skillList
        self.nameField = nameField
        self.db        = database
        self.tablename = "habilidad"
        self.skillSet  = {}
        try:
            self.__newTableCharacter()
        except:
            pass
        self.name   = name
        self.exists = self.__readEntity()
    
    def __newTableCharacter(self):
        # TODO: Check fields in SkillSet == fields in  table
        self.db.createTableText(self.finalList, self.tablename)

    def __readEntity(self):
        # Check whether the character exists and read database if that's the case
        # return true if it exists and false otherwise
        characterQuery = self.db.readTable(self.tablename, self.nameField, self.name)

        if len(characterQuery) == 1:
            character = characterQuery[0][1:]
        elif len(characterQuery) == 0:
            return False
        else:
            print(" >> There was something wrong in the Character reading, more than 1 character")
            print(" CharacterQuery: ")
            print(characterQuery)
            print("Let's treat it as true for safety and select the last one")
            character = characterQuery[-1][1:]

        for skill, value in zip(self.finalList, character):
            self.skillSet[skill] = value
        return True

    def printEntity(self):
        return self.skillSet

    def printSkill(self, skillName):
        if skillName in self.finalList:
            return self.skillSet[skillName]
        else:
            return None

    def saveNewEntity(self, dictionary):
        # store into database
        inputList = []
        for skill in self.finalList:
            inputList.append(dictionary[skill])
        self.db.insertDataInTable(inputList, self.tablename)
        # Update character
        self.exists = self.__readEntity()

    def modifyEntity(self, field, value): 
        # TODO: Check field is actually in the list of fields
        self.db.modifyRecord(self.tablename, field, value, self.nameField, self.name)
        # Update character
        self.exists = self.__readEntity()



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
    dictOut = oldCharacter.printEntity()
    for skill in listTo:
        print(skill + ": " + dictOut[skill]) 
    print("Modifying some skill:")
    oldCharacter.modifyEntity(listTo[5], "Pepito")
    dictOut = oldCharacter.printEntity()
    for skill in listTo:
        print(skill + ": " + dictOut[skill]) 
    print(oldCharacter.printSkill("Engañar"))




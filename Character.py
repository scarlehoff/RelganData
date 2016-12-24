# -*- coding: utf-8 -*-
class Character:

    def __init__(self, database, name):
        if __name__ == "Character" or __name__ == "__main__":
            from SkillSet import nameField, skillList, utf8dict
        else:
            from .SkillSet import nameField, skillList, utf8dict
        # TODO: This should be input!
        self.finalList = [utf8dict[idSk] for idSk in skillList]
        self.skillIds  = skillList
        self.nameField = nameField
        self.db        = database
        self.tablename = "habilidad"
        self.skillSet  = {}
        self.idSet     = {}
        try:
            self.__newTableCharacter()
        except:
            pass
        self.name   = name
        self.exists = self.__readEntity()
    
    def __newTableCharacter(self):
        # TODO: Check fields in SkillSet == fields in  table
        self.db.createTableText(self.skillIds, self.tablename)

    def __readEntity(self):
        # Check whether the character exists and read database if that's the case
        # return true if it exists and false otherwise
        characterQuery = self.db.readTable(self.tablename, self.nameField, self.name)

        if len(characterQuery) == 1:
            character = characterQuery[0][1:] # Remove id field
        elif len(characterQuery) == 0:
            return False
        else:
            print(" >> There was something wrong in the Character reading, more than 1 character")
            print(" CharacterQuery: ")
            print(characterQuery)
            print("Let's treat it as true for safety and select the last one")
            character = characterQuery[-1][1:]

        for skid, skill, value in zip(self.skillIds, self.finalList, character):
            self.skillSet[skill] = value
            self.idSet[skid]     = value
        return True

    def __saveNewEntity(self, dictionary, idList):
        # store into database
        inputList = []
        for skill in idList:
            inputList.append(dictionary[skill])
        self.db.insertDataInTable(inputList, self.tablename)
        # Update character
        self.exists = self.__readEntity()

    def printEntity(self):
        return self.skillSet

    def printEntityById(self):
        return self.idSet

    def printSkill(self, skillName):
        if skillName in self.finalList:
            return self.skillSet[skillName]
        else:
            return None

    def saveNewEntityByName(self, dictionary):
        self.__saveNewEntity(dictionary, self.finalList)

    def saveNewEntityById(self, dictionary):
        self.__saveNewEntity(dictionary, self.skillIds)

    def modifyEntity(self, field, value): 
        # TODO: Check field is actually in the list of fields
        # Let's get the index of the field to ge the idname of the field
        if "sk" in field:
            fieldId = field
        else:
            index   = self.finalList.index(field)
            fieldId = self.skillIds[index]
        self.db.modifyRecord(self.tablename, fieldId, value, self.nameField, self.name)
        # Update character
        self.exists = self.__readEntity()

    def modifyEntireEntity(self, dictIn):
        keys   = dictIn.keys()
        values = []
        if self.skillIds[-1] in keys:
            if self.nameField not in keys:
                dictIn[self.nameField] = self.name
            for skillId in self.skillIds:
                values.append(dictIn[skillId])
        elif self.finalList[-1] in keys:
            idxname = self.skillIds.index(self.nameField)
            if self.finalList[idxname] not in keys:
                dictIn[self.finalList[idxname]] = self.name
            for skillName in self.finalList:
                values.append(dictIn[skillId])
        self.db.modifyRecordMany(self.tablename, self.skillIds, values, self.nameField, self.name)
        # Update character
        self.exists = self.__readEntity()

if __name__ == "__main__":
    from SkillSet import skillList
    from sqhelper import basedatos
    print("Testing character class: ")
    charName = input("Enter the new character name: ")
    dictIn = {}
    j      = 0
    listTo = skillList
    for skill in listTo:
        dictIn[skill] = str(j)
        j += 1
    dictIn[listTo[0]] = charName
    # Create a new character and save it the database
    database  = basedatos("Relgan.dat")
    newCharacter = Character(database, charName)
    newCharacter.saveNewEntityById(dictIn)
    # Read the character back from the database
    print("Reading an old character:")
    oldCharacter = Character(database, charName)
    dictOut = oldCharacter.printEntity()
    listNames = oldCharacter.finalList
    for skill in listNames:
        print(skill + ": " + dictOut[skill]) 
    print("Modifying some skill:")
    oldCharacter.modifyEntity(listNames[5], "Pepito")
    dictOut = oldCharacter.printEntity()
    listNames = oldCharacter.finalList
    for skill in listNames:
        print(skill + ": " + dictOut[skill]) 
#    print(oldCharacter.printSkill("Engañar"))




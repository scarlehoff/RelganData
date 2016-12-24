# This is just a few wrappers to be called by the web server
# -*- coding: utf-8 -*-

def dropNameField(listIn, nameField, listIn2 = None):
    listOut1 = []
    listOut2 = []
    if listIn2:
        listLoop = zip(listIn, listIn2)
    else:
        listLoop = zip(listIn, listIn)
    for i,j in listLoop:
        if nameField != i:
            listOut1.append(i)
            if listIn2: listOut2.append(j)
    if listIn2:
        return listOut1, listOut2
    else:
        return listOut1

def getCharacter(name, dbPath):
    if __name__ == "__main__":
        from Character import Character
        from sqhelper import basedatos
    else:
        from .Character import Character
        from .sqhelper import basedatos
    db        = basedatos(dbPath)
    character = Character(db, name)
    if not character.exists:
        return -1
    idFields = character.skillIds
    nameFields = character.finalList
    nameField = character.nameField
    dictOut = character.printEntityById()
    ids, skillNames = dropNameField(idFields, nameField, nameFields)
    return ids, skillNames, dictOut

def listFields():
    if __name__ == "__main__":
        from SkillSet import skillList, nameField, utf8dict
    else:
        from .SkillSet import skillList, nameField, utf8dict
    idList   = dropNameField(skillList, nameField)
    nameList = [utf8dict[idSk] for idSk in idList]
    return idList, nameList, nameField

def listCharacters(dbPath):
    if __name__ == "__main__":
        from sqhelper import basedatos
        from SkillSet import nameField, tableName
    else:
        from .sqhelper import basedatos
        from .SkillSet import nameField, tableName
    db         = basedatos(dbPath)
    characters = db.readTable(tableName, returnVal = nameField)
    return characters


def saveCharacter(name, dbPath, dictIn):
    if __name__ == "__main__":
        from Character import Character
        from sqhelper import basedatos
    else:
        from .Character import Character
        from .sqhelper import basedatos
    db        = basedatos(dbPath)
    character = Character(db, name)
    if character.exists:
        return -1
    character.saveNewEntityById(dictIn)
    return 0

def modifyCharacter(name, dbPath, dictIn):
    if __name__ == "__main__":
        from Character import Character
        from sqhelper import basedatos
    else:
        from .Character import Character
        from .sqhelper import basedatos
    db        = basedatos(dbPath)
    character = Character(db, name)
    character.modifyEntireEntity(dictIn)


if __name__ == "__main__":
    a, b, c = getCharacter("TestingChar", "Relgan.dat")
    print(a)
    print(b)
    print(c)
    listTo, names, namef = listFields() # working with ids here
    dictIn = {}
    j = 2
    for skill in listTo:
        dictIn[skill] = str(j)
        j += 1
#     saveCharacter("Pepit3", "Relgan.dat", dictIn)
    a, b, c = getCharacter("Pepit3", "Relgan.dat")
    print(a)
    print(b)
    print(c)
    print("And now modify the entire entity just to get value 5 into JAJAJAJABIEN")
    dictIn[listTo[4]] = "JAJAJAJAJABIEN"
    modifyCharacter("Pepit3", "Relgan.dat", dictIn)
    a, b, c = getCharacter("Pepit3", "Relgan.dat")
    print(a)
    print(b)
    print(c)



    

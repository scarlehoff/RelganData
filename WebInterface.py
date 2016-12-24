# This is just a few wrappers to be called by the web server
# -*- coding: utf-8 -*-

def dropNameField(listIn, nameField):
    listOut = []  
    for i in listIn:
        if nameField != i: listOut.append(i)
    return listOut

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
    allFields = character.finalList
    nameField = character.nameField
    dictOut   = character.printEntity()
    outFields = dropNameField(allFields, nameField)
    return outFields, nameField, dictOut

def listFields():
    if __name__ == "__main__":
        from SkillSet import skillList, nameField, utf8dict
    else:
        from .SkillSet import skillList, nameField, utf8dict
    idList   = dropNameField(skillList, nameField)
    nameList = [utf8dict[idSk] for idSk in idList]
    return idList, nameList, nameField

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



    

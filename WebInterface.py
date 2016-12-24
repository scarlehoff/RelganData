# This is just a few wrappers to be called by the web server

def dropNameField(listIn, nameField):
    listOut = []  
    for i in listIn:
        if nameField != i: listOut.append(i)
    return listOut

def getCharacter(name, dbPath):
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
    from .SkillSet import statList, skillList, nameField
    finalList = dropNameField(statList + skillList, nameField)
    return finalList, nameField

def saveCharacter(name, dbPath, dictIn):
    from .Character import Character
    from .sqhelper import basedatos
    db        = basedatos(dbPath)
    character = Character(db, name)
    if character.exists:
        return -1
    character.saveNewEntity(dictIn)
    return 0


if __name__ == "__main__":
    a, b, c = getCharacter("TestingChar", "Relgan.dat")
    print(a)
    print(b)
    print(c)
    listTo, namef = listFields()
    dictIn = {}
    j = 2
    for skill in listTo:
        dictIn[skill] = str(j)
        j += 1
    dictIn[namef] = "Pepito"
    saveCharacter("Pepito", "Relgan.dat", dictIn)
    a, b, c = getCharacter("Pepito", "Relgan.dat")
    print(a)
    print(b)
    print(c)


    

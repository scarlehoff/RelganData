import sqlite3 as dbapi

class basedatos:
    def __init__(self, database):
        self.name = database
        self.db   = dbapi.connect(database)

    def executeAndCommitDB(self,stringRaw,options = None):
        c = self.db.cursor()
        string = stringRaw.lower()
        if options:
            c.execute(string,options)
        else:
            c.execute(string)
        c.close()
        self.db.commit()

    def createTableText(self, campos, nombre):
        # Creates a table of name "nombre"
        # and campos "campos" (all of them being text)
        # into database self.db
        head = "create table " + nombre
        tail = ' (id INTEGER PRIMARY KEY, '
        for i in campos:
            tipo = " text, "
            tail += i + tipo
        if tail[-2] == ',': tail = tail[:-2]
        tail += ') '
        self.executeAndCommitDB(head+tail)
        print("Table " + nombre + " has been created.")


    def insertDataInTable(self, dataList, table):
        head = "insert into " + table + "("
        campos = self.listOfFields(table)
        for i in campos:
            head = head + i + ","
        if head[-1] == ',': head = head[:-1]
        head = head + ")" + " values "
        tail = '('
        # todo: check that len(fields) = len(data)
        for i in dataList:
            tail += "?,"
        if tail[-1] == ',': tail = tail[:-1]
        tail += ')'
        self.executeAndCommitDB(head+tail,dataList)
        print("Data inserted at " + table)

    def readTable(self, table, field=None, value=None, returnVal='*'):
        cadena = "select " + returnVal + " from " + table
        c = self.db.cursor()
        if type(field) == type([1,2]):
            cadena += " where"
            for i,j in zip(field, value):
                cadena += " " + i
                cadena += " like '%" + j + "%'"
                cadena += " AND"
            cadena = cadena[:-4]
        else:
            if field and value:
                cadena += " where " + field 
                cadena += " like '%" + value + "%'"
        c.execute(cadena)
        dataList = []
        for i in c: dataList.append(i)
        c.close()
        return dataList

    def modifyRecord(self, table, fieldName, newValue, idField, idValue):
        cadena  = "UPDATE " + table + " SET " + fieldName + " = ? WHERE "
        cadena += idField + " = ?"
        tupla   = (newValue, idValue)
        self.executeAndCommitDB(cadena, tupla)
        print("Data modified for " + idValue)

    def modifyRecordMany(self, table, fieldNames, newValues, idField, idValue):
        cadena  = "UPDATE " + table + " SET "
        for fieldName in fieldNames:
            cadena += fieldName + " = ?, "
        cadena  = cadena[:-2]
        cadena += " WHERE " + idField + " = ?"
        lista   = newValues + [idValue]
        self.executeAndCommitDB(cadena, lista)
        print("Data modified for " + idValue)

#     def modifyRecord(self, tabla):
#          # Modify a record of the table tabla
#         d = self.readTable(tabla)
#         for i in d: print i
#         print "Select record id"
#         idr = protectedInput(" > id of the field: ")
#         print "Which field do you want to modify?"
#         campos = self.listOfFields(tabla)
#         print "Fields:"
#         for i in campos: print i
#         fieldr = protectedInput(" > name of the field: ")
#         cad = "UPDATE " + tabla + " SET " + fieldr + " = ? WHERE id = ?"
#         print "Introduce the new value for this field:"
#         newvl = protectedInput(" > new value: ")
#         tupla = (newvl, idr)
#         self.executeAndCommitDB(cad,tupla)
#         return 0

    def listOfTables(self, filt = None):
        # Return list of tables in self.db
        # (that are called filt+something)
        c = self.db.cursor()
        cadena = "select * from sqlite_master WHERE type='table';"
        c.execute(cadena)
        listOfTables = []
        for j in c:
            tabname = j[1]
            if filt:
                if tabname.startswith(filt):
                    listOfTables.append(tabname)
            else:
                listOfTables.append(tabname)
        c.close()
        return listOfTables

    def listOfFields(self, tabla):
        # Return a list of fields in table tabla
        listOfFields = []
        c = self.db.cursor()
        cadena = "PRAGMA table_info(" + tabla + ")"
#        cadena = "SELECT name FROM sqlite_master WHERE type='table';"
#        cadena = "SELECT * FROM " + tabla + " LIMIT 1;"
        listOfFieds = []
        c.execute(cadena)
        for i in c:
            if i[1] != u"id": listOfFields.append(i[1])
        c.close()
        return listOfFields

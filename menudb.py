import json
import os
import general


defaultMenuCurrency = "PLN"
defaultMenuName = "MENU"
draftMenuDB = [{ "menuName": defaultMenuName, "menuCurrency": defaultMenuCurrency, "dishList" : []}]
locationMenuDB = 'menudb.minify.db'



class MenuDB:
    def __init__(self):
        self.setLocation(locationMenuDB)
        self.loadSpecificMenuDB()


    def setLocation(self, location):
        self.location = os.path.expanduser(location)


    def loadSpecificMenuDB(self, menuName = 'Menu Swojskie'):
        newDB = [db  for db in general.loadDB(locationMenuDB)  if db['menuName'] == menuName][0]
        self.db = newDB  if newDB  else draftMenuDB


    def dumpFullMenuDB(self):
        general.dumpDB(self.db, self.location)


    def dumpMenuDB(self):
        general.dumpPartOfDB(self.db, self.location, 'menuName')


    def getMenuName(self):
        return self.db.get('menuName')


    def getMenuCurrency(self):
        return self.db.get('menuCurrency')


    def getMenuRecord(self, key, value):
        try:
            result = [  record
                        for record in self.db['dishList']
                            if record[key] == value ]
            return result
        except:
            return False


    def getAllMenuRecords(self):
        return self.db.get('dishList')


    def correctAllMenuRecordsPosition(self):
        for i, record in enumerate(self.db['dishList']):
            properPosition = i+1
            if record['position'] != properPosition:
                self.db['dishList'][i]['position'] = properPosition


    def addMenuRecord(self, obj):
        try:
            obj = json.loads(obj)
            result = [  record
                        for record in self.db['dishList']
                            if record.dish['dishName'] == obj.dish['dishName'] ]
            
            #general.printInformation('', result)

            if len(result) > 0:
                raise Exception('Record already exist')
            else:
                self.db['dishList'].append(obj)
                self.dumpMenuDB()
                general.alertAdded('nową pozycję do menu')
                return True
        except:
            general.alertProblemOccured('dodaniem rekordu: nowa pozycja w menu')
            return False


    def editMenuRecord(self, obj):
        try:
            obj = json.loads(obj)
            position = obj['position']
            index = [ i
                        for i, record in enumerate(self.db['dishList'])
                        if record['position'] == position ][0]
            
            if index != None:
                self.db['dishList'][index] = obj
                self.dumpMenuDB()
                general.alertEdited('pozycję nr ' + str(position) + ' w menu')
                return True
            else:
                raise Exception('Record to edit does not exist')
        except:
            general.alertProblemOccured('edycją rekordu: pozycja nr ' + str(position) + ' w menu')
            #general.alertDoneNothing(msg)
            return False #'Record does not exist yet'


    def deleteMenuRecord(self, i):
        try:
            if i >= 0:
                del self.db['dishList'][i]
                self.correctAllMenuRecordsPosition()
                self.dumpMenuDB()
                position = i+1
                general.alertDeleted('pozycję nr ' + str(position) + ' w menu')
                return True
            else:
                raise Exception('Record index does not exist')
        except:
            general.alertProblemOccured('usunięciem rekordu: pozycja numer ' + str(position) + ' w menu')
            return False
        



menuDBController = MenuDB()
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
            
        except:
            return False
        
        finally:
            self.db['dishList'].append(obj)
            self.dumpMenuDB()
            return True


    def editMenuRecord(self, obj):
        try:
            obj = json.loads(obj)

            for i, record in enumerate(self.db['dishList']):

                if record['position'] == obj['position']:
                    self.db['dishList'][i] = obj
                    self.dumpMenuDB()
                    return True

        except:
            return 'Record does not exist yet'


    def deleteMenuRecord(self, i):
        try:
            del self.db['dishList'][i]
            self.correctAllMenuRecordsPosition()
            self.dumpMenuDB()
            return True
        except:
            return False
        



menuDBController = MenuDB()
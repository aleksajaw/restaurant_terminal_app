import json
import os
import general


class OrdersDB:
    def __init__(self):
        self.location = os.path.expanduser('ordersdb.minify.db')
        self.loadOrdersDB(self.location)


    def loadOrdersDB(self, location):
        newDB = general.loadDB(location)
        self.db = newDB if newDB else []


    def dumpOrdersDB(self):
        try:
            general.dumpDB(self.db, self.location)
            return True
        except:
            return False


    def getOrdersRecord(self, key, value):
        try:
            result = [record  for record in self.db  if record[key] == value]
            return result
        except:
            return False


    def getAllOrdersRecords(self):
        return self.db


    def addOrdersRecord(self, obj):
        try:
            obj = json.loads(obj)
            id = obj['orderID']
            result = [ record
                            for record in self.db
                            if record['orderID'] == id ]
            if not len(result):
                self.db.append(obj)
                self.dumpOrdersDB()
                general.alertAdded('nowe zamówienie')
                return True
            else:
                raise Exception('Record already exists')
        except:
            general.alertProblemOccured('dodaniem rekordu zamówienia')
            return False


    def deleteOrdersRecord(self, id):
        try:
            index = [ i
                        for i, record in enumerate(self.db)
                            if record['orderID'] == id ][0]
            if index != None:
                del self.db[index]
                self.dumpOrdersDB()
                general.alertDeleted('zamówienie nr ' + str(id))
                return True
            else:
                raise Exception('Record does not exist')
        except:
            general.alertProblemOccured('usunięciem rekordu: zamówienie nr ' + str(id))
            return False




ordersDBController = OrdersDB()
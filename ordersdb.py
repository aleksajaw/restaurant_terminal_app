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
            result = [record  for record in self.db  if record['date'] == obj['date']]
            if len(result) == 0:
                raise Exception('Record does not exist yet')
        except:
            return False
        
        finally:
            self.db.append(obj)
            self.dumpOrdersDB()
            return True


    def deleteOrdersRecord(self, id):
        try:
            result = [  i
                        for i, record in enumerate(self.db)
                            if record['orderId'] == id ]
            #print(str(result))
            return result
        except:
            return False
        #try:
        #    obj = json.loads(obj)
        #    i = self.db.index(obj)
        #    del self.db[i]
        #    self.dumpDB()
        #    return True
        #except:
        #    return False




ordersDBController = OrdersDB()
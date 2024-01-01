import os
import general


draftServicesDB = { 'startServices' : {}, 'mainServices': {}, 'menuServices': {}, 'ordersServices': {}}
locationServicesDB = 'servicesdb'



class ServicesDB:
    def __init__(self):
        self.location = os.path.expanduser(locationServicesDB)
        self.db = {}
        self.loadServicesDB(self.location)


    def loadServicesDB(self, location):
        newDB = general.loadDB(location)
        self.db = newDB  if newDB  else draftServicesDB


    def dumpServicesDB(self):
        try:
            general.dumpDB(self.db , self.location)
            return True
        except:
            return False


    def getServicesByName(self, name):
        return self.db.get( name + 'Services')


    def getAllServices(self):
        return self.db
    



servicesDBController = ServicesDB()
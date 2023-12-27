import json
import os
import general


draftUsersDB = [{ "login": "guest", "password": "", "hasPassword": False }]



class UsersDB:
    def __init__(self):
        self.location = os.path.expanduser('usersdb.db')
        self.loadUsersDB(self.location)


    def loadUsersDB(self, location):
        newDB = general.loadDB(location)
        self.db = newDB  if newDB  else draftUsersDB


    def doesUsersRecordExist(self, login):
        checkingResult = bool( self.getUsersRecord(login) )
        return checkingResult


    def getUsersRecord(self, login):
        result = general.getDBRecordByKeyValue(self.db, 'login', login, 'użytkownika')
        return result


    def checkUsersRecordKeyValue(self, login, key, value):
        userRecord =  self.getUsersRecord(login)
        result = None
        try:
            result = (userRecord[key] == value)
        except:
            general.alertMain('atrybutem użytkownika')
        finally:
            return result


    def getUsersRecordKeyValue(self, login, key):
        userRecord = self.getUsersRecord(login)
        result = None
        try:
            result = userRecord[key]
        except:
            general.alertMain('atrybutem użytkownika')
        finally:
            return result
        



usersDBController = UsersDB()
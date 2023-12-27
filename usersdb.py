import json
import os
import general


class UsersDB:
    def __init__(self):
        self.location = os.path.expanduser('usersdb.db')
        self.loadUsersDB(self.location)


    def loadUsersDB(self, location):
        draftUserDB = [{ "login": "guest", "password": "", "hasPassword": False }]
        if os.path.exists(location):
            try:
                self.db = json.load(open(self.location, 'r', encoding="utf-8"))
            except:
                self.db = draftUserDB
        else:
            self.db = draftUserDB
        return True


    def doesUsersRecordExist(self, login):
        checkingResult = self.getUserRecord(login) != None
        if not checkingResult: general.printInformation('', 'Może chcesz się zalogować jako gość? Wpisz "guest"')
        return checkingResult


    def getUsersRecord(self, login):
        result = None
        try:
            result = [record  for record in self.db  if record['login'] == login][0]
        except:
            general.alertProblemExist('rekordem użytkownika')
        finally:
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
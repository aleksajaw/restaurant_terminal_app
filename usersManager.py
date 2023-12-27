from usersdb import usersDBController
import json
import general



class Users:
    def __init__ (self):
        self.isAnyUserLogged = False
        self.isLoggedAsAdmin = False
    

    def setIsAnyUserLogged(self, value):
        self.isAnyUserLogged = value

    def setIsLoggedAsAdmin(self, value):
        self.isLoggedAsAdmin = value

    def logInUser(self, login, password):
        if usersDBController.checkUsersRecordKeyValue(login, 'password', password):
            self.setIsAnyUserLogged(True)
            self.setIsLoggedAsAdmin(self.hasAdminPermissions(login) )

        elif self.isAnyUserLogged:
            self.logOutUser()
            
        return self.isAnyUserLogged


    def logOutUser(self):
        self.setIsAnyUserLogged(False)
        self.setIsLoggedAsAdmin( False )


    def doesUserExist(self, userName):
        return usersDBController.doesUsersRecordExist(userName)


    def hasAdminPermissions(self, login):
        return usersDBController.getUsersRecordKeyValue(login, 'isAdmin')


    def doesUserHavePassword(self, login):
        return usersDBController.getUsersRecordKeyValue(login, 'hasPassword')


usersController = Users()
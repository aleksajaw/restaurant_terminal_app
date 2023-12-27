 
import general
from usersManager import usersController
import getpass



def inputCorrectLogin():
    attempt = 0
    correctLogin = ''

    while not correctLogin:
        attempt+1
        inputLogin = general.getStringInputValueWithValidation('Login')

        if usersController.doesUserExist(inputLogin):
            correctLogin = inputLogin
            break
        else:
            general.printInformation('', 'Może chcesz się zalogować jako gość? Wpisz "guest"')

    return correctLogin



def inputCorrectPassword(user):
    attempt = 0
    correctPass = False

    ### logging attempt counter ###
    while attempt < 3 and not correctPass:
        inputPassword = getpass.getpass('Hasło: ')

        if usersController.logInUser(user, inputPassword):
            correctPass = True
            break

        elif inputPassword == '':
            general.alertNoCommand('hasło')

        else:
            attempt+=1
            general.alertWrongPassword('\nNieudane próby logowania: ' + str(attempt))

    return correctPass



def getPermissions():
    if usersController.isAnyUserLogged:
        usersController.logOutUser()
    
    isUserLogged = False

    while not isUserLogged:
        userLogin = inputCorrectLogin()

        if userLogin:

            isUserLogged = (not usersController.doesUserHavePassword(userLogin))  or  inputCorrectPassword(userLogin)

            if isUserLogged:
                msg = 'ZALOGOWANO.'

            else:

                # after 3 unsuccessful logging attempts as the selected user
                # log as guest
                general.alertYouCannotGet('uprawnień wybranego użytkownika')
                msg = 'zalogowano jako gość' 

            general.printInformation(msg)
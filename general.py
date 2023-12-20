import json
import os
import sys
import stepsManager
import random


###   G L O B A L   V A R I A B L E S   ###

booleanValues = {
                    'trueValues': ('true', 't', 'tak', 'y', 'yes'),
                    'falseValues': ('false', 'f', 'n', 'no', 'nie')
                }

stepLine = '--------------------------------------------------------'

weightUnits = [ {
                  'name' : 'g',
                  'target' : 'dish'
                },
                {
                  'name' : 'ml',
                  'target' : 'drink'
                } ]




###   P R I N T S   ###

def printInformation(textTitle = '', baseText = '', partOfText = '', hasLine = False):
    global stepLine
    information = ( '\n' + stepLine )  if hasLine  else ''
    information += ('\n' + textTitle + '\n')  if textTitle  else ''
    information += str(baseText)
    if partOfText:
        information += ' ' + partOfText + '.'
    if baseText: information += '\n'
    print(information)




###   R E M I N D E R S   /   D E F A U L T   M E S S A G E S   ###

def getReminder( reminder ):
    return convertReminder(reminder)

def printReminder( reminder ):
    printInformation('', reminder)



def getExitAppReminder():
    global exitAppReminder
    getReminder(exitAppReminder)

exitAppReminder = { 'name' : 'exit',
                    'description' : 'zamknąć aplikację',
                    'fnLocation' : 'general',
                    'fnName' : 'closeApp()',
                    'resetStepPossibility' : 'True' }

def printExitAppReminder():
    global exitAppReminder
    printReminder(getExitAppReminder())



def getBackOffReminder():
    global backOffReminder
    getReminder(backOffReminder)

backOffReminder = { 'name' : 'back',
                    'description' : 'wrócić do poprzedniego kroku',
                    'fnLocation' : '',
                    'fnName' : 'loadAppStep(-1, False)',
                    'resetStepPossibility' : 'True' }

def printBackOffReminder():
    global backOffReminder
    printReminder(getBackOffReminder())



stepBackReminders = [backOffReminder, exitAppReminder]
stepBackNames = [reminder['name'] for reminder in stepBackReminders]



def filterStepBackReminders(canGoBack = True):
    global stepBackReminders
    global filteredStepBackReminders

    filteredStepBackReminders = []
    filteredStepBackNames = []

    for reminder in stepBackReminders:
        isFilterBackInUse = canGoBack  or  (not canGoBack and reminder['name'] != 'back')
        
        if isFilterBackInUse:
            filteredStepBackReminders.append(reminder)
            filteredStepBackNames.append(reminder['name'])



def getFilteredStepBackReminders():
    global filteredStepBackReminders
    return getStepReminders(filteredStepBackReminders, 'Polecenia powrotu')

filteredStepBackReminders = stepBackReminders
filteredStepBackNames = [ reminder['name'] for reminder in filteredStepBackReminders ]

def printFilteredStepBackReminders():
    global filteredStepBackReminders
    printInformation('', getFilteredStepBackReminders())


defaultReminders = filteredStepBackReminders



def getStepReminders(reminders = [], remindersTitle = 'Wpisz jedno z poleceń' ):
    global defaultReminders, stepLine
    if not len(reminders):
        reminders = defaultReminders
    msg = ''
    msg += stepLine
    msg += '\n' + remindersTitle + ':'
    msg += getConvertedReminders(reminders)
    msg += '\n'
    return msg

def printStepReminders():
    printInformation('', getStepReminders())



def getConvertedReminders(reminders = []):
    msg = ''
    for i, reminder in enumerate(reminders):
        msg += '\n-->' + convertReminder(reminder)
        #if i < len(reminders)-1:
        msg += ';'
    #msg += '\n'
    return msg


def convertReminder(reminder):
    #return '  -  aby '.join( f'{v}' for v in reminder.values() )
    return reminder['name'] + '  -  aby ' + reminder['description']



def getWelcomeMessage():
    global welcomeMessage
    msg = welcomeMessage
    #msg += getStepReminders( [ exitAppReminder ])
    return msg

welcomeMessage = '\n\nWitaj!'

def printWelcomeMessage():
    printInformation('', getWelcomeMessage())




###   A L E R T S   ###

def alertMain(baseText='', partOfText = '', hasTitle = True):
    msg = ''
    if hasTitle: alertTitle = '!UWAGA!'
    msg += baseText
    printInformation('', (alertTitle + ' ' + baseText), partOfText)


def alertUnknownCommand():
    alertMain('Nieznane polecenie. Spróbuj ponownie.')


def alertNoCommand(command = 'polecenie'):
    alertMain('Wpisz', command)


def alertDeletion(element):
    alertMain('Usunięto', element)


def alertAddition(element):
    alertMain('Dodano', element)


def alertEdition(element):
    alertMain('Edytowano', element)


def alertDoneNothing(element):
    alertMain('Nie wykonano żadnej czynności związanej z:', element)


def alertNoElements(elements):
    alertMain('Brak', elements)


def alertNoExist(element):
    alertMain('Nie istnieje',  element)


def alertYouCannot(command):
    alertMain('Nie możesz', command)


def alertYouCannotGet(command):
    alertYouCannot('uzyskać ' + command)


def alertProblemExist(partOfText=''):
    baseText = 'Wystąpił problem'
    if partOfText: partOfText = 'z ' + partOfText
    alertMain(baseText, partOfText)


def alertWrongPassword(partOfText = ''):
    alertMain('Niepoprawne hasło.', partOfText)




###   A S K   F O R   A   C O M M A N D   ###

def askForCommand(command):
    printInformation('', 'Podaj', command)


def askForValue(command = 'wartość'):
    printInformation('', 'Podaj', command)




###   V A L U E   C H E C K I N G   ###

def isElementValueDefault(el, defaultValue=''):
    return el in [defaultValue, None, '']


def isNumber(str):
    try:
        str = correctNrNotation(str)
        convertedStr = float(str)
        return True
    except ValueError:
        return False




###   V A L U E   C O N V E R S I O N   ###

def convertNumberType(nr, nrType = 'int', roundLimit = 2):
    nrValue = nr
    if nrValue:
        try:
            if isinstance(nrValue, str):
                nrValue = correctNrNotation(nrValue)
            nrValue = round(float(nrValue), roundLimit)
            if nrType == 'int':
                nrValue = int(nrValue)

            #printInformation( ( 'Konwersja wartości %s: z %s na %d %s.' % (nr, type(nr), nrValue, type(nrValue) ) ) )
        finally:
            return nrValue


def correctNrNotation(val):
    val = removeSpaces(str(val)).replace(',', '.')
    return val


def removeSpaces(val):
    return val.replace(' ','')


def getSpecificKeyValuesFrom(elList = [], keyName = 'name'):
    return ( [ el.get(keyName)  for el in elList ]
                if len(elList)
                else None )


def convertToDict(el):
    newEl = getDict(el)
    for key in newEl.keys():
        try:
            convertedValue = json.dumps( newEl[key] )
        except:
            newEl[key] = getDict(newEl[key])

    return newEl


def getDict(el):
    try:
        return el.__dict__
    except:
        return el
    

def printDict(el):
    printInformation('', getDict(el))



###   I N P U T   V A L I D A T I O N   ###

def getNumberInputValueWithValidation(partOfText = '', nrType = 'int', defaultValue = 0, roundLimit = 2, noLessThan = 0.01, noMoreThan = None):
    from stepsManager import stepBack
    inputCommandText = 'Podaj'
    if partOfText != '': inputCommandText += ' ' + partOfText
    inputCommandText += ': '

    inputValue = defaultValue

    while isElementValueDefault(inputValue, defaultValue):

        inputValue = removeSpaces(input(inputCommandText))
        
        if inputValue in stepBackNames:
            stepBack(inputValue, True)
        
        if not len(inputValue):
            alertNoCommand()

        elif not isNumber(inputValue):
            alertYouCannot('podać takiej wartości')
            inputValue = None

        else:
            convertedValue = convertNumberType(inputValue, nrType, roundLimit)

            if convertedValue < noLessThan:
                alertYouCannot('podać liczby mniejszej od ' + str(noLessThan))
                inputValue = None

            elif noMoreThan != None and convertedValue > noMoreThan:
                alertYouCannot('podać liczby większej niż ' + str(noMoreThan))
                inputValue = None

    return convertedValue


def getStringBooleanValueWithValidation(baseText = '', keyName = '', defaultValue = None):
    from stepsManager import stepBack
    global booleanValues
    sentenceMark = '?'

    inputCommandText = ( baseText
                            if baseText != ''
                            else 'Czy' + sentenceMark ) + ' (t/n) '
    inputAlertText = 'podać liczby jako wartość'
    
    if keyName != '':
        inputAlertText += ' ' + keyName

    inputValue = defaultValue

    while True:
        inputValue = removeSpaces(input(inputCommandText))
        
        if inputValue in stepBackNames:
            stepBack(inputValue)

        if isNumber(inputValue):
           alertYouCannot(inputAlertText)
           inputValue = ''

        else:
            return inputValue in (booleanValues['trueValues'])  and  inputValue not in (booleanValues['falseValues'])


def getStringInputValueWithValidation(baseText = '', partOfText = '', availableValues = [], defaultValue = None):
    from stepsManager import stepBack
    sentenceMark = ': '
    baseText = baseText or 'Podaj'
    if partOfText: partOfText = ' ' + partOfText
    inputCommandText = baseText + partOfText + sentenceMark

    inputValue = defaultValue

    while isElementValueDefault(inputValue, defaultValue):
        inputValue = input(inputCommandText)

        if inputValue in stepBackNames:
            stepBack(inputValue)

        cannotInput = ( ( len(availableValues)  and  inputValue not in availableValues )
                            or isNumber(inputValue) )

        if cannotInput:
            alertYouCannot('podać takiej wartości')
            inputValue = ''

    return inputValue




###   J S O N   F U N C T I O N S   ###

def getJSON(el):
    el = convertToDict(el)
    return json.dumps(el)


def isJSONserializable(el):
    try:
        json.dumps(el)
        return True
    except (TypeError, OverflowError):
        return False


#def getJSONforNestedDict(el):
#    if isJSONserializable(el):

#    else:




###   D A T A B A S E   M A N A G E R   B A S I C S   ###

def loadDB(location):
    db = []
    if os.path.exists(location):
        try:
            db = json.load(open(location, 'r', encoding="utf-8"))
            #print(db)
        except json.decoder.JSONDecodeError:
            printInformation('', 'String could not be converted to JSON.')
    return db


def dumpDB(db, location):
    try:
        json.dump(db, open(location, 'w+', encoding="utf-8"))
        return True
    except:
        return False


def dumpPartOfDB(partOfDB, location, dbKey):
    try:
        oldDB = loadDB(location)
        dbIndexToChange = [i  for i, db in enumerate(loadDB(location))  if db[dbKey] == partOfDB[dbKey]][0]
        oldDB[dbIndexToChange] = partOfDB
        dumpDB(oldDB, location)
        return True
    except:
        print('error')
        return False


def generateRandomID(dbElements = [], idKey = 'id'):
    isIDInUse = True
    while isIDInUse:
        availableID = random.randint(111111, 999999)
        isIDInUse = bool (len([i  for i, el in enumerate(dbElements)  if el[idKey] == availableID]))

    return availableID



###   D E F A U L T   A P P   M A N A G E R   ###
def closeApp():
    sys.exit()
import json
import os
import sys
import stepsManager
import random


# Following functions and variables were created to achieve greater coherence and order in code.



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

# "Reminders" are things which should be attached to each step.

def getReminder( reminder ):
    return convertReminder(reminder)

def printReminder( reminder ):
    printInformation('', reminder)



def getExitAppReminder():
    global exitAppReminder
    getReminder(exitAppReminder)

### 'name' property of every single reminder is a word, which should be typing to call the appropriate command
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

def convertNumberType(nr, desiredType = 'int', roundLimit = 2):
    nrValue = nr
    if nrValue:
        try:
            if isinstance(nrValue, str):
                nrValue = correctNrNotation(nrValue)

            nrValue = round(float(nrValue), roundLimit)

            if desiredType == 'int':
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

def getNumberInputValueWithValidation(baseText = '', partOfText = '', desiredType = 'int', defaultValue = 0, roundLimit = 2, noLessThan = 0.01, noMoreThan = None):
        # BEGINNING of the universal part #

    ### variables correction & declaration ###
    baseText = baseText or 'Podaj'
    sentenceMark = ':'

    ###
    if partOfText:
        partOfText = ' ' + partOfText

    ###
    inputCommandText = baseText + partOfText + sentenceMark + ' '

    ### set initial value ###
    inputValue = defaultValue

        # END of an universal part #

    while isElementValueDefault(inputValue, defaultValue):

        inputValue = removeSpaces(input(inputCommandText))
        
        if inputValue in stepBackNames:
            stepsManager.stepBack(inputValue, True)
        
        elif not len(inputValue):
            alertNoCommand()

        elif not isNumber(inputValue):
            alertYouCannot('podać takiej wartości')
            inputValue = None

        else:
            convertedValue = convertNumberType(inputValue, desiredType, roundLimit)

            if convertedValue < noLessThan:
                alertYouCannot('podać liczby mniejszej od ' + str(noLessThan))
                inputValue = None

            elif noMoreThan != None and convertedValue > noMoreThan:
                alertYouCannot('podać liczby większej niż ' + str(noMoreThan))
                inputValue = None

    return convertedValue


def getStringBooleanValueWithValidation(introductoryText = '', baseText = '', partOfText = '', keyName = '', defaultValue = None):
    global booleanValues

        # BEGINNING of the universal part #

    ### variables correction & declaration ###
    baseText = baseText or 'Czy'
    sentenceMark = '?'

    ###
    if partOfText:
        partOfText = ' ' + partOfText 
    
    ###
    inputCommandText = baseText + partOfText + sentenceMark + ' (t/n) '

    ###
    inputAlertText = 'podać liczby jako wartość'
    if keyName:
        inputAlertText += ' ' + keyName

    ### set initial value ###
    inputValue = defaultValue

        # END of the universal part #


    ### A loop without any special condtions
    ### just waits for an action called inside
    while True:
        
        if introductoryText:
            print(introductoryText)
    
        inputValue = removeSpaces(input(inputCommandText))
        
        if inputValue in stepBackNames:
            stepsManager.stepBack(inputValue)

        elif isNumber(inputValue):
           alertYouCannot(inputAlertText)
           inputValue = ''

        else:
            isInputValueTrue = inputValue in (booleanValues['trueValues'])
            isInputValueFalse = inputValue in (booleanValues['falseValues'])

            return isInputValueTrue and not isInputValueFalse


def getStringInputValueWithValidation(baseText = '', partOfText = '', availableValues = [], defaultValue = None):
        ### BEGINNING of the universal part ###

    ### variables correction & declaration ###
    baseText = baseText or 'Podaj'
    sentenceMark = ': '

    ###
    if partOfText:
        partOfText = ' ' + partOfText

    ###
    inputCommandText = baseText + partOfText + sentenceMark

    ### set initial value ###
    inputValue = defaultValue

        ### END of the universal part ###


    while isElementValueDefault(inputValue, defaultValue):
        inputValue = input(inputCommandText)

        if inputValue in stepBackNames:
            stepsManager.stepBack(inputValue)

        isValuesLimitInUse = bool( len(availableValues) )
        cannotInput = ( ( isValuesLimitInUse  and  inputValue not in availableValues )
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


def getDBRecordByKeyValue(dbElements = [], keyName = '', desiredValue = None, alertText = ''):
    try:
        result = [  record
                    for record in dbElements
                        if record[keyName] == desiredValue ][0]
        return result

    except:
        msg = 'rekordem'
        if alertText:
            msg = ' ' + alertText
        alertProblemExist(msg)
        return False


def checkIfDBRecordExist(dbElements = [], keyToCompare = 'id', baseOfExpectedValue = None, addKeyToBasement = True):
    if not '[' == keyToCompare[0]:
        keyToCompare = '.' + keyToCompare
    
    if addKeyToBasement:
        if keyToCompare  and  isinstance(baseOfExpectedValue, (object, dict)):
            baseOfExpectedValue = eval('baseOfExpectedValue' + keyToCompare)

    try:
        result = bool( len([ i  for i, record in enumerate(dbElements)
                                if eval('record' + keyToCompare) == baseOfExpectedValue ] ) )

        return result

    except:
        return False


def generateUniqueRandomID(dbElements = [], idKey = 'id'):
    isIDInUse = True

    while isIDInUse:
        generatedID = random.randint(111111, 999999)
        isIDInUse = checkIfDBRecordExist(dbElements, idKey, generatedID, False)

    return generatedID




###   D E F A U L T   A P P   M A N A G E R   ###
def closeApp():
    sys.exit()
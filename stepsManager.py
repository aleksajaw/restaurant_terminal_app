import general
import authorization
import general


mainChosenService = ''
currentServiceStep = 0



def changeMainChosenService(chosenService):
    global mainChosenService
    mainChosenService = chosenService


def inputStepService(filteredServices = [], servicesInnerController=''):
    servicesLen = len(filteredServices)
    nrLimit = ( servicesLen
                    if servicesLen
                    else None )
    
    isInputNumberType = bool(nrLimit)
    
    serviceInput = ( general.getNumberInputValueWithValidation('numer wybranego polecenia', 'int', '', 0, 1, nrLimit)
                        if isInputNumberType
                        else general.getStringInputValueWithValidation('Które polecenie wybierasz', '', general.filteredStepBackNames ) )

    isNumberInLimit = general.isNumber(serviceInput)  and  general.convertNumberType(serviceInput) <= nrLimit
        
    if servicesLen and isNumberInLimit:
        callChosenService(filteredServices, servicesInnerController, serviceInput)

    else:
        general.alertNoExist('opcja ' + serviceInput)
        inputStepService(filteredServices, servicesInnerController)


def callChosenService(filteredServices, servicesInnerController, serviceInput):
    from menuManager import menuController
    from ordersManager import ordersController
    from usersManager import usersController

    serviceIndex = int(serviceInput) - 1
    chosenService = filteredServices[serviceIndex]
    fnToCallName = servicesInnerController + chosenService['partOfFunction']
    fnToCallName += '()'  if '(' not in fnToCallName  else ''

    eval(fnToCallName)


def printStepBackService():    
    general.filterStepBackReminders(currentServiceStep > 0)
    general.printFilteredStepBackReminders()


def generateFullServicesStep(stepServices = [], doTakeStepForward = True):
    from servicesManager import servicesController
    filteredServices = stepServices
    innerController = ''

    if len(stepServices):
        filteredServices = servicesController.getFilteredServicesByPermissions(stepServices)
        servicesController.printFilteredServicesByPermissions()
        innerController = stepServices['innerController']
 
    printStepBackService()
    
    inputStepService(filteredServices, innerController)
    if doTakeStepForward: loadAppStep(+1, False)




###   S T E P S   M A N A G E R    B A S I C S   ###

def step3():
    stepTemplate('', False)


def step2():
    stepTemplate(mainChosenService)


def step1():
    stepTemplate('main')


def step0():
    general.printWelcomeMessage()
    stepTemplate()


def stepTemplate(servicesName = 'start', doTakeStepForward = True):
    from servicesManager import servicesController
    stepServices = ( servicesController.getServices(servicesName)
                        if servicesName
                        else [] )
    generateFullServicesStep( stepServices, doTakeStepForward )



def loadAppStep(nrValue, isStepNr = True):
    makeStepInApp(nrValue, isStepNr)
    eval('step' + str(currentServiceStep) + '()')


def makeStepInApp(nrValue, isStepNr = False):
    global currentServiceStep
    step = ( nrValue
                if isStepNr
                else currentServiceStep + nrValue )
    setCurrentServiceStep(step)


def setCurrentServiceStep(step):
    global currentServiceStep
    if step < 0: step = 0
    elif step > 3: step = 3
    currentServiceStep = step



def isItCurrentStepBackCommand(inputValue):
    try:
        result = general.filteredStepBackNames.index(inputValue)
        return result
    except:
        return -1


def stepBack(command, resetStep = False):
    index = ( isItCurrentStepBackCommand(command)
                if isinstance(command, str)
                else -1 )
    doStepBack = index >= 0
    if doStepBack:
        commandEl = general.filteredStepBackReminders[index]
        #if resetStep and commandEl['resetStepPossibility']:
        #    loadAppStep(0, False)
        #else:
        commandFn = ( commandEl['fnLocation'] + '.' 
                        if commandEl['fnLocation']
                        else '' )
        commandFn += commandEl['fnName']
        eval(commandFn)
    else:
        loadAppStep(0, False)
    return doStepBack
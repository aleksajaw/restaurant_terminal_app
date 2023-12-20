from menudb import menuDBController
import general


defaultWeightValue = 0
defaultWeightUnit = 'g'



class Price:
    def __init__(self, current = 0.0, standard = 0.0, isPromotion = False):
        self.setStandard(standard)
        self.setCurrent(current or standard)
        self.setIsPromotion(isPromotion)


    def setStandard(self, value = 0.0):
        self.standard = value


    def getStandard(self):
        return self.standard
    

    def setCurrent(self, value = 0.0):
        self.current = value


    def getCurrent(self):
        return self.current    


    def setIsPromotion(self, value = False):
        self.isPromotion = value


    def getIsPromotion(self):
        return self.isPromotion



class Dish:
    def __init__(self, dishName = '', weight = {}):
        self.setName(dishName)
        self.setWeight(weight)

        
    def createNew(self):
        self.inputName()
        self.inputWeightValue()
        self.inputWeightUnit()


    def inputName(self):
        name = general.getStringInputValueWithValidation('', 'nazwę dania')
        self.setName(name)
    

    def setName(self, value = ''):
        self.dishName = value.capitalize()


    def getName(self):
        return self.dishName
    

    def setWeight(self, value = {}):
        global defaultWeightValue, defaultWeightUnit

        if not hasattr(self, 'weight'):
            self.weight = {}

        value = ( { 'weightValue' : defaultWeightValue, 'unit' : defaultWeightUnit }
                    if value == {}
                    else value )

        weightValue = value['weightValue']
        unit = value['unit']
        self.setWeightValue(weightValue)
        self.setWeightUnit(unit)


    def inputWeightValue(self):
        inputValue = general.getNumberInputValueWithValidation('', 'wagę lub objętość w formie liczby całkowitej', 'int', 0, 0, 1)
        self.setWeightValue(inputValue)


    def setWeightValue(self, newValue):
        self.weight['weightValue'] = newValue


    def getWeightValue(self):
        return self.weight['weightValue']
    

    def inputWeightUnit(self):
        inputValue = general.getStringInputValueWithValidation('', 'jednostkę miary', general.getSpecificKeyValuesFrom(general.weightUnits))
        self.setWeightUnit(inputValue)


    def setWeightUnit(self, newValue):
        self.weight['unit'] = newValue


    def getWeightUnit(self):
        return self.weight['unit']


    def editAttrs(self):
        dishEditionObj = [  {
                                'name': 'dish name',
                                'getterFnName': 'getName()',
                                'editValue': 'Name()'
                            },
                            {
                                'name': 'weight value',
                                'getterFnName': 'getWeightValue()',
                                'editValue': 'WeightValue()'
                            },
                            {
                                'name': 'weight unit',
                                'getterFnName': 'getWeightUnit()',
                                'editValue': 'WeightUnit()'
                            } ]

        for item in dishEditionObj:

            itemValue = str(eval('self.' + item['getterFnName']))
            inputCommandText = 'Obecna wartość pola ' + item['name'] + ' to ' + itemValue + '. Czy chcesz ją zmienić? (t/n)'
            doChange = general.getStringBooleanValueWithValidation(inputCommandText)
            if doChange:
                eval('self.input' + item['editValue'])

        #general.printDict(self)


    def getFullInfo(self):
        #spaceForDescription = (len(self.dishName) + 3) * ' '
        fullInfo = self.dishName + ' (' + str(self.weight['weightValue']) + self.weight['unit'] + ')'
        return fullInfo
      


class MenuElement:
    def __init__ ( self, position = 0, dish = {}, price = {} ):
        self.setPosition(position)
        self.setDish(dish)
        self.setPrice(price)


    def setPosition(self, value):
        self.position = value


    def getPosition(self):
        return self.position
        
        
    def createNew(self):
        self.dish.createNew()
        self.inputPrice()


    def setDish(self, value):
        try:
            dishValue = Dish(**value)
        except:
            dishValue = Dish(value)
        self.dish = dishValue


    def getDish(self):
        return self.dish


    def inputPrice(self):
        inputValue = general.getNumberInputValueWithValidation('', 'cenę', 'float')
        elPrice = inputValue
        self.setPrice(elPrice)


    def setPrice(self, value = {}):
        try:
            priceValue = Price(**value)
        except:
            priceValue = Price(value)
        self.price = priceValue


    def getPrice(self):
        return self.price


    def getDishWithPrice(self):
        import copy
        #IMPORTANT
        newEl = copy.deepcopy(self)
        del newEl.position
        return newEl


    def editAttrs(self):
        menuElEditionKeys = [ {
                                'name': 'current price',
                                'getterFnName': 'price.getCurrent()',
                                'editValue': 'Price()'
                            } ]

        for item in menuElEditionKeys:

            itemValue = str(eval('self.' + item['getterFnName']))
            inputCommandText = 'Obecna wartość pola ' + item['name'] + ' to ' + itemValue + '. Czy chcesz ją zmienić? (t/n)'
            doChange = general.getStringBooleanValueWithValidation(inputCommandText)
            if doChange:
                eval('self.input' + item['editValue'])

        #general.printDict(self)


    def getFullInfo(self, currency = ''):
        position = str(self.position) + '.'
        dish = self.dish
        dishName = dish.getName()
        dishWeightWithUnit = '/' + str(dish.getWeightValue()) + dish.getWeightUnit() + '/'
        dishCurrentPrice = '%.2f' % self.price.getCurrent()

        menuElementInfoStr = position + dishName + dishWeightWithUnit + dishCurrentPrice
        lengthOfSpace = 50
        spaceForPrice = ( lengthOfSpace - (len(menuElementInfoStr) + 2) ) * '.'


        fullInfo = position + ' ' + dishName + ' ' + dishWeightWithUnit + spaceForPrice + dishCurrentPrice

        if currency:
            fullInfo += ' ' + currency
        
        #fullInfo += '\n' + (len(position) + 2 ) * ' ' + '/' + dishWeightWithUnit + '/'
        return fullInfo


    def printFullInfo(self, currency = ''):
        general.printInformation('', self.getFullInfo(currency))



class Menu:
    def __init__ (self):
        self.setName()
        self.setMenuCurrency()
        self.loadMenu()
    

    def loadMenu(self):
        self.menuCurrency = menuDBController.getMenuCurrency()
        self.menuName = menuDBController.getMenuName()
        self.dishList = []
        for menuElement in menuDBController.getAllMenuRecords():
            #general.printInformation('', menuElement)            
            try:
                menuElValue = MenuElement(**menuElement)
            except:
                menuElValue = MenuElement(menuElement)
            formattedMenuElement = menuElValue
            self.dishList.append(formattedMenuElement)
    

    def printMenu(self):
        menuCurrency = self.getMenuCurrency()
        msg = ''
        dishList = self.dishList
        for menuElement in dishList:
            msg += '\n' + menuElement.getFullInfo(menuCurrency)
        general.printInformation('- ' + self.menuName + ' -', msg, '', True)
        
        if not len(dishList):
            general.alertNoElements('pozycji w menu')
    

    def getMenuElement(self, i):
        i = int(i) - 1
        try:
            return self.dishList[i]
        except:
            return None


    def getMenuPositionNumber(self, partOfText = ''):
        inputCommandText = 'numer pozycji w menu'
        if partOfText:
            inputCommandText += ' ' + partOfText

        inputNrLimit = (len(self.dishList))
        inputValue = general.getNumberInputValueWithValidation('', inputCommandText, 'int', 0, 0, 1, inputNrLimit)
        #if inputValue:
        position = inputValue
        return position
        

    def getMenuElementsLength(self):
        return len(self.dishList)


    def setMenuCurrency(self, value = ''):
        self.menuCurrency = value


    def getMenuCurrency(self):
        return self.menuCurrency


    def setName(self, value = ''):
        self.menuName = value


    def getName(self, value = ''):
        self.menuName = value


    def deleteMenuElement(self):
        from stepsManager import makeStepInApp
        makeStepInApp(+1)
        
        self.printMenu()
        if len(self.dishList):
            position = self.getMenuPositionNumber('do usunięcia')
            menuDBController.deleteMenuRecord(position-1)
            self.loadMenu()
            general.alertDeletion('pozycję numer ' + str(position) + ' w menu')
            self.printMenu()
    
        else:
            general.alertYouCannot('dokonać usunięcia')


    def addMenuElement(self):
        from stepsManager import makeStepInApp
        makeStepInApp(+1)

        self.printMenu()
        newMenuElement = MenuElement()
        newMenuElement.createNew()
        newMenuElement.position = self.getMenuElementsLength()+1
        menuDBController.addMenuRecord(general.getJSON(newMenuElement))
        self.loadMenu()
        self.printMenu()
        #general.alertAddition('nową pozycję do menu')


    def editMenuElement(self):
        from stepsManager import makeStepInApp
        makeStepInApp(+1)

        self.printMenu()
        if len(self.dishList):
            position = self.getMenuPositionNumber('do edycji')
            menuElToEdit = self.getMenuElement(position)
            menuElBeforeEdit = menuElToEdit
            menuElToEdit.dish.editAttrs()
            menuElToEdit.editAttrs()

            if menuElBeforeEdit != menuElToEdit:
                menuElToSave = menuElToEdit
                menuElToSave = general.convertToDict(menuElToSave)
                try:
                    menuDBController.editMenuRecord(general.getJSON(menuElToSave))
                finally:
                    self.loadMenu()
                    msg = 'pozycję numer ' + str(position) + ' w menu'
                    general.alertEdition(msg)
            else:
                msg = 'pozycją numer ' + str(position) + ' w menu'
                general.alertDoneNothing(msg)
            self.printMenu()
        else:
            general.alertYouCannot('dokonać edycji')
        



menuController = Menu()
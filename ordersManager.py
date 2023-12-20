from ordersdb import ordersDBController
from menuManager import menuController
from datetime import datetime
import general
import menuManager


defaultCurrency = menuController.getMenuCurrency()


class OrderElement:
    def __init__(self, dish = {}, price = {}, amount = 1, totalElementPrice = 0.0):
        self.setDish(dish)
        self.setAmount(amount)
        self.setPrice(price)
        self.setTotalElementPrice(totalElementPrice or self.countTotalPrice())


    def setDish(self, value = {}):
        if not isinstance(value, menuManager.Dish):
            try:
                dishValue = menuManager.Dish(**value)
            except:
                dishValue = menuManager.Dish(value)
        else:
            dishValue = value
        self.dish = dishValue


    def setAmount(self, value = 0):
        self.amount = value


    def setPrice(self, value = {}):
        if not isinstance(value, menuManager.Price):
            try:
                priceValue = menuManager.Price(**value)
            except:
                priceValue = menuManager.Price(value)
        else:
            priceValue = value
        self.price = priceValue


    def getCurrentPrice(self):
        return self.price.getCurrent()


    def setTotalElementPrice(self, value = 0.0):
        self.totalElementPrice = value


    def getTotalElementPrice(self):
        return self.totalElementPrice


    def countTotalPrice(self):
        totalElementPrice = float(self.amount) * self.getCurrentPrice()
        return general.convertNumberType( totalElementPrice, 'float' )


    def getFullInfo(self):
        fullInfo = self.dish.getFullInfo()
        fullInfo += '  ' + str(self.getCurrentPrice()) + ' x ' + str(self.amount) + ' = ' + ('%.2f' % self.getTotalElementPrice())
        return fullInfo



class Order:
    def __init__ (self, orderID = None, dateTime = '', orderElements = [], totalPrice = 0.0, orderCurrency = defaultCurrency):
        self.setOrderID(orderID)
        self.setDateTime(dateTime)
        self.setOrderElements(orderElements)
        self.setTotalPrice(totalPrice or self.countTotalPrice())
        self.orderCurrency = orderCurrency


    def setOrderID(self, value):
        if not value:
            value = general.generateRandomID(ordersDBController.getAllOrdersRecords(), 'orderID')
        self.orderID = value


    def getOrderID(self):
        return self.orderID


    def setDateTime(self, value):
        if not value:
            value = datetime.now().strftime('%X %A %d %b %Y')
        self.dateTime = value


    def getDate(self):
        return self.dateTime

        
    def getTime(self):
        return self.dateTime
    


    def createNew(self):
        import copy
        continueOrdering = True
        orderAccepted = False
        orderList = ''
        i = 0
        while not orderAccepted:
            if i:
                menuController.printMenu()

            while continueOrdering:

                i = menuController.getMenuPositionNumber()
                #IMPORTANT
                menuEl = copy.deepcopy(menuController.getMenuElement(i))
                print(menuEl.getFullInfo())
                fullMenuEl = menuEl.getDishWithPrice()

                amount = general.getNumberInputValueWithValidation( 'ilość', 'int', 0, 0, 1)
                fullMenuEl.amount = amount

                fullMenuEl = OrderElement(**general.getDict(fullMenuEl))

                totalElPrice = fullMenuEl.getTotalElementPrice()
                orderList += menuEl.dish.getFullInfo() + ' ' + "%.2f" % menuEl.price.getCurrent() + ' x ' + str(amount) + ' = ' + str(totalElPrice)
                orderList += '\n'

                fullMenuEl = general.convertToDict(fullMenuEl)
                self.orderElements.append(fullMenuEl)
                self.setTotalPrice(self.countTotalPrice())
                
                orderingMsg = '\nZamówienie\n' + orderList + '\n' + self.getTotalPriceMsg()
                print(orderingMsg)

                continueOrdering = general.getStringBooleanValueWithValidation('Czy kontynuować zamawianie?')
                print()

            self.printFullInfo('Podsumowanie:')
            orderAccepted = general.getStringBooleanValueWithValidation('Czy zamówienie gotowe?')
            if not orderAccepted: continueOrdering = True
        


    def setOrderElements(self, elements = []):
        elementsList = []
        for element in elements:
            #print('to jest element: ' + str(element))
            if not isinstance(element, OrderElement):
                try:
                    elValue = OrderElement(**element)
                except:
                    elValue = OrderElement(element)
                element = elValue
            elementsList.append(element)
        self.orderElements = elementsList
        #if len(self.orderElements): print(self.orderElements[0].getFullInfo())


    def getOrderElements(self):
        return self.orderElements
    

    def setTotalPrice(self, value = 0.0):
        self.totalPrice = value


    def getTotalPrice(self):
        return self.totalPrice


    def getTotalPriceMsg(self):
        return 'Pełna kwota zamówienia: ' + str(self.getTotalPrice()) + ' ' + self.getOrderCurrency()


    def countTotalPrice(self):
        totalPrice = 0.0
        for element in self.orderElements:
            totalPrice += ( element['totalElementPrice']
                                if not isinstance(element, OrderElement)
                                else element.totalElementPrice )
        return general.convertNumberType(totalPrice, 'float')


    def getOrderCurrency(self):
        return self.orderCurrency


    def getFullInfo(self):
        fullInfo = '\n\nZamówienie nr ' + str(self.orderID) + '\n'
        for i, element in enumerate(self.orderElements):
            if not isinstance(element, OrderElement):
                try:
                    element = OrderElement(**element)
                except:
                    element = OrderElement(element)
            fullInfo += '\n' + str(i+1) + '. ' + element.getFullInfo()
        fullInfo += '\n\n' + self.getTotalPriceMsg()
        return fullInfo


    def printFullInfo(self, partOfText = ''):
        fullInfo = ''
        if partOfText: fullInfo += partOfText
        fullInfo = self.getFullInfo()
        general.printInformation(fullInfo)




class Orders:
    def __init__(self):
        self.list = []
        self.loadOrders()


    def loadOrders(self):
        self.list = []
        for order in ordersDBController.getAllOrdersRecords():
            try:
                orderValue = Order(**order)
            except:
                orderValue = Order(order)
            formattedOrder = orderValue
            self.list.append(formattedOrder)


    def printOrders(self):
        msg = ''
        for order in self.list:
            msg += '\n' + order.getFullInfo()
        general.printInformation('Zamówienia', msg, '', True)
        if not msg:
            general.alertNoElements('zamówień')

    
    def getOrderIdNumber(self, partOfText):
        inputCommandText = 'numer id zamówienia'
        if inputCommandText:
            inputCommandText += ' ' + partOfText

        inputValue = general.getNumberInputValueWithValidation( inputCommandText, 'int', '', 0, 1 )
        #if inputValue:
        position = inputValue
        return position
    

    def deleteOrder(self):
        from stepsManager import makeStepInApp
        makeStepInApp(+1)
        
        self.printOrders()
        orderId = self.getOrderIdNumber('do usunięcia')
        ordersDBController.deleteOrdersRecord(orderId)
        self.loadOrders()
        general.alertDeletion('zamówienie numer ' + str(orderId))
        self.printOrders()


    def addOrder(self):
        from stepsManager import makeStepInApp
        makeStepInApp(+1)
        
        menuController.printMenu()
        newOrder = Order()
        newOrder.createNew()
        ordersDBController.addOrdersRecord(general.getJSON(newOrder))
        self.loadOrders()
        self.printOrders()
        #general.alertAddition('nową pozycję do menu')


ordersController = Orders()
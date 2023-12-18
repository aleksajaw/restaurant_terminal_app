from ordersdb import OrdersDB
from menuManager import menuController
from datetime import datetime
import general

ordersDBController = OrdersDB()
currency = menuController.getMenuCurrency()



class OrderElement:
    def __init__(self, element):
        self.name = element['name']
        self.amount = element['amount']
        self.price = float(element['price'])
        self.totalElementPrice = 0
        if not hasattr(element, 'totalElementPrice'):
            self.countTotalElementPrice()
        elif element['totalElementPrice'] == 0:
            self.countTotalElementPrice()
        else:
            self.totalElementPrice = element['totalElementPrice']


    def changeAmount(self, amount):
        self.amount = int(amount)
        self.countTotalElementPrice()


    def countTotalElementPrice(self):
        self.totalElementPrice = float(self.price) * int(self.amount)


    def printOrderElementInfo(self):
        name = self.name
        amount = str(self.amount)
        price = str(self.price)
        totalElPrice = str(self.totalElementPrice)
        info = amount + ' x ' + name + ': '
        info += totalElPrice + ' ' + currency
        info += ' (' + amount + ' x ' + price + ' ' + currency + ')'
        general.printInformation('', info)



class Order:
    def __init__ (self, date = datetime.now().strftime('%X %A %d %b %Y'), orderElements = [], totalPrice = 0):
        self.date = date
        self.orderElements = orderElements
        self.totalPrice = totalPrice


    def printOrderInfo (self):
        general.printInformation('', 'data : ' + self.date + '\n')
        self.printOrderElements()
        general.printInformation('', '\nCałkowity koszt: ' + str(self.totalPrice) + currency)


    def printOrderElements (self):
        for i,element in enumerate(self.orderElements):
            orderEl = OrderElement(element)
            orderEl.printOrderElementInfo()


    def addOrderElement(self):
        enterOrderElPos = ''
        while enterOrderElPos == '':
            enterOrderElPos = input('\nPodaj numer pozycji dania bądź wpisz "koniec", aby zakończyć zamawianie: ')
            if enterOrderElPos == 'koniec':
                return False

            elif not general.isNumber(enterOrderElPos):
                general.alertUnknownCommand()
                enterOrderElPos = ''

            elif int(enterOrderElPos) < 1 or int(enterOrderElPos)-1 > len(menuController.dishList):
                general.alertNoExist('pozycja o numerze ' + enterOrderElPos)
                enterOrderElPos = ''

            elif enterOrderElPos == '':
                general.alertNoCommand()

            else:
                newOrderElement = menuController.getMenuElement( int(enterOrderElPos) )
                amount = 0
                maxAmount = 100
                while amount == 0:
                    amount = input('Podaj ilość zamawianej pozycji: ')
                    if amount == '':
                        general.alertNoCommand('ilość')
                    elif not general.isNumber(amount):
                        general.alertUnknownCommand()
                        amount = 0
                    elif not int(amount):
                        general.alertYouCannot('zamówić tej pozycji w ilości mniejszej niż 1')
                        amount = 0
                    elif int(amount) > maxAmount:
                        general.alertYouCannot('zamówić tej pozycji w ilości większej niż ' + str(maxAmount))
                        amount = 0
                newOrderElement['amount'] = int(amount)
                newOrderElement = OrderElement(newOrderElement)
                self.orderElements.append( general.getJSON(newOrderElement))
            return True


    def ordering(self):
        continueOrdering = True
        itemAddedEnded = False
        menuController.printMenu()
        while continueOrdering:
            itemAddedEnded = self.addOrderElement()
            if itemAddedEnded:
                self.printOrderElements()
            else:
                continueOrdering = False
        if len(self.orderElements) > 0:
            self.countFullCosts()
            ordersDBController.addOrdersRecord(general.getJSON(self))
            return True


    def countFullCosts (self):
        totalPrice = 0
        for i,element in enumerate(self.orderElements):
            totalPrice += element['totalElementPrice']
        self.totalPrice = totalPrice
        ordersController.loadOrders()


        
class Orders:
    def __init__(self):
        self.list = []
        self.loadOrders()


    def loadOrders(self):
        self.list = []
        for order in ordersDBController.getAllOrdersRecords():
            formattedOrder = Order(order['date'], order['orderElements'], order['totalPrice'])
            self.list.append(formattedOrder)


    def printOrders(self):
        general.printInformation('\nZAMÓWIENIA')
        if not len(self.list):
            general.alertNoElements('zamówień')
        for i, record in enumerate(self.list):
            j = i+1
            general.printInformation('\nZMÓWIENIE ' + str(j) + '. ')
            record.printOrderInfo()


    def addOrder(self):
        newOrder = Order()
        orderSuccesfullyComplete = newOrder.ordering()
        if orderSuccesfullyComplete:
            self.loadOrders()
            general.alertAddition('zamówienie')
            newOrder.printOrderInfo()


    def deleteOrder(self):
        self.printOrders()
        orderNrToDel = None
        while orderNrToDel == None:
            orderNrToDel = input('\nPodaj numer zamówienia do usunięcia: ')
            if general.isNumber(orderNrToDel):
                if int(orderNrToDel) > len(self.list) or not int(orderNrToDel):
                    general.alertNoExist('zamówienie numer ' + orderNrToDel)
                    orderNrToDel = None
                else:
                    orderIndexToDel = int(orderNrToDel) - 1
                    ordersDBController.deleteOrdersRecord(general.getJSON(self.list[orderIndexToDel]))
                    self.loadOrders()
                    self.printOrders()
                    general.alertDeletion( 'zamówienie ' + orderNrToDel)
                
            elif orderNrToDel == '':
                general.printInformation('', 'Wpisz numer zamówienia.')
            else:
                general.alertUnknownCommand()
                orderNrToDel = None



ordersController = Orders()
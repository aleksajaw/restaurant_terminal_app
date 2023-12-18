from servicesdb import servicesDBController
from usersManager import usersController
import general



class Services:
    def __init__(self):
        self.setStartServices()
        self.setMainServices()
        self.setMenuServices()
        self.setOrdersServices()
        self.loadServices()
        self.setFilteredServicesByPermissions = {}
    

    def setStartServices(self, value = {}):
        self.startServices = value
    

    def setMainServices(self, value = {}):
        self.mainServices = value


    def setMenuServices(self, value = {}):
        self.menuServices = value


    def setOrdersServices(self, value = {}):
        self.ordersServices = value


    def getService(self, name):
        return servicesDBController.getServicesByName(name)


    def filterServicesByPermissions(self, services):
        if usersController.isLoggedAsAdmin:
            self.filteredServicesByPermissions = services['servicesList']

        else:
            self.filteredServicesByPermissions = [ service
                                for service in services['servicesList']
                                    if not service['needPermission'] ]


    def getFilteredServicesByPermissions(self, services):
        self.filterServicesByPermissions(services)
        return self.filteredServicesByPermissions


    def printFilteredServicesByPermissions(self):
        services = self.filteredServicesByPermissions
        if services:
            msg = ''

            for i, service in enumerate(services):
                j = str(i+1)
                msg += '\n' + j + '. ' + service['name']
            general.printInformation('Dostępne numery poleceń:', msg, '', True)


    def loadServices(self):
        serviceNames = ('start', 'main', 'menu', 'orders')
        for name in serviceNames:
            self.loadServiceByName(name)


    def loadServiceByName(self, serviceName = 'start'):
        serviceData = self.getService(serviceName)
        fnName = 'self.set' + (serviceName).capitalize() + 'Services'
        eval(fnName + '(' + str(serviceData) + ')')


    def getServices(self, name):
        return self.__getattribute__(name + 'Services')
    
        

servicesController = Services()
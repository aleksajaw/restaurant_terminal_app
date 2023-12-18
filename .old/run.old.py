# importowanie kontrolerów obsługujących bazy danych z innych plików
# z pliku o nazwie ... importuj element o nazwie ...
from menumanager import menuController
from ordersmanager import ordersController
from servicesmanager import servicesController
# importowanie zbioru funkcji systemowych
# tutaj akurat w celu użycia funkcji zamykającej program
import sys

# zmienna globalna
# w zależności od tego, czy to użytkownik guest, czy admin,
# możliwe są inne funkcje do użycia
userHasPermissions = False


# funkcja wypisująca ponumerowane usługi (możliwe opcje do wyboru)
def writeServices(filteredServices):
    print('\n')
    j = ''
    for i, service in enumerate(filteredServices):
        j = str(i+1)
        print( j + '. ' + service['name'] )


# funkcja służąca do dynamicznego wywoływania funkcji,
# zmniejszenia ilości kodu kosztem zwiększenia jego stopnia zaawansowania
# opiera się na elementach pobranych z bazy danych:
# podstawowej funkcji "innerController" i jej dalszej część "partOfFunction",
# które są przesyłane do tej funkcji poprzez inne funkcje
# funkcja sprawdza, czy zostały zawarte nawiasy - jeśli nie, to dodaje je
# "eval" to funkcja wbudowana, która zmienną zawierającą ciąg znaków używa jako
# nazwy funkcji, zmiennych itp. i je wywołuje
# następnie wywołuje funkcję inputService, która umożliwia wybranie kolejnego kroku
# argument funkcji comeBackFn domyślne ma wartość "startApp", gdyż jest to pierwszy krok aplikacji
def callServiceFn(fnName, servicesInnerController='', comeBackFn = 'startApp'):
    bracketStr = '('
    fullFnName = servicesInnerController + fnName
    if bracketStr not in fnName: fullFnName += '()'
    eval(fullFnName)
    inputService(fnName, comeBackFn, servicesInnerController)


# funkcja odpowiada za wywoływanie funkcji z argumentami, umożliwiającymi
# powrót do poprzedniego kroku lub wyjście z aplikacji, zamknięcie jej
def goBackFn(serviceInput, mainServicesStep):
    if serviceInput == 'back':
        callServiceFn(mainServicesStep,'','')
    elif serviceInput == 'exit':
        sys.exit()


# funkcja drukująca informację o możliwych poleceniach powrotu
def backOffReminder():
    print('\nAby wrócić wpisz "back".')
    print('Aby wyjść wpisz "exit".\n')


# funkcja odpowiadająca za wybieranie usług
# zawiera funkcję warunkową odpowiadającą za opcje wybrania powrotu lub wyjścia
# oraz opcje wybrania dalszego działania aplikacji
# w swoich argumentach używa usług przefiltrowanych względem uprawnień użytkownika
# zawiera również argumenty będące odpowiednikiem "innerController" oraz "parentStep"
# z bazy danych, które są tylko przesyłane do kolejnych funkcji
# mainServicesStep służy do powrotów - tę funkcję wywołujemy, aby wykonać poprzedni krok

def inputService(filteredServices, mainServicesStep, servicesInnerController=''):
    backOffReminder()
    serviceInput = input('Wybierz usługę: ')
    if serviceInput == 'back' or serviceInput == 'exit':
        goBackFn(serviceInput, mainServicesStep)
    elif filteredServices != None and int(serviceInput) <= len(filteredServices):
        serviceIndex = int(serviceInput) - 1
        chosenServiceFnName = filteredServices[serviceIndex]['partOfFunction']
        print('mainServicesStep: ' + mainServicesStep)
        print('servicesInnerController: ' + servicesInnerController)
        print('chosenServiceFnName: ' + chosenServiceFnName)
        callServiceFn(chosenServiceFnName, servicesInnerController, mainServicesStep)


def generateFullServicesStep(services):
    if userHasPermissions:
        filteredServices = services['servicesList']
    else:
        filteredServices = [service for service in services['servicesList'] if service['needPermission'] == False]
    writeServices(filteredServices)
    inputService(filteredServices, services['parentStep'], services['innerController'])


def getPermissions():
    global userHasPermissions
    command = ''
    check = False
    availableCommands = ['guest', 'admin', 'exit']
    while command not in availableCommands:
        command = input("Zaloguj się. Wpisz swoje dane logowania lub sam login 'guest', aby zalogować się jako gość:")
        if command == 'quest':
            startApp()
        elif command == 'admin':
            checkPermissions()
            if not check: 
                print('Nie uzyskano uprawnień wybranego użytkownika.')
        elif command == 'exit':
            sys.exit()
        else:
            print('Nieznane polecenie.')
    userHasPermissions = check
    startApp()

 
def checkPermissions():
    password = '12345'
    attempt = 0
    authorization = False
    while attempt < 3 and authorization == False:
        inputPassword = input('Podaj hasło: ')
        if inputPassword == password:
            authorization = True
            break
        else:
            print('Niepoprawne hasło.\n')
            attempt+=1

    return authorization


def startApp():
    generateFullServicesStep(servicesController['startServices'])


getPermissions()
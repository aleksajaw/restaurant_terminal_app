## General Info

This project is a terminal restaurant manager.


## Text Navigation

The project is not fully in English yet, but at least the README is :)


* Return commands

    - back -> to go back;
    - exit -> to quit app.


* Other commands

    - To select another available command, enter a specific command number from among those you can see in the current step (with the permissions you have).
        - For example, in step 0, the only number you can enter is the 1 for Login.
    - A version of other steps depends on your user/admin permissions.


## Databases

* All databases are located in *.minify.db files.
* Unminified files have not been created automatically yet.

    
## Users

* Difficult to guess and safe login data for basic users:
    - login: admin
        - password: 123

    - login: guest
        - no password

* Users Database
    - The users data are in usersdb.db file.
    - For now, a primary key here for each record is 'login'.


## Services

* The services data are used to automatically create an each step by inter alia eval() function and loops.

* Services Database
    - We do not really need any primary key here. Services are grouped by 'parent' name, and then their own (service) name.


## Menu

* The menu data file contains dish list and their attributes.

* Menu Database
    - A primary key here for each record is 'position'.


## Orders

* The menu data file contains orders list; their elements and attributes.

* Orders Database
    - A primary key here for each record is 'orderID'.
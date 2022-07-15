# Users_management

Simple messaging server. 


## Table of Contents
* [General info](#general-info)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Contact](#contact)


## General info
The aim of this project was to learn how to integrate databases with object-oriented programing.


## Technologies Used
Project was created with:
* Python version: 3.6.9
* psycopg2-binary version: 2.9.3


## Features
* File `create_db`: simple script creating database and tables. It's idempotent (the property of certain operations in
computer science whereby they can be applied multiple times without changing the result beyond the initial application.)
It means it should work, whether we already have database or not (or if there are any tables). It should not delete data
if there are some in the database
* File `password.py`: we would never store passwords in databases (at least not in its pure form). I used hash
function - function that can be used to map data of arbitrary size to fixed-size values. But it is not enough - if our
data leak into network and other website uses the same hash function what our, so someone who obtained our hash
passwords can easily log in into this site (it only checks passwords hashed, so raw passwords are not needed). <br>
We can protect against it with the help of cryptographic salt ( random data that is used as an additional input to a
one-way function that hashes data, a password or passphrase). So we obtain different hashes from the same string of
characters (using additional random factor, our passwords are even more secure). In addition, each password should have
an individual salt value generated - by using the same salt for all passwords it is like you are not using it at all.
* File `models.py`: a separate class is implemented for each table. Each object has attributes that correspond to the
columns of table. The class implements methods for communicating with database. An object of this class will represent
on row in table. This object is used both to hold data and communicate with the database, as well as to implement any
logic needed further in the program. <br>
The object can be in two states - synchronized or out of sync. Object is synchronized with the databases if the data
held in its attributes is the same as the data in the corresponding row. It occurs in the following cases: loading row
from database to the object; save the object to the database. The object is out of sync with the database in the
following cases: the data held in its attributes is not the same as the data in the corresponding row; there is no row
in the database fot the attributes of the object. Out of sync occurs in the following case: create a new object (there
is no corresponding row); delete a row from the database; changes of any attribute after the last synchronization; row
change in the database after last synchronization.
* File `users.py`: a simple console application for user management. It should handle parameters passed to it from the
console level - argparse library was used for it.
* File `messages.py`: another console application that allows to send messages between users. 


## Screenshots

### Main page:
![Strona główna](/screenshots/1.png)


## Setup
Project requirements are in _requirements.txt_. <br>
To get started:
* ```pip install -r requirements.txt```


## Usage
* After you clone this repo to your desktop, go to its root directory and run ```pip install -r requirements.txt```
to install its dependencies
* You will be able to access it from console, for example when you want to list all users: ```python users.py -l```


## Project Status
Project is _complete_.


## Contact
Created by 117marta - feel free to contact me!

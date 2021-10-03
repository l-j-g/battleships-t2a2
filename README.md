# Battleships-t2a2

Battleships is a multi-player text based game written in python demonstrating development capabilities with networking, use of classes and other object oriented programming.

## Installation: 

To download the source code of the application execute the following command at your command line prompt:
`git clone https://github.com/l-j-g/battleships-t2a2.git`


## Dependencies / Packages Used:
This program runs on Python. To install Python, check out https://installpython3.com/'


Before starting the application ensure that all of the system environment requirements have been met.

To install the necessary dependencies, navigate to your type src folder and execute the following command in your command line prompt:
`pip install -r requirements.txt`

*Battleships* requires the following python packages to be installed.

- `random` : python standard library, used to randomly generate numbers 
- `numpy` : external python package, used to create an array and manipulate data that represents a battleships game board  
- `pdb` : python standard library, used for debugging 
- `socket`: python standard library, for networking and establishing connection between server and client. 
- `sys` : python standard library, used to exit the program.
- `art` : external python package, used to display game title.
- `traceback` : python standard library, used to display debugging information upon error.
- `literal_eval` from asl - python standard library, used to evalute strings communicated over network connection as a Python expression.
- `os` - python standard library, used to evoke a function that will clear the terminal screen, regardless of users operating system.


### Input 

Input is taken from the user during three destinct processes:

- Setting up connection: port, address and role
- Placement of ships: row and column 
- Co-ordinates of an attack: row and column

### Output

### Error Handling
Structure 


## Control Flow:

At a high level the control flow of the program can be described as follows: 

- initialise battleship class 
- initialise connection class as either server or client
- place ships on to the board
- while ships remain on both players boards, players take turns guessing the location of enemy ships.


![Battleships flowchart, showing control flow](./flowchart.svg)
### Classes 

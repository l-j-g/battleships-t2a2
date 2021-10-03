""" Multi-player text based game written in python demonstrating development
 capabilities with networking, use of classes and object oriented programming.
 Author: Lachlan Greve
"""
from classes import Battleships, Connection
import ipaddress


# Initialise battleship game object
game = Battleships()

# Set up a connection between two players
while game.connection_established is False:
    print("Welcome to Battleships")
    print("Setting up a connection...")
    while True:
        try:
            # Get IP address for connection
            address = ipaddress.ip_address(input("Which address to Use? \
(Default: 127.0.0.1): ") or "127.0.0.1")
            address = str(address)
            break
        except ValueError:
            print("Enter an IP address: ")
    while True:
        try:
            # Get port for connection
            port = int(input("Which Port to Use? (Default: 65432): ") or 65432)
            break
        except ValueError:
            print("Enter a number.")
    while True:
        try:
            # Set up two way communication as either a server or a client.
            c_o_s = input("Will you be the (C)lient or (S)erver?: ")
            if c_o_s[0].lower() == 'c':
                game.player = 2
                server = Connection("client", game, address, port)
                break

            if c_o_s[0].lower() == 's':
                game.player = 1
                server = Connection('server', game, address, port)
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid Selection.")
        except IndexError:
            print("Invalid Selection.")

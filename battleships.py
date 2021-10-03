from classes import Battleships,Connection
import ipaddress


game = Battleships()

while game.connection_established == False:
    print("Welcome to Battleships")
    print("Setting up a connection...")
    while True:
        try:
            address = ipaddress.ip_address(input("Which address to Use? (Default: 127.0.0.1): ") or "127.0.0.1")
            address = str(address)
            break
        except ValueError:
            print("Enter an IP address: ")
    while True:
        try:
            port = int(input("Which Port to Use? (Default: 65432): ") or 65432)
            break
        except ValueError:
            print("Enter a number.")
    while True:
        try:
            c_o_s = input("Will you be the (C)lient or (S)erver?: ")
            if c_o_s[0].lower() == 'c':
                game.player = 2
                server = Connection("client",game,address,port)
                break

            if c_o_s[0].lower() == 's':
                game.player = 1
                server = Connection('server',game,address,port)
                break
            else:
                raise ValueError
            
        except ValueError:
            print("Invalid Selection.")
        except IndexError:
            print("Invalid Selection.")
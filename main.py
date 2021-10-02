from classes import Battleships,Connection
import ipaddress


game = Battleships()

while game.connection_established == False:
    print("Welcome to Battleships")
    print("Setting up a connection...")
    while True:
        try:
            address = ipaddress.ip_address(input("Which address to Use? (Default: 127.0.0.1): ") or "127.0.0.1")
            break
        except ValueError:
            print("Enter an IP address: ")
    while True:
        try:
            port = int(input("Which Port to Use? (Default: 65432): ") or 65432)
            break
        except ValueError:
            print("Enter a number.")
    print(" Will you be the Client or Server?")
    c_o_s = input()
    if c_o_s[0].lower() == 'c':
        game.player = 2
        server = Connection("client",game)

    if c_o_s[0].lower() == 's':
        server = Connection('server',game)

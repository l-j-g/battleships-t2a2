from classes import Battleships,Connect
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

game = Battleships()
server = Connect()

while server.connection_established == False:
    print("Client or Server?")
    c_o_s = input()
    if c_o_s[0].lower() == 'c':
        server.role = 'client'
        client = server.set_up()
        game.player = 2
        cls()

    if c_o_s[0].lower() == 's':
        server.role = 'server'
        server.set_up()
        game.player = 1
        cls()

while game.ships_placed == False:
    print("How would you like to place your ships?: (M)anual or (A)utomatic")
    placement = input()
    if placement[0].lower() == 'a':
        for ship in game.ships.values():
            game.place_ships(ship)
        game.ships_placed = True




while game.ready == True:
    game.draw()
    guess = input("Enter the Co-ordinates of your attack: (Row, Column)")
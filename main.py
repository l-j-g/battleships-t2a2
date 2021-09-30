from classes import Battleships,Connection
from functions import *
import pdb


game = Battleships()

while game.ships_placed == False:
    print("How would you like to place your ships?: (M)anual or (A)utomatic")
    placement = input()
    if placement[0].lower() == 'a':
        for ship in game.ships.values():
            game.place_ships(ship)

    game.ships_placed = True

while game.connection_established == False:
    print("Client or Server?")
    c_o_s = input()
    if c_o_s[0].lower() == 'c':
        game.player = 2
        server = Connection("client",game)


    if c_o_s[0].lower() == 's':
        server = Connection('server',game)

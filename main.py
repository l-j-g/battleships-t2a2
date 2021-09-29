from classes import Battleships,Connect
from functions import *
import pdb


game = Battleships()
server = Connect()

while game.ships_placed == False:
    print("How would you like to place your ships?: (M)anual or (A)utomatic")
    placement = input()
    if placement[0].lower() == 'a':
        for ship in game.ships.values():
            game.place_ships(ship)

    game.ships_placed = True

while server.connection_established == False:
    print("Client or Server?")
    c_o_s = input()
    if c_o_s[0].lower() == 'c':
        server.role = 'client'
        server.set_up()
        game.player = 2


    if c_o_s[0].lower() == 's':
        server.role = 'server'
        server.set_up()
        game.player = 1



while game.health > 0 or game.opp_health > 0:
    game.draw()
    game.take_turn(server)
        


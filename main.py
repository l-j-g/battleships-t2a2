from classes import Battleships,Connection
from functions import *
import pdb


game = Battleships()

while game.connection_established == False:
    print("Client or Server?")
    c_o_s = input()
    if c_o_s[0].lower() == 'c':
        game.player = 2
        server = Connection("client",game)

    if c_o_s[0].lower() == 's':
        server = Connection('server',game)

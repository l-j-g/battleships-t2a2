from classes import Battleships,Connect
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

game = Battleships()
print("Client or Server?")

c_o_s = input()
if c_o_s[0].lower() == 'c':
    client = Connect()
    client.client()
    game.player = 2
    cls()

if c_o_s[0].lower() == 's':
    server = Connect()
    server.server()
    game.player = 1
    cls()

game.draw()
print("How would you like to place your ships?: (M)anual or (A)utomatic")
placement = input()
if placement[0].lower() == 'a':
    for ship in game.ships.values():
        game.place_ships(ship)
game.draw()



while game.ready == True:
    guess = input("Enter the Co-ordinates of your attack: (Row, Column)")
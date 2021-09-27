from classes import Battleships,Connect

print("Client or Server?")
c_o_s = input()
if c_o_s[0].lower() == 'c':
    client = Connect()
    client.client()
if c_o_s[0].lower() == 's':
    server = Connect()
    server.server()

game = Battleships()

game.draw()
for ship in game.ships.values():
    game.place_ships(ship)
game.draw()

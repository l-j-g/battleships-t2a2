import classes 

game = classes.Battleships()

game.draw()
for ship in game.ships.values():
    game.place_ships(ship)
game.draw()

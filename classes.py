import string
import random
import numpy as np
class Battleships():
    def __init__(self) -> None:
        self.row_size = 8 #number of rows
        self.col_size = 8 #number of columns
        self.elements = self.row_size * self.col_size
        self.num_ships = 3
        # self.max_ship_size = 4 
        # self.min_ship_size = 1
        # self.num_turns = 39

        self.board = np.zeroes(col_size, row_size)



        self.ships = {
            "carrier" : 5,
            "battleship" : 4,
            "cruiser" : 3,
            "submarine" : 3,
            "destroyer" : 2

        }

    def draw(self):
        board = [[0] * self.col_size for x in range(self.row_size)]
        board_display = [["~"] * self.col_size for x in range(self.row_size)]

        print("\n  " + " ".join(str(x) for x in range(1, self.col_size + 1))) # Column Coodinates (Numbers)
        for row in range(self.row_size):
            print(str(row + 1) + " " + " ".join(str(c) for c in board_display[row]))
        print()

    def place_ships(self):
        for length in self.ships.values():

            direction = 'horizontal' if random.randint(0, 1) == 0 else 'vertical'
            if direction == 'horizontal':
                pass
'''                 if length <= self.col_size:
                    for r in range (self.row_size):
                        for r in range (col_size - length + 1):
                            if 1 not in [board[r][c:c+size]:
                                locations.append({'row' : r, 'col': c}) '''
                        
                    





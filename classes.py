import string
import random
import numpy as np
import pdb
class Battleships():
    def __init__(self) -> None:
        self.row_size = 8 #number of rows
        self.col_size = 8 #number of columns
        self.elements = self.row_size * self.col_size
        self.num_ships = 3
        # self.max_ship_size = 4 
        # self.min_ship_size = 1
        # self.num_turns = 39

        self.board = np.zeros((self.col_size, self.row_size))


        self.ships = {
            "carrier" : 5,
            "battleship" : 4,
            "cruiser" : 3,
            "submarine" : 3,
            "destroyer" : 2
        }


    def draw(self):

        print("  " +" ".join(str(x) for x in range(1, self.col_size + 1))) # Column Coodinates (Numbers)

        count = 1
        for row in self.board:
            print(str(count), end = "" )
            count = count + 1
            for element in row:
                if element == 0:
                    element = ' ~'
                    print(element,end="")
                if element == 1:
                    element = ' x'
                    print(element, end="")
            print("")   

    def place_ships(self,ship):
        direction = 'horizontal' if random.randint(0, 1) == 0 else 'vertical'
        locations = []
        if direction == 'horizontal':

            for r in range (self.row_size):
                for c in range (self.col_size - ship + 1):
                    if 1 not in self.board[r][c:c+ship]:
                        locations.append({'row' : r, 'col': c})
            start_point = locations[random.randint(0,len(locations)-1)]                    
            self.board[start_point['row'],start_point['col']:start_point['col']+ship] = 1

        if direction == 'vertical':
            for c in range (self.col_size):
                for r in range (self.row_size - ship + 1):
                    if 1 not in [self.board[i][c] for i in range(r,r+ship)]:
                        locations.append({'row' : r, 'col': c})
            start_point = locations[random.randint(0,len(locations)-1)]                    
            self.board[start_point['row']:start_point['row']+ship,start_point['col']] = 1
                                
        print(f"Ship Placed at Row: {start_point['row']+1}, Column: {start_point['col']+1}, Direction: {direction}, Length: {ship}")
            





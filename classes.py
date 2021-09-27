import random
import numpy as np
import pdb
import socket
from art import * 


class Battleships:
    def __init__(self) -> None:
        self.row_size = 8 #number of rows
        self.col_size = 8 #number of columns
        self.elements = self.row_size * self.col_size
        self.num_ships = 3
        self.ready = False
        self.player = 1

        self.board = np.zeros((self.col_size, self.row_size))
        self.opp_board = np.zeros((self.col_size, self.row_size))


        self.ships = {
            "carrier" : 5,
            "battleship" : 4,
            "cruiser" : 3,
            "submarine" : 3,
            "destroyer" : 2
        }


    def draw(self):

        tprint('BATTLESHIPS')
        print("     " + Format.underline +"Player 1:" + Format.end)
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

        print("     " + Format.underline +"Player 1:" + Format.end)
        print("  " +" ".join(str(x) for x in range(1, self.col_size + 1))) # Column Coodinates (Numbers)
        count = 1
        for row in self.opp_board:
            print(str(count), end = "" )
            count = count + 1
            for element in row:
                if element == 0:
                    element = ' ?'
                    print(element,end="")
                if element == 1:
                    element = ' x'
                    print(element, end="")
            print("")   
        return



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
        self.ready = True
        return 
            
class Connect:
    def __init__(self, address = "127.0.0.1", port = 65432):
        
        self.address = address
        self.port = 65432
        self.connection_established = False
        self.role = ""


    def set_up(self):

        if self.role == 'server': 
             # Create Socket: 
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #

            try:
                # because sever need to bind and listen
                server_socket.bind((self.address, self.port))
                server_socket.listen()
                print("Waiting for opponent...")
            except:
                print("Error")

            # once the client requests, we need to accept it: 
            connection, address = server_socket.accept()
            self.connection_established = True
            print("Connection Established")

            server_socket.close()

        if self.role == 'client':

            # create socket 
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            # client connects to a listening sever 
            try:
                client_socket.connect((self.address, self.port))
                self.connection_established = True
                print("Connection Established")
            except:
                print("Error: No Server Found")

            """message_to_send = "Test"

            # send the message
            client_socket.sendall(bytes(message_to_send, "utf-8"))

            # get a response 
            received_message = client_socket.recv(1024)

            print(repr(received_message)) """

    def send(self,message):
        pass

class Format:
    end = '\033[0m'
    underline = '\033[4m'

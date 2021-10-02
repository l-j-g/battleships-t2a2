import random
import numpy as np
import pdb
import socket
import sys
from art import * 
import traceback
from ast import literal_eval
import os 
import pdb
'''
TODO: 
	- Commenting 
	- Readme
	- Flowchart
'''

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Battleships:
	"""
 	A class to represent a game of battlehips
	"""
	def __init__(self):
		"""
		Constructs all of the nessecary attributes of the Battleships Object
		"""
		self.row_size = 8  # number of rows
		self.col_size = 8  # number of columns

		self.ships_placed = False
		self.player = ""
		self.connection_established = False
		self.board = np.zeros((self.col_size, self.row_size))
		self.opp_board = np.zeros((self.col_size, self.row_size))
		self.turn = 1

		self.ships = { # length of different ships 
			"Carrier" : 5,
			"Battleship" : 4,
			"Cruiser" : 3,
			"Submarine" : 3,
			"Destroyer" : 2
		}

		self.health = sum(self.ships.values())
		self.opp_health = self.health


	def draw(self):
		""" Clears the terminal screen, prints title display boards."""
		cls()
		tprint('BATTLESHIPS')
		print("   " + Format.underline + "Player " +str(self.player) + "(You):" + Format.end)
		Battleships.print_board(self,self.board)
		print("     " + Format.underline +"Opponent:" + Format.end)
		Battleships.print_board(self,self.opp_board)
		return

	def print_board(self,board): 
		""" 
  		Prints a visual representation of a battleships board (numpy darray)

		Args:
			board (numpy.darray): numpy darray object representation of ship placements
		"""

		print("  " +" ".join(str(x) for x in range(1, self.col_size + 1))) # Print rolumn Coodinates (Numbers)
		count = 1
		for row in board:
			print(str(count), end = "" )
			count = count + 1
			for element in row:
				# empty
				if element == 0:
					element = ' ~'
					print(element,end="")
				# ship present
				if element == 1:
					element = Format.green + ' x' + Format.reset
					print(element, end="")
				# short fired - hit
				if element == 2:
					element = Format.red + ' x' + Format.reset
					print(element,end="")
				# shot fired - missed
				if element == 3:
					element = Format.blue + ' o' + Format.reset
					print(element, end="")
			print("")   
		return



	def get_input(self, direction):
		"""
		Takes user input 

		Args:
			direction (string): direction of input to recieve (row or collumn)

		Returns:
			int: selection of coordinate in direction.
		"""
		while True:
			try:
				guess = int(input(f"Enter {direction}: "))
				if guess in range(1, self.row_size +1):
					guess = guess - 1
					return guess 
				else:
					print("Selection out of range")
			except ValueError:
				print("Enter a number. ")

	def check(self,attack):
		"""
 		Checks to see if input co-ordinates correspondes with the location of a ship on the players board.
		Updates the values of the board and the health depending on the result. 
		
		Args:
			attack (list): co-ordinates of a recieved attack

		Returns:
			int: returns either 1 or 0 to indiciate if the attack was a hit or miss
		"""
		if self.board[attack[0],attack[1]] == 1:
			# hit
			self.health -= 1
			self.board[attack[0],attack[1]] = 2
			return 1
			# miss
		if self.board[attack[0],attack[1]] == 0:
			self.board[attack[0],attack[1]] = 3
			return 0


	def update_opponent_board(self,guess):
		"""
 		Takes a list that describes the co-ordinates of an attack and result and updates
  		the corresponding opponent health and board values.

		Args:
			guess (list): A list corresponding to the result an attack made with structure [row, column, result].
		"""
		if guess[2]== 0:
			self.opp_board[guess[0],guess[1]] = 3

		if guess[2] == 1:
			self.opp_board[guess[0],guess[1]] = 2
			self.opp_health -= 1
	
	def print_turn_text(self, attack):
		"""
		Takes a list that describes the co-ordinates of an attack and result and displays the outcome of the turn to a user.

		Args:
			attack (type): A list corresponding to the result an attack made with structure [row, column, result].
		"""
		print(f"Player {((self.turn+1)%2)+1} fired at Row: {attack[0]+1}, Column {attack[1]+1}...", end="")

		if attack[2] == 1:
    			print("and HIT!")

		if attack[2] == 0:
			print("and Missed!!")

		print(f"You have {self.health} sea people remaining!")
		print(f"Your opponent has {self.opp_health} sea people left!")

	def automatic_placement(self):
		for ship in self.ships.values():

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
		return 
	
	def manual_placement(self):
		for ship in self.ships:
			ship_length = self.ships[ship]
			self.draw()
			while True:
				print(f"Enter the direction to place your {ship} (length: {ship_length})")
				direction = input("(H)orizontal or (V)ertical: ")
				if direction[0].lower() == 'h' or direction[0].lower() == 'v':
					direction = direction[0]
					break
				else:
					print("Invalid selection. Try again.")
			while True:
				print(f"Enter start point of your {ship} (length: {ship_length}): ")
				row = self.get_input("Row")
				col = self.get_input("Column")
				if direction == 'h':
					
					if 1 not in self.board[row][col:col+ship_length] and col+ship_length < self.col_size+1:
						self.board[row,col:col+ship_length] = 1
						break
				if direction =='v':
					if 1 not in self.board[row:row+ship_length,col] and row+ship_length < self.col_size+1:
						self.board[row:row+ship_length,col] = 1
						break
				else:
					print("The ship cannot be placed in that location.")

      


class Connection:
	""" A class to establish two way connection  for a game of battleships 
	
 
  	"""

	def __init__(self, role, game, address = "127.0.0.1", port = 65432):
	   
		# create socket 
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
		self.address = address
		self.port = port 
		self.role = role
		self.game = game

		with self.socket as server:
			try: 
				self.set_up(server)

				if self.game.connection_established == False:
					return

				while self.game.ships_placed == False:
					self.place_ships(server)

				while self.game.health > 0 and self.game.opp_health > 0:
					if self.game.turn == 1:
						self.game.draw()	
						print("Connection Established!... Lets Get Started")
						print(f"You are Player {self.game.player}")
					self.take_turn(server)
				if self.game.health > 0:
					print("Game Over - Congratulations, You Won")

				if self.game.health == 0:
					print("Game Over - Bummer, You Lost")
			except KeyboardInterrupt:
				server.close()


	def set_up(self,server):

		if self.role == 'server': 
			try:
				# sever needs to bind and listen
				server.bind((self.address, self.port))
				server.listen()
				print("Waiting for opponent...")
				# once the client requests, we need to accept it: 
				self.connection, self.address = server.accept()
				self.game.connection_established = True
			except Exception as e:
				print("That port/address doesnt seems to be avalible at the momment")
				print("Try again later.")
				sys.exit(1)
		if self.role == 'client':

			# client connects to a listening sever 
			try:
				server.connect((self.address, self.port))
				self.game.connection_established = True
			except Exception as e: 
				print("ERROR: No valid server was found with the given configuration...")
				print("Restarting...")
				return

	def place_ships(self,server):
		print("How would you like to place your ships?: (M)anual or (A)utomatic")
		placement = input()
		if placement[0].lower() == 'a':
			self.game.automatic_placement()
		if placement[0].lower() == 'm':
			self.game.manual_placement()

		if self.role == 'server':
			print("Waiting for opponent to place their ships...")
			response = self.recieve(server)
			self.send(server,response)
			

		if self.role == 'client':
			self.send(server,'placed')
			print("Waiting for opponent to place their ships...")
			response = self.recieve(server)

		if response == 'placed':
			self.game.ships_placed = True	
     			
	def send(self,s,message):
		try:
			if self.role =='server':
				self.connection.sendall(bytes(message,'utf-8'))
			if self.role == 'client':
				s.sendall(bytes(message,'utf-8'))
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			sys.exit(1)

	def recieve(self,s):
		try:
			if self.role == "server":
				while True:
					message = self.connection.recv(1024)
					if not message:
						break
					return message.decode('utf-8')
			if self.role == "client":
				while True:
					message = s.recv(1024)
					if not message:
						break
					return message.decode('utf-8')
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			sys.exit(1)


	def take_turn(self,server):
		# oscillates between (1, 2)
		if (self.game.turn+1)%2+1 == self.game.player:
			while True:
				guess = []
				guess.append(self.game.get_input("Row"))
				guess.append(self.game.get_input("Column"))

				if self.game.opp_board[guess[0],guess[1]] != 0:
					print("You have already fired at that location")
				else:
					break
        
			self.send(server,repr(guess))
			attack = literal_eval(self.recieve(server))
			self.game.update_opponent_board(attack)

		# oscillates between (2, 1) to dictate turn action
		if (self.game.turn)%2+1 == self.game.player:
			print("Waiting for Opponent to take their turn...")
			attack = literal_eval(self.recieve(server))
			# check if the attack was a hit or miss and update the board
			result = self.game.check(attack)

			attack.append(result)
			self.send(server,repr(attack))

		self.game.draw()
		self.game.print_turn_text(attack)
		self.game.turn += 1

def close_connection(self):
        self.socket.close()

class Format:
	""" A class to represent 
	"""
	end = '\033[0m'
	underline = '\033[4m'
	red = '\u001b[31m'
	reset = '\u001b[0m'
	blink = '\33[5m'
	green = '\u001b[32m'
	blue = '\u001b[34m'
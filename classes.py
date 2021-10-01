import random
import numpy as np
import pdb
import socket
import sys
from art import * 
import traceback
from _thread import *
from ast import literal_eval


class Battleships:
	def __init__(self) -> None:
		self.row_size = 8 #number of rows
		self.col_size = 8 #number of columns
		self.elements = self.row_size * self.col_size
		self.ready = False
		self.ships_placed = False
		self.player = ""
		self.connection_established = False

		self.board = np.zeros((self.col_size, self.row_size))
		self.opp_board = np.zeros((self.col_size, self.row_size))
		self.health = 17
		self.opp_health = 17
		self.turn = 1


		self.ships = {
			"carrier" : 5,
			"battleship" : 4,
			"cruiser" : 3,
			"submarine" : 3,
			"destroyer" : 2
		}


	def draw(self):

		tprint('BATTLESHIPS')
		print("    " + Format.underline +"Your Fleet:" + Format.end)
		Battleships.print_board(self,self.board)
		print("     " + Format.underline +"Opponent:" + Format.end)
		Battleships.print_board(self,self.opp_board)
		return

	def print_board(self,board): 

		print("  " +" ".join(str(x) for x in range(1, self.col_size + 1))) # Column Coodinates (Numbers)
		count = 1
		for row in board:
			print(str(count), end = "" )
			count = count + 1
			for element in row:
				if element == 0:
					element = ' ~'
					print(element,end="")
				if element == 1:
					element = Format.green + ' x' + Format.reset
					print(element, end="")
				if element == 2:
					element = Format.red + ' x' + Format.reset
					print(element,end="")
				if element == 3:
					element = ' o'
					print(element, end="")
			print("")   
		return



	def get_input(self, direction):
		while True:
			try:
				guess = int(input(f"{direction} Guess: "))
				if guess in range(1, self.row_size +1):
					guess = guess - 1
					return guess 
				else:
					print("Selection out of range")
			except ValueError:
				print("Enter a number. ")

	def check(self,attack):
		print(f"Your Opponent fired at Row: {attack[0]+1}, Column {attack[1]+1}...", end="")
		if self.board[attack[0],attack[1]] == 1:
			# hit
			print("and HIT!")
			self.board[attack[0],attack[1]] = 2
			return 1

		if self.board[attack[0],attack[1]] == 0:
			print("and Missed!!")
			self.board[attack[0],attack[1]] = 3
			return 0
				
	def update_opponent_board(self,guess):
		print(guess)
		if guess[2]== 0:
			print("Bummer, you missed")
			self.opp_board[guess[0],guess[1]] = 2

		if guess[2] == 1:
			print("Gottem")
			self.opp_board[guess[0],guess[1]] = 1
	
	def manual_placement(self):
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




class Connection:
	def __init__(self, role, game, address = "127.0.0.1", port = 65432):
	   
		# create socket 
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
		self.address = address
		self.port = port 
		self.role = role
		self.game = game

		with self.socket as server:
			self.set_up(server)

			while self.game.ships_placed == False:
				self.place_ships(server)

			while game.health > 0 or game.opp_health > 0:
				self.game.draw()	
				self.take_turn(server)

	def place_ships(self,server):
		print("How would you like to place your ships?: (M)anual or (A)utomatic")
		placement = input()
		if placement[0].lower() == 'a':
			self.game.manual_placement()

		if self.role == 'server':
			print("Waiting for opponent to place their ships...")
			response = self.recieve(server)
			self.send(server,response)
			

		if self.role == 'client':
			self.send(server,'recieved')
			print("Waiting for opponent to place their ships...")
			response = self.recieve(server)

		if response == 'recieved':
			self.game.ships_placed = True	
     			
	def set_up(self,server):
		if self.role == 'server': 
			try:
				# because sever need to bind and listen
				server.bind((self.address, self.port))
				server.listen()
				print("Waiting for opponent...")
				# once the client requests, we need to accept it: 
				self.connection, self.address = server.accept()
				self.game.connection_established = True
				self.game.player = 1
			except Exception as e:
				print(e)
				print(traceback.format_exc())
				sys.exit(1)

		if self.role == 'client':

			# client connects to a listening sever 
			try:
				server.connect((self.address, self.port))
				self.game.connection_established = True
				self.game.player = 2
			except Exception as e: 
				print("No Server Found")
				self.connection_established = False



				
	def send(self,s,message):
		print(f"Sending {message}")
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
					print(f"Got {message}")
					return message.decode('utf-8')
			if self.role == "client":
				while True:
					message = s.recv(1024)
					if not message:
						break
					print(f"Got {message}")
					return message.decode('utf-8')
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			sys.exit(1)


	def close_connection(self):
			self.socket.close()

	def take_turn(self,server):
		guess = []
		result= ""
		attack = ""

		if self.game.turn == 1:
			print("Connection Established!... Lets Get Started")
			print(f"You are Player {self.game.player}")

		if self.game.turn % 2 == 1:
			if self.game.player == 1: 
				guess.append(self.game.get_input("Row"))
				guess.append(self.game.get_input("Column"))
				self.send(server,repr(guess))
				result = self.recieve(server)

				print(result)

				result = literal_eval(result)
				self.game.update_opponent_board(result)

			if self.game.player == 2: 
				print("Waiting for Opponent to take their turn...")
				attack = literal_eval(self.recieve(server))
				print(attack)
				result = self.game.check(attack)
				attack.append(result)
				print(attack)
				self.send(server,repr(attack))

		if self.game.turn % 2 == 0:
			if self.game.player == 2: 
				guess.append(self.game.get_input("Row"))
				guess.append(self.game.get_input("Column"))
				self.send(server,repr(guess))

				response = literal_eval(self.recieve(server))
				self.game.update_opponent_board(response)

			if self.game.player == 1: 
				print("Waiting for Opponent to take their turn...")

				attack = literal_eval(self.recieve(server))
				response = self.game.check(attack)
				attack.append(response)
				self.send(server,repr(attack))

		self.game.turn += 1
		self.game.draw()

class Format:
	end = '\033[0m'
	underline = '\033[4m'
	red = '\u001b[31m'
	reset = '\u001b[0m'
	blink = '\33[5m'
	green = '\u001b[32m'

import random
import numpy as np
import pdb
import socket
import sys
from art import * 
import traceback
from _thread import *


class Battleships:
	def __init__(self) -> None:
		self.row_size = 8 #number of rows
		self.col_size = 8 #number of columns
		self.elements = self.row_size * self.col_size
		self.ready = False
		self.ships_placed = False
		self.player = ""

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
		print("     " + Format.underline +"Player 1:" + Format.end)
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
								
		return 

	def take_turn(self,server):
		guess = []
		if self.turn % 2 == 1:
			if self.player == 1: 
				guess.append(self.get_row())
				guess.append(self.get_col())
				server.send(guess)
			if self.player == 2: 
				print("Waiting for Opponent to take their turn...")
		if self.turn % 2 == 0:
			if self.player == 2: 
				guess.append(self.get_row())
				guess.append(self.get_col())
				server.send(guess)
			if self.player == 1: 
				print("Waiting for Opponent to take their turn...")
		self.turn += 1
		self.draw()

	def get_row(self):
		while True:
			try:
				guess = int(input("Row Guess: "))
				if guess in range(1, self.row_size +1):
					return guess - 1
				else:
					print("Selection out of range")
			except:
				print("Enter a number. ")

	def get_col(self):
		while True:
			try:
				guess = int(input("Column Guess: "))
				if guess in range(1, self.row_size +1):
					return guess - 1
				else:
					print("Selection out of range")
			except:
				print("Enter a number. ")
class Connect:
	def __init__(self, address = "127.0.0.1", port = 65432):
	   
		# create socket 
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
		self.address = address
		self.port = 65432
		self.connection_established = False
		self.role = ""

	def set_up(self):

		if self.role == 'server': 
			try:
				# because sever need to bind and listen
				with self.socket as s:
					s.bind((self.address, self.port))
					s.listen()
					print("Waiting for opponent...")
					# once the client requests, we need to accept it: 
					self.connection, self.address = s.accept()
					self.connection_established = True
			except Exception as e:
				print(e)
				print(traceback.format_exc())
				sys.exit(1)

		if self.role == 'client':

			# client connects to a listening sever 
			try:
				with self.socket as s:
					self.socket.connect((self.address, self.port))
					self.connection_established = True
			except Exception as e: 
				print("No Server Found")
				self.connection_established = False


				
	def send(self,message):
		try:
			if self.role =='server':
				self.connection.sendall(bytes(message, "utf-8"))
			if self.role == 'client':
				self.socket.sendall(bytes(message, "utf-8"))
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			sys.exit(1)


	def recieve(self):
		try:

			if self.role =='server':
				self.connection.sendall(bytes(message, "utf-8"))
			if self.role == 'client':
    			while True: 
					received_message = self.socket.recv(1024)
					if not received_message: 
						break
			return received_message
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			sys.exit(1)

	def close_connection(self):
			self.socket.close()

class Format:
	end = '\033[0m'
	underline = '\033[4m'

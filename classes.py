import random
import numpy as np
import socket
import sys
from art import tprint
import traceback
from ast import literal_eval
import os


def cls():
    ''' Function used to clear the terminal screen'''
    os.system('cls' if os.name == 'nt' else 'clear')


class Battleships:
    """ Class representing a game of battle ships
    """
    def __init__(self):
        """
        Constructs all of the nessecary attributes of the Battleships Object

        Attributes:
            row_size (int): number of rows on the board
            col_size (int): number of columns on the board
            ships_placed (bool): indicator if ships have been placed yet or not
            player (int): 1 or 2 corresponding to server or client
            board (np.darray) : array representing a board of battleships game
            opp_board (np.darray): array represeting opponents board
            ships (dict): key-value pair of name of ship, length of ship
            health (int): number of points not yet guessed by opponent
            opp_health (int): number of points not yet guessed by player
        """
        self.row_size = 8  # number of rows
        self.col_size = 8  # number of columns

        self.ships_placed = False
        self.player = 0
        self.connection_established = False
        # create array of size col,row
        self.board = np.zeros((self.col_size, self.row_size))
        # create opponent array of same size
        self.opp_board = np.zeros((self.col_size, self.row_size))
        self.turn = 1

        self.ships = {  # length of different ships
            "Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2
        }

        self.health = sum(self.ships.values())
        self.opp_health = self.health

    def draw(self):
        """ Clears the terminal screen, prints title display boards."""
        # Clear the Screen
        cls()
        # Print tile of the game
        tprint('BATTLESHIPS')
        # Print which player the user is
        print("   " + Format.underline + "Player "
              + str(self.player) + "(You):" + Format.end)
        # Print the location of the players ships and opponents guesses
        Battleships.print_board(self, self.board)
        print("     " + Format.underline + "Opponent:" + Format.end)
        # Print the location of your guesses and their outcomes
        Battleships.print_board(self, self.opp_board)
        return

    def print_board(self, board):
        """
          Prints a visual representation of a battleships board (numpy darray)

        Args:
            board (numpy.darray): numpy darray of ship placements
        """
        # Print column Coodinates (Numbers)
        print("  " + " ".join(str(x) for x in range(1, self.col_size + 1)))
        count = 1
        for row in board:
            # Print row co-ordinates
            print(str(count), end="")
            count = count + 1
            for element in row:
                # visual representation of a empty element (0) is a tilde
                if element == 0:
                    element = ' ~'
                    print(element, end="")
                # visual representation of a friendly ship present is a green x
                if element == 1:
                    element = Format.green + ' x' + Format.reset
                    print(element, end="")
                # visual representation of a ship that has been hit is a red x
                if element == 2:
                    element = Format.red + ' x' + Format.reset
                    print(element, end="")
                # visual representation of a missed guess is a blue circle
                if element == 3:
                    element = Format.blue + ' o' + Format.reset
                    print(element, end="")
            print("")
        return

    def get_input(self, direction):
        """
        Takes user input corresponding to a specific direction

        Args:
            direction (string): direction of input to recieve (row or column)

        Returns:
            int: selection of coordinate in direction.
        """
        while True:
            try:
                guess = int(input(f"Enter {direction}: "))
                if guess in range(1, self.row_size + 1):
                    guess = guess - 1
                    return guess
                else:
                    # if the entered number is not within the size of the board
                    print("Selection out of range")
            # if the entered value is not a number
            except ValueError:
                print("Enter a number. ")

    def check(self, attack):
        """
        Checks to see if input co-ordinates correspondes with the
        location of a ship on the players board.
        Updates the values of the board and the health depending on the result.

        Args:
            attack (list): co-ordinates of a recieved attack

        Returns:
            int: indiciate if the attack was a hit (0) or miss (1)
        """
        if self.board[attack[0], attack[1]] == 1:
            # hit
            self.health -= 1
            # update the numerical representation of the outcome of the attack
            self.board[attack[0], attack[1]] = 2
            return 1
            # miss
        if self.board[attack[0], attack[1]] == 0:
            # update the numerical representation of the outcome of the attack
            self.board[attack[0], attack[1]] = 3
            return 0

    def update_opponent_board(self, guess):
        """
         Takes a list that describes the co-ordinates of an attack and
         result and updates the corresponding opponent health and board values.

        Args:
            guess (list): A list corresponding to the result an
            attack made with structure [row, column, result].
        """
        if guess[2] == 0:
            self.opp_board[guess[0], guess[1]] = 3

        if guess[2] == 1:
            self.opp_board[guess[0], guess[1]] = 2
            self.opp_health -= 1

    def print_turn_text(self, attack):
        """
        Takes a list that describes the co-ordinates of an attack and result
        and displays the outcome of the turn to the user.

        Args:
            attack (type): A list corresponding to the result an attack
            made with structure [row, column, result].
        """
        print(f"Player {((self.turn+1)%2)+1} fired at Row: \
{attack[0]+1}, Column: {attack[1]+1}...", end="")

        if attack[2] == 1:
            print("and HIT!")

        if attack[2] == 0:
            print("and Missed!!")

        print(f"You have {self.health} sea people remaining!")
        print(f"Your opponent has {self.opp_health} sea people left!")

    def automatic_placement(self):
        """This function will automatically automatically
        set the placement of the users ships.
        """
        for ship in self.ships.values():
            # direction is randomly chosen as either horizontal or vertical
            direction = ('horizontal' if random.randint(0, 1) == 0
                         else 'vertical')
            # a list of all possible valid locations will be created.
            locations = []

            if direction == 'horizontal':
                # for each row of the board
                for r in range(self.row_size):
                    # for each column of the board where the ship will fit
                    for c in range(self.col_size - ship + 1):
                        # if a ship is not already present
                        if 1 not in self.board[r][c:c+ship]:
                            # add the location to the list of viable locations
                            locations.append({'row': r, 'col': c})
                # select a location randomly from all viable locations
                start_point = locations[random.randint(0, len(locations)-1)]
                # place the ship at the chosen location
                self.board[start_point['row'],
                           start_point['col']:start_point['col']+ship] = 1

            if direction == 'vertical':
                # for each column of the board
                for c in range(self.col_size):
                    # for each row of the board, where the ship will fit
                    for r in range(self.row_size - ship + 1):
                        # if a ship is not already present
                        if 1 not in [self.board[i][c]
                                     for i in range(r, r + ship)]:
                            # add the location to the list of viable locations
                            locations.append({'row': r, 'col': c})
                # select a location randomly from all viable locations
                start_point = locations[random.randint(0, len(locations)-1)]
                # place the ship at the chosen location
                self.board[start_point['row']:start_point['row']
                           + ship, start_point['col']] = 1
        return

    def manual_placement(self):
        """ A function to manually enter the coordinates for a players ships
        """
        # for each ship
        for ship in self.ships:
            ship_length = self.ships[ship]
            # update the visual display after each ship is placed
            self.draw()
            while True:
                print(f"Enter the direction to place your {ship}\
(length: {ship_length})")
                # input if the ship will be horizontal or vertical
                direction = input("(H)orizontal or (V)ertical: ")
                if direction[0].lower() == 'h' or direction[0].lower() == 'v':
                    direction = direction[0]
                    break
                else:
                    print("Invalid selection. Try again.")
            while True:
                print(f"Enter start point of your {ship}\
(length: {ship_length}): ")
                # input the start row
                row = self.get_input("Row")
                # input the start column
                col = self.get_input("Column")
                if direction == 'h':
                    # check if no other ship is present and if the ship fits
                    if 1 not in (self.board[row][col:col + ship_length]
                                 and col + ship_length < self.col_size+1):
                        self.board[row, col:col+ship_length] = 1
                        break
                if direction == 'v':
                    # check if no other ship is present and if the ship fits
                    if 1 not in (self.board[row:row + ship_length, col]
                                 and row+ship_length < self.col_size+1):
                        self.board[row:row + ship_length, col] = 1
                        break
                else:
                    print("The ship cannot be placed in that location.")


class Connection:
    """ A class to establish two way communication between a server and a client
    """

    def __init__(self, role, game, address="127.0.0.1", port=65432):
        """Initialize the connection to the server .

        Attributes:
            role (str): role of the agent (server or client)
            socket (int): socket for connection
            address (str, optional): IP address to connect to
                Defaults to "127.0.0.1".
            port (int, optional): port to connect to. Defaults to 65432.
            game (Battleships): variables and methods relating to game play
        """

        # create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ip address for connection
        self.address = address
        # port for connection
        self.port = port
        # role of agent in connection (either server or client)
        self.role = role
        # access to battleship functions and variables
        self.game = game
        # Use context manager to automatically close connection when finished
        with self.socket as server:
            try:
                # set up connection
                self.set_up(server)

                # confirm that connection was established
                if self.game.connection_established is False:
                    return

                while self.game.ships_placed is False:
                    # prompt the user to place their battleships
                    self.place_ships(server)

                # continuously take turns until one player has no health left
                while self.game.health > 0 and self.game.opp_health > 0:

                    # actions specific to the first turn of the game
                    if self.game.turn == 1:
                        # update visual display of game board
                        self.game.draw()
                        print("Connection Established!... Lets Get Started")
                        print(f"You are Player {self.game.player}")

                    # function to progress the game
                    self.take_turn(server)

                # user wins
                if self.game.health > 0:
                    print("Game Over - Congratulations, You Won")

                # user loses
                if self.game.health == 0:
                    print("Game Over - Bummer, You Lost")

            # if CTRL + C
            except KeyboardInterrupt:
                server.close()

    def set_up(self, server):
        """binds the player to the server

        Args:
            server (Socket): the socket to which the connection is bound
        """

        if self.role == 'server':
            try:
                # sever needs to bind and listen
                server.bind((self.address, self.port))
                server.listen()
                print("Waiting for opponent...")
                # once the client requests, we need to accept it:
                self.connection, self.address = server.accept()
                self.game.connection_established = True
            except Exception:
                print("That port/address doesnt seems to\
 be avaliable at the momment")
                print("Try again later.")
                sys.exit(1)
        if self.role == 'client':

            # client connects to a listening sever
            try:
                server.connect((self.address, self.port))
                self.game.connection_established = True
            except Exception:
                print("ERROR: No valid server was found with the \
given configuration...")
                print("Restarting...")
                return

    def place_ships(self, server):
        """ Place ships on the game board and communicate to opponent when ready.

        Args:
            server (Socket): the socket to which the connection is bound
        """
        print("How would you like to place your ships?: \
(M)anual or (A)utomatic")
        placement = input()
        if placement[0].lower() == 'a':
            self.game.automatic_placement()
        if placement[0].lower() == 'm':
            self.game.manual_placement()

        if self.role == 'server':
            print("Waiting for opponent to place their ships...")
            # wait for opponent to indicate they are ready
            response = self.recieve(server)
            # indicate that you are ready
            self.send(server, response)

        if self.role == 'client':
            # indicate that you are ready
            self.send(server, 'placed')
            print("Waiting for opponent to place their ships...")
            # wait for opponent to indicate they are ready
            response = self.recieve(server)

        # when both players have indicated they are ready
        if response == 'placed':
            self.game.ships_placed = True

    def send(self, s, message):
        """Send a message over an established connection

        Args:
            s (Socket): the socket to which the connection is bound
            message (str): message to send to opponent.
        """
        try:
            if self.role == 'server':
                self.connection.sendall(bytes(message, 'utf-8'))
            if self.role == 'client':
                s.sendall(bytes(message, 'utf-8'))
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            sys.exit(1)

    def recieve(self, s):
        """Receive a message over an established connection.

        Args:
            s (Socket):  the socket to which the connection is bound

        Returns:
            (str) : message received from the connection
        """
        try:
            if self.role == "server":
                # wait until a message has been recieved
                while True:
                    message = self.connection.recv(1024)
                    # if empty message is recieved, stop waiting
                    if not message:
                        break
                    return message.decode('utf-8')
            if self.role == "client":
                # wait until a message has been recieved
                while True:
                    message = s.recv(1024)
                    # if empty message is recieved, stop waiting
                    if not message:
                        break
                    return message.decode('utf-8')
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            sys.exit(1)

    def take_turn(self, server):
        """ Send and recieve coordiantes relating to a turn in a game of battleships

        Args:
            server (Socket): the socket to which the connection is bound
        """
        attack = []
        # oscillates between (1, 2) as each turn progresss
        if (self.game.turn+1) % 2 + 1 == self.game.player:
            # player is the aggressor
            while True:
                guess = []
                # get input for row to attack
                guess.append(self.game.get_input("Row"))
                # get input for column to attack
                guess.append(self.game.get_input("Column"))

                # check that these co-ordinates havent already been used
                if self.game.opp_board[guess[0], guess[1]] != 0:
                    print("You have already fired at that location")
                else:
                    break
            # send the co-ordinates of the attack to the opponent
            self.send(server, repr(guess))
            # recieve the response to your attack & convert to list
            attack = literal_eval(self.recieve(server))
            # update score with result recieved
            self.game.update_opponent_board(attack)

        # oscillates between (2, 1) as each turn progesses
        if (self.game.turn) % 2 + 1 == self.game.player:
            print("Waiting for Opponent to take their turn...")
            # recieve co-ordinates of an attack from opponent
            attack = literal_eval(self.recieve(server))
            # check if the attack was a hit or miss and update the board
            result = self.game.check(attack)
            # add the result to the co-ordinates recieved
            attack.append(result)
            # send back to opponent
            self.send(server, repr(attack))

        # Update the visual representation of the game
        self.game.draw()
        # Print text to the user to describe the outcome of the turn
        self.game.print_turn_text(attack)
        # Advance to the next turn of the game
        self.game.turn += 1


def close_connection(self):
    self.socket.close()


class Format:
    """ A class to represent ASCI escape codes
    """
    end = '\033[0m'
    underline = '\033[4m'
    red = '\u001b[31m'
    reset = '\u001b[0m'
    blink = '\33[5m'
    green = '\u001b[32m'
    blue = '\u001b[34m'

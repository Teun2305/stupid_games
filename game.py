import numpy as np
from random import randint
from time import sleep

BOARD_SIZE = 3  # Size of one size of the board, the board is always a square
GAME_N = 3  # Amount of squares in a line needed to win


class PlayerInterface:
    """
    Interface for Human and AI players
    
    attributes:
        symbol (str):
            symbol of the player, used for representing a player-square
        name (str):
            player's name        
    """

    def __init__(self, symbol):
        """"constructor"""
        self._symbol = symbol
        self._name = self.set_name()

    def get_name(self):
        """"getter of the attribute name"""
        return self._name

    def set_name(self):
        """"setter of the attribute name"""
        pass

    def get_symbol(self):
        """"getter of the attribute symbol"""
        return self._symbol

    def play(self, board):
        """"function which gets the player's next move"""
        pass

    def __str__(self):
        """"dunder method str"""
        return self._symbol

    def __eq__(self, other):
        """"
        dunder method eq
        they are compared on their symbols
        """
        if isinstance(other, self.__class__):
            return self._symbol == other.get_symbol()
        return False


class HumanPlayer(PlayerInterface):
    """
    Class for the human player
    """

    def set_name(self):
        """setter for the attribute name"""
        return input(f"Player {self._symbol}, what is your name? >> ")

    def play(self, board):
        """
        asks the user for their next move

        Returns
        -------
        int
            row of the next move's square
        int
            column of the next move's square

        """
        number = int(input(f'{self._name}, which square would you like to play? >> ')) - 1
        return number // BOARD_SIZE, number % BOARD_SIZE


class MiniMaxPlayer(PlayerInterface):
    """
    Class for the AI player
    """

    def set_name(self):
        """setter for the attribute name"""
        return 'MiniMax'

    def set_other_player(self, other_player):
        """
        setter for the attribute other player

        Parameters
        ----------
        other_player : PlayerInterface
            the opponent of self.

        """
        self.__other_player = other_player

    def __minimax(self, board, maximizing, alpha, beta):
        """
        applying minimax (with alpha-beta pruning) on the game
        this implementation does not have a max depth, so it will 
        become very slow when expanding the board size

        Parameters
        ----------
        board : Board
            the playing board.
        maximizing : bool
            whether it is the maximizing or minimizing player's turn.
        alpha : int
            aplha-value.
        beta : int
            beta-value.

        Returns
        -------
        int
            value of the move.
        (int, int)
            move corresponding the the square on the board.

        """
        if board.is_winner(self):
            return 1, None
        elif board.is_winner(self.__other_player):
            return -1, None
        elif board.is_full():
            return 0, None

        if maximizing:  # Maximizing player
            value = float('-inf')
            move = None
            alpha = float('-inf')
            for row in range(BOARD_SIZE):
                for column in range(BOARD_SIZE):
                    square = row, column
                    if board.move_is_valid(square):
                        new_board = board.get_board_copy()
                        new_board.play_board(square, self)
                        new_value, new_move = self.__minimax(new_board, not maximizing, alpha, beta)
                        alpha = max(new_value, alpha)
                        if new_value > value:
                            value = new_value
                            move = square
                        if alpha >= beta:
                            return value, move
            return value, move
        else:  # Minimizing player
            value = float('inf')
            move = None
            for row in range(BOARD_SIZE):
                for column in range(BOARD_SIZE):
                    square = row, column
                    if board.move_is_valid(square):
                        new_board = board.get_board_copy()
                        new_board.play_board(square, self.__other_player)
                        new_value, new_move = self.__minimax(new_board, not maximizing, alpha, beta)
                        beta = min(new_value, beta)
                        if new_value < value:
                            value = new_value
                            move = square
                        if alpha >= beta:
                            return value, move

            return value, move

    def play(self, board):
        """
        gets the AI's next move

        Returns
        -------
        int
            row of the next move's square
        int
            column of the next move's square

        """
        sleep(randint(4, 8)*0.1)
        return self.__minimax(board, True, float('-inf'), float('inf'))[1]


class Board:
    """
    Class representing a the playing board
    
    attributes:
        board (2d list):
            matrix of size BOARD_SIZE x BOARD_SIZE representing the playing board
    """

    def __init__(self, board=None):
        """
        initialising board, creates an board full of zeroes
        unless a board is given as parameter
        then that board is passed to the attribute

        Parameters
        ----------
        board : 2d list, optional
            matrix of size BOARD_SIZE x BOARD_SIZE representing the playing board.
            The default is None.
        """
        if board is None:
            self.reset_board()
        else:
            self.__board = board

    def reset_board(self):
        """
        creates an list from 1 to BOARD_SIZE and assigns it to the attribute board
        the list is 2d with each list having a length of BOARD_SIZE

        """
        number = 1
        next_board = []
        for i in range(BOARD_SIZE):
            arr = []
            for j in range(BOARD_SIZE):
                arr.append(number)
                number += 1
            next_board.append(arr)

        self.__board = np.array(next_board, dtype=object)

    def get_board(self):
        """getter of the attribute board"""
        return self.__board

    def get_board_copy(self):
        """"returns a copy of the attribute board"""
        return Board(board=self.__board.copy())

    def is_winner(self, player):
        """
        checks whether a players has won the game

        Parameters
        ----------
        player : PlayerInterface
            the player for who to check

        Returns
        -------
        bool
            player has won

        """
        return self.__hori_vert_winner(player) or self.__digonal_winner(player)

    def __hori_vert_winner(self, player):
        """
        checks whether a player has won
        by lining up squares horizontally or vertically

        Parameters
        ----------
        player : PlayerInterface
            the player for who to check

        Returns
        -------
        bool
            player has won by placing sqaures horizontally or vertically

        """
        # Checking for each row
        for row in self.__board:
            if self.__has_winner(row, player):
                return True
        # Checking for each column
        for column in self.__board.transpose():
            if self.__has_winner(column, player):
                return True
        return False

    def __digonal_winner(self, player):
        """
        checks whether a player has won
        by lineing up squares diagonally

        Parameters
        ----------
        player : PlayerInterface
            the player for who to check

        Returns
        -------
        bool
            player has won by placing sqaures diagonally

        """
        # Top left to bottom right
        for row in range(BOARD_SIZE - GAME_N + 1):
            for column in range(BOARD_SIZE - GAME_N + 1):
                array = []
                for i in range(GAME_N):
                    array.append(self.__board[row + i, column + i])
                if self.__has_winner(array, player):
                    return True

        # Top right to bottom left
        for row in range(BOARD_SIZE - GAME_N + 1):
            for column in range(GAME_N - 1, BOARD_SIZE):
                array = []
                for i in range(GAME_N):
                    array.append(self.__board[row + i, column - i])
                if self.__has_winner(array, player):
                    return True
        return False

    def __has_winner(self, array, player):
        """
        counts the amount of consecutive squares a player
        has in an input list

        Parameters
        ----------
        array : list
            1-D list consisting of zeroes and PlayerInterfaces
        player : PlayerInterface
            the player for who to check

        Returns
        -------
        bool
            player has a GAME_N amount of consecutive squares

        """
        counter = 0
        for element in array:
            if element == player:
                counter += 1
            else:
                counter = 0
            if counter == GAME_N:
                return True
        return False

    def play_board(self, selected_square, player):
        """
        adds a player to a specified square on the board

        Parameters
        ----------
        selected_square : (int, int)
            coordinates of a square on the board
        player : PlayerInterface
            player which has to be placed on the board
        """
        row, column = selected_square
        self.__board[row, column] = player

    def move_is_valid(self, selected_square):
        """
        checks whether a move has already been played

        Parameters
        ----------
        selected_square : (int, int)
            coordinates of a square on the board

        Returns
        -------
        bool
            whether the square is still unoccupied

        """
        row, column = selected_square
        return isinstance(self.__board[row, column], int)

    def is_full(self):
        """
        checks if all squares on the board are occupied

        Returns
        -------
        bool
            whether every square on the board is occupies

        """
        for row in self.__board:
            for column in row:
                if isinstance(column, int):
                    return False
        return True

    def get_open_squares(self):
        squares = []
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if not isinstance(self.__board[row, column], PlayerInterface):
                    squares.append((row, column))
        return squares

    def __str__(self):
        """"dunder method str"""
        t = u'\u2550' * 3  # Three horizontal, double lines
        l = u'\u2551'  # One vertical double line
        string = ''
        # Top row
        string += u'\u2554' + (t + u'\u2566') * (BOARD_SIZE - 1) + t + u'\u2557\n'

        # Body of the board
        for i, row in enumerate(self.__board):
            for column in row:
                nr_digits = len(str(column))
                if isinstance(column, int):
                    if nr_digits == 1:
                        string += l + f' {column} '
                    elif nr_digits == 2:
                        string += l + f'{column} '
                    elif nr_digits == 3:
                        string += l + f'{column}'
                    else:
                        raise ValueError('Your board size is too large.')
                else:
                    string += l + ' {} '.format(column)
            string += l + '\n'
            if i < BOARD_SIZE - 1:
                string += u'\u2560' + (t + u'\u256C') * (BOARD_SIZE - 1) + t + u'\u2563\n'
        # Bottom Row        
        string += u'\u255A' + (t + u'\u2569') * (BOARD_SIZE - 1) + t + u'\u255D'
        return string


class Game:
    """"
    Class containing the game logic
    
    attributes:
        player1 (PlayerInterface):
            the first player of the game
        player2 (PLayerInterface):
            the second player of the game
        board (Board):
            the playing board
    """

    def __init__(self):
        """initializes the players and board. Initilizes one human and one AI player"""
        self.__player1 = HumanPlayer(u'\u00D7')
        self.__player2 = MiniMaxPlayer(u'\u25CB')
        self.__player2.set_other_player(self.__player1)
        self.__board = Board()

    def play_game(self):
        """the turn-based game logic is defined in this function"""
        player_turn = self.__player1
        while not self.__board.is_full():
            # Printing board and info
            print('>' * 10 + '<' * 10)
            print(f'{player_turn.get_name()}, it is your turn.')
            print(self.__board)

            # Player making their turn
            turn = self.__get_turn(player_turn)
            self.__board.play_board(turn, player_turn)
            if self.__board.is_winner(player_turn):
                break
            elif player_turn == self.__player1:
                player_turn = self.__player2
            else:
                player_turn = self.__player1

        # Printing final messages        
        print(self.__board)
        if self.__board.is_full():
            print('It\'s a draw!!!')
        else:
            print(f'Congratulations {player_turn.get_name()}, you have won!')

    def __get_turn(self, player):
        """
        retrieves the next move of a player
        also deals with potential misinput

        Parameters
        ----------
        player : PlayerInterface
            player whose move to retrieve

        Returns
        -------
        int
            row of the next move's square
        int
            column of the next move's square

        """
        try:
            turn = player.play(self.__board)
            row, column = turn
            assert 0 <= row < BOARD_SIZE
            assert 0 <= column < BOARD_SIZE
            assert self.__board.move_is_valid(turn)
            return row, column
        except ValueError:
            print('Please enter a NUMBER.')
            return self.__get_turn(player)
        except AssertionError:
            print(f'Please enter a number between 0 and {BOARD_SIZE ** 2 + 1}.')
            print('If a square is already taken, you cannot play it again.')
            return self.__get_turn(player)


def yes_no_input():
    """
    asks the user a yes-ir-no question

    Returns
    -------
    str
        y if the user ansewered yes, n if the users ansewred no

    """
    try:
        response = input('[y/n] >> ').lower()
        assert response == 'y' or response == 'n'
        return response
    except AssertionError:
        print('Invalid input, please enter y or n.')
        return yes_no_input()


if __name__ == '__main__':
    assert GAME_N <= BOARD_SIZE  # Checking whether the constants make sense
    print('Welcome to Tic Tac No!!!')
    print('The game is about to start, do you want to read through the rules first?', end='')

    if yes_no_input() == 'y':
        print('Selecting a square is done by entering the number of that square.')
        print('The number corresponds to its position on the board.')
        print(f'The top left number is 1 and the bottom right number is {BOARD_SIZE ** 2}.')
        print('If you don\'t understand the basic rules of Tic Tac Toe, just google them.')

    # Plays a game until the user's had enough
    while True:
        game = Game()
        game.play_game()
        print('Do you want to play another game?', end='')
        if yes_no_input() == 'n':
            break
    print('Fuck off!')

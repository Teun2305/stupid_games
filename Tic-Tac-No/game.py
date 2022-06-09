import numpy as np
from time import sleep

BOARD_SIZE = 3  # Size of one size of the board, the board is always a square
GAME_N = 3  # Amount of squares in a line needed to win


class PlayerInterface:
    """
    Interface for Human and AI players.

    Attributes:
        symbol (str):
            symbol of the player, used for representing a player-square
        name (str):
            player's name
    """

    def __init__(self, symbol):
        """"Constructor."""
        self.symbol = symbol
        self.name = self.set_name()

    def get_name(self):
        """"Getter of the attribute name."""
        return self.name

    def set_name(self):
        """"Setter of the attribute name."""
        pass

    def get_symbol(self):
        """"Getter of the attribute symbol."""
        return self.symbol

    def play(self, board):
        """"Function which gets the player's next move."""
        pass

    def __str__(self):
        """"Dunder method str."""
        return self.symbol

    def __eq__(self, other):
        """"
        Dunder method eq.
        They are compared on their symbols.
        """
        if isinstance(other, self.__class__):
            return self.symbol == other.get_symbol()
        return False


class HumanPlayer(PlayerInterface):
    """
    Class for the human player
    """

    def set_name(self):
        """Setter for the attribute name."""
        return 'Player'

    def play(self, board):
        """
        Asks the user for their next move.

        Returns
        -------
        int
            Row of the next move's square.
        int
            Column of the next move's square.

        """
        number = int(input(
            f'{self.name}, which square would you like to play? >> ')) - 1
        return number // BOARD_SIZE, number % BOARD_SIZE


class MiniMaxPlayer(PlayerInterface):
    """
    Class for the AI player
    """

    def set_name(self):
        """Setter for the attribute name."""
        return 'AI'

    def set_other_player(self, other_player):
        """
        Setter for the attribute other player.

        Parameters
        ----------
        other_player : PlayerInterface
            The opponent of self.

        """
        self.other_player = other_player

    def minimax(self, board, maximizing, alpha, beta):
        """
        Applying minimax (with alpha-beta pruning) on the game.
        This implementation does not have a max depth, so it will
        become very slow when expanding the board size.

        Parameters
        ----------
        board : Board
            The playing board.
        maximizing : bool
            Whether it is the maximizing or minimizing player's turn.
        alpha : int
            Aplha-value.
        beta : int
            Beta-value.

        Returns
        -------
        int
            Value of the move.
        (int, int)
            Move corresponding the the square on the board.

        """
        if board.is_winner(self):
            return 1, None
        elif board.is_winner(self.other_player):
            return -1, None
        elif board.is_full():
            return 0, None

        if maximizing:  # Maximizing player
            value = float('-inf')
            move = None
            for row in range(BOARD_SIZE):
                for column in range(BOARD_SIZE):
                    square = row, column
                    if board.move_is_valid(square):
                        new_board = board.get_board_copy()
                        new_board.play_board(square, self)
                        new_value, new_move = self.minimax(
                            new_board, not maximizing, alpha, beta)
                        alpha = max(new_value, alpha)
                        if new_value > value:
                            value = new_value
                            move = square
                        # Alpha-Beta pruning step
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
                        new_board.play_board(square, self.other_player)
                        new_value, new_move = self.minimax(
                            new_board, not maximizing, alpha, beta)
                        beta = min(new_value, beta)
                        if new_value < value:
                            value = new_value
                            move = square
                        # Alpha-Beta pruning step
                        if alpha >= beta:
                            return value, move

            return value, move

    def play(self, board):
        """
        Gets the AI's next move.

        Returns
        -------
        int
            Row of the next move's square.
        int
            Column of the next move's square.

        """
        sleep(1.5)
        return self.minimax(board, True, float('-inf'), float('inf'))[1]


class Board:
    """
    Class representing a the playing board

    Attributes:
        board (2d list):
            Matrix of size BOARD_SIZE x BOARD_SIZE representing the playing board.
    """

    def __init__(self, board=None):
        """
        Initialising board, creates an board full of zeroes.
        Unless a board is given as parameter,
        then that board is passed to the attribute.

        Parameters
        ----------
        board : 2d list, optional
            Matrix of size BOARD_SIZE x BOARD_SIZE representing the playing board.
            The default is None.
        """
        if board is None:
            self.reset_board()
        else:
            self.board = board

    def reset_board(self):
        """
        Creates an list from 1 to BOARD_SIZE and assigns it to the attribute board.
        The list is 2d with each list having a length of BOARD_SIZE.

        """
        number = 1
        next_board = []
        for i in range(BOARD_SIZE):
            arr = []
            for j in range(BOARD_SIZE):
                arr.append(number)
                number += 1
            next_board.append(arr)

        self.board = np.array(next_board, dtype=object)

    def get_board(self):
        """Getter of the attribute board."""
        return self.board

    def get_board_copy(self):
        """"Returns a copy of the attribute board."""
        return Board(board=self.board.copy())

    def is_winner(self, player):
        """
        Checks whether a players has won the game.

        Parameters
        ----------
        player : PlayerInterface
            The player for who to check.

        Returns
        -------
        bool
            Player has won.

        """
        return self.hori_vert_winner(player) or self.diagonal_winner(player)

    def hori_vert_winner(self, player):
        """
        Checks whether a player has won
        by lining up squares horizontally or vertically.

        Parameters
        ----------
        player : PlayerInterface
            The player for who to check.

        Returns
        -------
        bool
            Player has won by placing sqaures horizontally or vertically.

        """
        # Checking for each row and column
        for row, column in zip(self.board, self.board.transpose()):
            if self.has_winner(row, player) or self.has_winner(column, player):
                return True
        return False

    def diagonal_winner(self, player):
        """
        Checks whether a player has won
        by lining up squares diagonally.

        Parameters
        ----------
        player : PlayerInterface
            The player for who to check.

        Returns
        -------
        bool
            Player has won by placing sqaures diagonally.

        """
        # Top left to bottom right
        for row in range(BOARD_SIZE - GAME_N + 1):
            for column in range(BOARD_SIZE - GAME_N + 1):
                array = []
                for i in range(GAME_N):
                    array.append(self.board[row + i, column + i])
                if self.has_winner(array, player):
                    return True

        # Top right to bottom left
        for row in range(BOARD_SIZE - GAME_N + 1):
            for column in range(GAME_N - 1, BOARD_SIZE):
                array = []
                for i in range(GAME_N):
                    array.append(self.board[row + i, column - i])
                if self.has_winner(array, player):
                    return True
        return False

    def has_winner(self, array, player):
        """
        Counts the amount of consecutive squares a player
        has in an input list.

        Parameters
        ----------
        array : list
            1-D list consisting of zeroes and PlayerInterfaces.
        player : PlayerInterface
            The player for who to check.

        Returns
        -------
        bool
            Player has a GAME_N amount of consecutive squares.

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
        Adds a player to a specified square on the board.

        Parameters
        ----------
        selected_square : (int, int)
            Coordinates of a square on the board.
        player : PlayerInterface
            Player which has to be placed on the board.
        """
        row, column = selected_square
        self.board[row, column] = player

    def move_is_valid(self, selected_square):
        """
        Checks whether a move has already been played.

        Parameters
        ----------
        selected_square : (int, int)
            Coordinates of a square on the board.

        Returns
        -------
        bool
            Whether the square is still unoccupied.

        """
        row, column = selected_square
        return isinstance(self.board[row, column], int)

    def is_full(self):
        """
        Checks if all squares on the board are occupied.

        Returns
        -------
        bool
            Whether every square on the board is occupies.

        """
        for row in self.board:
            for column in row:
                if isinstance(column, int):
                    return False
        return True

    def get_open_squares(self):
        """
        Checks which squares of the board are still open.

        Returns
        -------
        squares : list
            List of squares that have not yet been played.

        """
        squares = []
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if not isinstance(self.board[row, column], PlayerInterface):
                    squares.append((row, column))
        return squares

    def __str__(self):
        """"Dunder method str of Board class."""
        t = '═══'
        l = '║'
        string = ''
        # Top row
        string += '╔' + (t + '╦') * (BOARD_SIZE - 1) + t + '╗\n'

        # Body of the board
        for i, row in enumerate(self.board):
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
                string += '╠' + (t + '╬') * (BOARD_SIZE - 1) + t + '╣\n'
        # Bottom Row
        string += '╚' + (t + '╩') * (BOARD_SIZE - 1) + t + '╝'
        return string


class Game:
    """"
    Class containing the game logic

    Attributes:
        player1 (PlayerInterface):
            The first player of the game.
        player2 (PLayerInterface):
            The second player of the game.
        board (Board):
            The playing board.
    """

    def __init__(self):
        """Initializes the players and board. Initilizes one human and one AI player."""
        self.player1 = HumanPlayer(u'\u00D7')
        self.player2 = MiniMaxPlayer(u'\u25CB')
        self.player2.set_other_player(self.player1)
        self.board = Board()

    def play_game(self):
        """The turn-based game logic is defined in this function."""
        # Set the starting player
        print('Would you like to go first?', end='')
        start = yes_no_input()
        if start == 'y':
            player_turn = self.player1
        else:
            player_turn = self.player2

        # One iteration of this loop is one player's turn
        while not self.board.is_full():
            # Printing board and info
            print('>' * 10 + '<' * 10)
            print(f'{player_turn.get_name()}, it is your turn.')
            print(self.board)

            # Player making their turn
            turn = self.get_turn(player_turn)
            self.board.play_board(turn, player_turn)
            if self.board.is_winner(player_turn):
                break
            elif player_turn == self.player1:
                player_turn = self.player2
            else:
                player_turn = self.player1

        # Printing final messages
        print('>' * 10 + '<' * 10)
        print(self.board)
        if self.board.is_full():
            print('It\'s a draw!!!')
        else:
            print(f'Congratulations {player_turn.get_name()}, you have won!')

    def get_turn(self, player):
        """
        Retrieves the next move of a player.
        Also deals with potential misinput.

        Parameters
        ----------
        player : PlayerInterface
            Player whose move to retrieve.

        Returns
        -------
        int
            Row of the next move's square.
        int
            Column of the next move's square.

        """
        try:
            turn = player.play(self.board)
            row, column = turn
            assert 0 <= row < BOARD_SIZE
            assert 0 <= column < BOARD_SIZE
            assert self.board.move_is_valid(turn)
            return row, column
        except ValueError:
            print('Please enter a NUMBER.')
            return self.get_turn(player)
        except AssertionError:
            print(
                f'Please enter a number between 0 and {BOARD_SIZE ** 2 + 1}.')
            print('If a square is already taken, you cannot play it again.')
            return self.get_turn(player)


def yes_no_input():
    """
    Asks the user a yes-or-no question.

    Returns
    -------
    str
        'y' if the user ansewered yes, 'n' if the users ansewred no.

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
        print(
            f'The top left number is 1 and the bottom right number is {BOARD_SIZE ** 2}.')
        print('If you don\'t understand the basic rules of Tic Tac Toe, just google them.')

    # Plays a game until the user's had enough
    while True:
        game = Game()
        game.play_game()
        print('Do you want to play another game?', end='')
        if yes_no_input() == 'n':
            break
    print('Fuck off!')

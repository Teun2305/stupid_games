import numpy as np

BOARD_SIZE = 4
GAME_N = 3


class PlayerInterface:
    def __init__(self, symbol):
        self._symbol = symbol
        self._name = self.set_name()

    def get_name(self):
        return self._name

    def set_name(self):
        pass

    def get_symbol(self):
        return self._symbol

    def play(self):
        pass

    def __str__(self):
        return self._symbol

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._symbol == other.get_symbol()
        return False


class HumanPlayer(PlayerInterface):
    def set_name(self):
        #return input(f"Player {self._symbol}, what is your name? >> ")
        return "Teun"

    def play(self):
        # Can raise ValueError
        number = int(input(f"{self._name}, which square would you like to play? >> ")) - 1
        row = number // BOARD_SIZE
        column = number % BOARD_SIZE
        return row, column


class MiniMaxPlayer(PlayerInterface):
    def set_name(self):
        return "MiniMax"

    def play(self):
        """
        TODO: add call to MiniMax algorithm
        TODO: write MiniMax algorithm
        """
        pass


class Board:
    def __init__(self, board=None):
        if board is None:
            self.reset_board()
        else:
            self.__board = board

    def reset_board(self):
        """
        assigns a 3x3 matrix which 0 to the attribute board
        :return: None
        """
        self.__board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=PlayerInterface)

    def get_board(self):
        return self.__board

    def get_board_copy(self):
        return self.__board.copy()

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
        by lineing up squares horizontally or vertically

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
                    array.append(self.__board[row + i][column + i])
                if self.__has_winner(array, player):
                    return True
    
        # Top right to bottom left
        for row in range(BOARD_SIZE - GAME_N + 1):
            for column in range(BOARD_SIZE - GAME_N + 1, BOARD_SIZE):
                array = []
                for i in range(GAME_N):
                    array.append(self.__board[row + i][column - i])
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
        row, column = selected_square
        self.__board[row][column] = player
    
    def __str__(self): 
        t = u"\u2550"*3
        l = u"\u2551"
        string = ""
        # Top row
        string += u"\u2554" + (t + u"\u2566")*(BOARD_SIZE - 1) + t + u"\u2557\n"
        
        # Body of the board
        for i, row in enumerate(self.__board):
            for column in row:
                if column == 0:
                    string += l + "   "
                else:
                    string += l + " " + str(column) + " "
            string += l + "\n"
            if i < BOARD_SIZE - 1:
                string += u"\u2560" + (t + u"\u256C")*(BOARD_SIZE - 1) + t + u"\u2563\n"
        # Bottom Row        
        string += u"\u255A" + (t + u"\u2569")*(BOARD_SIZE - 1) + t + u"\u255D\n"    
        return string
        

if __name__ == '__main__':
    player = HumanPlayer('X')
    board = Board()
    board.play_board(player.play(), player)
    print(board)

import numpy as np

BOARD_SIZE = 3
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
        return "Teun"
        # return input(f"Player {self._symbol}, what is your name? >> ")

    def play(self):
        # Can raise ValueError
        return int(input(f"{self._name}, which square would you like to play? >> "))


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
        self.__board[0][2] = player
        self.__board[1][1] = player
        self.__board[2][0] = player
        return self.__hori_vert_winner(player) or self.__digonal_winner(player)
    
    def __hori_vert_winner(self, player):
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
        counter = 0
        for element in array:
            if element == player:
                counter += 1
            else:
                counter = 0
            if counter == GAME_N:
                return True
        return False
            


if __name__ == '__main__':
    board = Board()
    player = HumanPlayer('X')
    print(board.is_winner(player))

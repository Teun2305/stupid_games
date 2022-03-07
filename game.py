BOARD_SIZE = 3

class PlayerInterface:
    def __init__(self, symbol):
        self.__name = self.set_name()
        self.__symbol = symbol

    def get_name(self):
        return self.__name

    def set_name(self):
        pass

    def get_symbol(self):
        return self.__symbol

    def play(self):
        pass

    def __str__(self):
        return self.__symbol

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__symbol == other.get_symbol()
        return False

class HumanPlayer(PlayerInterface):
    def set_name(self):
        return input(f"Player {self.__symbol}, what is your name?")

    def play(self):
        # Can raise ValueError
        return int(input(f"{self.__name}, which square would you like to play?"))

class MiniMaxPlayer(PlayerInterface):
    def set_name(self):
        return "MiniMax"

    def play(self):
        """
        TODO: add call to MiniMax algorithm
        TODO: write MiniMax algorithm
        """
        pass

if __name__ == '__main__':
    pass

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

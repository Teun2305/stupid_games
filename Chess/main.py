import numpy as np


class Board:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.board = np.zeros(shape=(self.width, self.height), dtype=object)

    def __str__(self):
        t = 3 * u'\u2550'  # Three horizontal, double lines
        l = u'\u2551'  # One vertical double line
        string = ''
        # letters
        letters = 'ABCDEFGH'
        for letter in letters:
            string += f'  {letter} '
        # Top row
        string += u'\n\u2554' + 7 * (t + u'\u2566') + t + u'\u2557\n'

        # Body of the board
        for i, row in enumerate(self.board):
            for column in row:
                if isinstance(column, int):
                    string += l + 3 * ' '
                else:
                    string += l + f' {column} '
            string += l + f' {i + 1}\n'
            if i < 7:
                string += u'\u2560' + 7 * (t + u'\u256C') + t + u'\u2563\n'

        # Bottom Row
        string += u'\u255A' + 7 * (t + u'\u2569') + t + u'\u255D'
        return string


if __name__ == '__main__':
    b = Board()
    print(b)

# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:08:16 2022

@author: teunh

Got inspiration from https://www.geeksforgeeks.org/tic-tac-toe-gui-in-python-using-pygame/
"""

import pygame as pg
import game
from time import sleep

"""
Class with the game logic .
"""
class App:
    def __init__(self, size):
        """
        Constructor for the App class.

        Parameters
        ----------
        size : int/float
            size of the display.

        """
        self.games_played, self.ai_won, self.draw, self.human_won = 0, 0, 0, 0
        self.human = game.HumanPlayer('X')
        self.ai = game.MiniMaxPlayer('O')
        self.ai.set_other_player(self.human)
        self.screen = Screen(size)

    def on_execute(self):
        """
        Handling the game logic.

        Returns
        -------
        bool
            False if the game is exited, true otherwise.

        """
        # Asking whether the human player wants to go first or not
        human_playing = self.screen.yes_or_no('Would you like to go first?')
        if human_playing is None:
            return False

        self.screen.draw_lines()
        running = True
        won = False
        draw = False

        # Main game loop, ends when the player exits or the game is over
        while running and not won and not draw:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # Checks whose turn it is and makes a ask which square they'll play
            if human_playing:
                current_player = self.human
                self.screen.text(current_player=current_player,
                                 human=self.human, ai=self.ai)
                move = self.screen.user_click()
            else:
                current_player = self.ai
                self.screen.text(current_player=current_player,
                                 human=self.human, ai=self.ai)
                move = self.ai.play(self.screen.board.get_board_copy())
            if move is None:
                return False

            # Makes a play and updates the display and variables
            self.play(move, current_player)
            self.screen.text(current_player=current_player,
                             human=self.human, ai=self.ai)

            winner = self.screen.is_winner(self.human, self.ai)
            won = winner > 0
            draw = winner == 0
            self.screen.update_visuals(move)
            human_playing = not human_playing

        # Draw the red line if someone has won            
        if won:
            self.screen.draw_winning_line(current_player)
            if current_player == self.ai:
                self.ai_won += 1
            else:
                self.human_won += 1
        else:
            self.draw += 1
        self.games_played += 1
        sleep(2) # Dramatic effect
        return True

    def play(self, move, player):
        """
        Calls the play function of the player's class in the game module.

        Parameters
        ----------
        move : tuple (int, int)
            row and column on the board to be played.
        player : game.PlayerInterface
            the one who is currently playing.

        """
        self.screen.board.play_board(move, player)

    def reset_board(self):
        """
        Calls the reset method of the board.

        """
        self.screen.board.reset_board()

    def print_results(self):
        """
        Prints a table of how many games were played and the win distribution.

        """
        # Initialize variables which come in handy later
        ai_len = 10 + len(str(self.ai_won))
        draw_len = 8 + len(str(self.draw))
        human_len = 13 + len(str(self.human_won))
        games_len = 20 + len(str(self.games_played))

        # Top line
        string = '╔' + (ai_len + draw_len + human_len + 2) * '═' + '╗\n'

        # Amount of whitespaces before and after the 'Total games played' message
        whitespaces = len(string) - 3 - games_len
        a, b = whitespaces // 2, whitespaces // 2
        if whitespaces % 2 == 1:
            b += 1

        # Second line
        string += '║' + a * ' '
        string += f'Total games played: {self.games_played}'
        string += b * ' ' + '║\n'

        # Third line
        string += '╠' + ai_len * '═' + '╦'
        string += draw_len * '═' + '╦'
        string += human_len * '═' + '╣\n'

        # Fourth line
        string += f'║ AI win: {self.ai_won} ║'
        string += f' Draw: {self.draw} ║'
        string += f' Human win: {self.human_won} ║\n'

        # Bottom line
        string += '╚' + ai_len * '═' + '╩'
        string += draw_len * '═' + '╩'
        string += human_len * '═' + '╝'

        print(string)


"""
Class handling all the display actions.
"""
class Screen:
    def __init__(self, size):
        """
        Constructor for the Screen class.

        Parameters
        ----------
        size : int/float
            size of the display.

        """
        self.board = game.Board()
        self.width, self.height = size, size
        self.screen = pg.display.set_mode((self.width,
                                           self.height + self.height / 5))
        self.circle, self.cross, self.yes_no = self.load_images()
        pg.display.set_caption('Tic-Tac-No')
        pg.init()

    def load_images(self):
        """
        Loads the images used in the app.

        Returns
        -------
        circle : Surface
            Image of a circle.
        cross : Surface
            Image of a cross.
        yes_no : Surface
            Image of yes and no.

        """
        # Loading the images
        o_img = pg.image.load('./images/circle.png')
        x_img = pg.image.load('./images/cross.png')
        yes_no_img = pg.image.load('./images/yes_no.png')

        # Resizing the images
        size = self.width / 3 - self.width / 60
        circle = pg.transform.scale(o_img, (size, size))
        cross = pg.transform.scale(x_img, (size, size))
        yes_no = pg.transform.scale(yes_no_img, (self.width, self.width))
        return circle, cross, yes_no

    def draw_lines(self):
        """
        Draws the lines, such that the sqaures become visible.

        """
        self.screen.fill((255, 255, 255))

        # Drawing the inner and outer lines 
        for i in range(4):
            pg.draw.line(self.screen, 0, (self.width / 3 * i, 0),
                         (self.width / 3 * i, self.height), 7)
            pg.draw.line(self.screen, 0, (0, self.height / 3 * i),
                         (self.width, self.height / 3 * i), 7)
        pg.display.update()

    def text(self, current_player=None, human=None, ai=None, msg=None):
        """
        Shows either msg at the bottom of the display,
        whose turn it is or wo has won.

        Parameters
        ----------
        current_player : game.PlayerInterface, optional
            Player whose turn it is. The default is None.
        human : game,HumanPlayer, optional
            The human player. The default is None.
        ai : game.MiniMaxPlayer, optional
            The AI player. The default is None.
        msg : str, optional
            Message to show. The default is None.

        """
        if msg is None:
            situation = self.is_winner(human, ai)
            if situation == -1:
                message = f'The {current_player.get_name()}\'s turn'
            elif situation == 0:
                message = 'It\'s a draw'
            elif situation == 1:
                message = f'The {human.get_name()} has won'
            elif situation == 2:
                message = f'The {ai.get_name()} has won'
        else:
            message = msg

        pg.font.init()
        font = pg.font.Font(None, self.width // 10)
        text = font.render(message, True, (255, 255, 255))
        self.screen.fill(0, (0, self.height, self.width, self.height / 5))
        text_rect = text.get_rect(center=(self.width / 2,
                                          self.height + self.height / 10))
        self.screen.blit(text, text_rect)
        pg.font.quit()
        pg.display.update()

    def user_click(self):
        """
        Handling the user's input, which is in the form of clicks.

        Returns
        -------
        None
            If the user decides to exit the app.
        row, col : int, int
            Tuple representing the column the player has chosen to play.

        """
        running = True

        # Getting the user input
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
                elif event.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()
                    running = False

        # Checking which square they clicked on
        col = int(x // (self.width / 3))
        if y > self.height:
            return self.user_click()
        else:
            row = int(y // (self.height / 3))

        # Checking whether it has already been selected or not
        if isinstance(self.board.get_board()[row, col], game.PlayerInterface):
            self.text(msg='Already taken, pick another')
            return self.user_click()

        return row, col

    def update_visuals(self, move):
        """
        Adds the latest move as a visual to the display

        Parameters
        ----------
        move : (int, int)
            The square of the board which has been played.

        """
        row, col = move

        if isinstance(self.board.get_board()[row, col], game.HumanPlayer):
            self.screen.blit(self.cross, (self.width / 3 * col,
                                          self.height / 3 * row))
        elif isinstance(self.board.get_board()[row, col], game.MiniMaxPlayer):
            self.screen.blit(self.circle, (self.width / 3 * col,
                                           self.height / 3 * row))
        pg.display.update()

    def draw_winning_line(self, current_player):
        """
        Draw a red line trough the three 'winning' squares on the board.

        Parameters
        ----------
        current_player : game.PlayerInterface
            The player who has won.

        """
        # Get the type of line to draw
        line, n = self.get_position(current_player)

        # Draw the line, depending on the type
        if line == 'row':
            pg.draw.line(self.screen, (255, 0, 0),
                         (self.width / 12, self.height / 6 + n * self.height / 3),
                         (self.width * 11 / 12, self.height / 6 + n * self.height / 3), 15)
        elif line == 'col':
            pg.draw.line(self.screen, (255, 0, 0),
                         (self.width / 6 + n * self.width / 3, self.height / 12),
                         (self.width / 6 + n * self.width / 3, self.height * 11 / 12), 15)
        elif line == 'dia' and n == 0:
            pg.draw.line(self.screen, (255, 0, 0),
                         (self.width / 12, self.height / 12),
                         (self.height * 11 / 12, self.height * 11 / 12), 15)
        elif line == 'dia' and n == 1:
            pg.draw.line(self.screen, (255, 0, 0),
                         (self.width * 11 / 12, self.height / 12),
                         (self.height / 12, self.height * 11 / 12), 15)
        pg.display.update()

    def get_position(self, current_player):
        """
        Looking which in which direction the winning line has to be drawn,
        and where it has to start.

        Parameters
        ----------
        current_player : game.PlayerInterface
            The player who has won.

        Returns
        -------
        str
            Description of the direction.
        int
            number of the staring column/row
            or in case the str is 'dia':
                0 -> top left to bottom right
                1 -> top right to bottom left.

        """
        b = self.board.get_board()

        # Check for a winner row
        for i, row in enumerate(b):
            if self.board.has_winner(row, current_player):
                return 'row', i

        # Check for a winner column
        for i, col in enumerate(b.transpose()):
            if self.board.has_winner(col, current_player):
                return 'col', i

        # Check for a diagonal winner
        if self.board.has_winner([b[0, 0], b[1, 1], b[2, 2]], current_player):
            return 'dia', 0
        if self.board.has_winner([b[0, 2], b[1, 1], b[2, 0]], current_player):
            return 'dia', 1

    def yes_or_no(self, message):
        """
        Shows the yes_no image on the display.

        Parameters
        ----------
        message : str
            Message that goes with the image.

        Returns
        -------
        result : boolean
            True if yes is chosen, False if no is chosen.

        """
        self.screen.blit(self.yes_no, (0, 0))
        self.text(msg=message)
        running = True

        # Checking user inputs
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
                elif event.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()

                    # If the player clicked in the top half of the display
                    result = y < self.height / 2
                    running = False
        return result

    def is_winner(self, human, ai):
        """
        Return the situation of the game.
        Whether either of the players has won, the game ended in a draw,
        or the game has not finished yet.

        Parameters
        ----------
        human : game.HumanPlayer
            The human player.
        ai : game.MiniMaxPlayer
            The AI player.

        Returns
        -------
        int
            1 if the human player has won.
            2 if the AI player has won.
            0 if the game ended in a draw.
            -1 if the game has not yet finished.

        """
        if self.board.is_winner(human):
            return 1
        elif self.board.is_winner(ai):
            return 2
        elif self.board.is_full():
            return 0
        else:
            return -1


if __name__ == '__main__':
    app = App(800)

    # Main loop, breaks when the player exits or doesn't want to play anymore
    while True:
        if not app.on_execute():
            break
        reset = app.screen.yes_or_no('Would you like to play again?')
        if reset is None or not reset:
            break
        app.reset_board()

    app.print_results()
    pg.quit()

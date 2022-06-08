# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:08:16 2022

@author: teunh

Got inspiration from https://www.geeksforgeeks.org/tic-tac-toe-gui-in-python-using-pygame/
"""

import pygame as pg
import game
from time import sleep
from pygame.locals import *


class App:
    def __init__(self, size):
        self.human = game.HumanPlayer('X')
        self.ai = game.MiniMaxPlayer('O')
        self.ai.set_other_player(self.human)
        self.board = game.Board()
        self.width, self.height = size, size
        self.screen = pg.display.set_mode((self.width, self.height + self.height / 5))
        self.circle, self.cross, self.yes_no = self.load_images()
        pg.display.set_caption('Tic-Tac-No')
        pg.init()

    def load_images(self):
        o_img = pg.image.load('./images/circle.png')
        x_img = pg.image.load('./images/cross.png')
        yes_no_img = pg.image.load('./images/yes_no.png')
        size = self.width / 3 - self.width / 60
        circle = pg.transform.scale(o_img, (size, size))
        cross = pg.transform.scale(x_img, (size, size))
        yes_no = pg.transform.scale(yes_no_img, (self.width, self.width))
        return circle, cross, yes_no

    def draw_lines(self):
        self.screen.fill((255, 255, 255))
        for i in range(4):
            pg.draw.line(self.screen, 0, (self.width / 3 * i, 0), (self.width / 3 * i, self.height), 7)
            pg.draw.line(self.screen, 0, (0, self.height / 3 * i), (self.width, self.height / 3 * i), 7)
        pg.display.update()

    def text(self, current_player=None, msg=None):
        if msg is None:
            situation = self.is_winner()
            if situation == -1:
                message = f'The {current_player.get_name()}\'s turn'
            elif situation == 0:
                message = 'It\'s a draw'
            elif situation == 1:
                message = f'The {self.human.get_name()} has won'
            elif situation == 2:
                message = f'The {self.ai.get_name()} has won'
        else:
            message = msg

        pg.font.init()
        font = pg.font.Font(None, self.width // 10)
        text = font.render(message, True, (255, 255, 255))
        self.screen.fill(0, (0, self.height, self.width, self.height / 5))
        text_rect = text.get_rect(center=(self.width / 2, self.height + self.height / 10))
        self.screen.blit(text, text_rect)
        pg.font.quit()
        pg.display.update()

    def user_click(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
                elif event.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()
                    running = False

        col = x // (self.width / 3)
        if y > self.height:
            return self.user_click()
        else:
            row = y // (self.height / 3)
        return int(row), int(col)

    def update_visuals(self):
        for i, row in enumerate(self.board.get_board()):
            for j, col in enumerate(row):
                if isinstance(col, game.HumanPlayer):
                    self.screen.blit(self.cross, (self.width / 3 * j, self.height / 3 * i))
                elif isinstance(col, game.MiniMaxPlayer):
                    self.screen.blit(self.circle, (self.width / 3 * j, self.height / 3 * i))
        pg.display.update()

    def yes_or_no(self, message):
        self.screen.blit(self.yes_no, (0, 0))
        self.text(msg=message)
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
                elif event.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()
                    result = y < self.height / 2
                    running = False
        return result

    def on_execute(self):
        human_playing = self.yes_or_no('Would you like to go first?')
        if human_playing is None:
            return False

        self.draw_lines()
        running = True
        won = False
        draw = False
        while running and not won and not draw:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            if human_playing:
                current_player = self.human
                self.text(current_player=current_player)
                move = self.user_click()
            else:
                current_player = self.ai
                self.text(current_player=current_player)
                move = self.ai.play(self.board.get_board_copy())
            if move is None:
                return False

            self.play(move, current_player)
            self.text(current_player=current_player)

            winner = self.is_winner()
            won = winner > 0
            draw = winner == 0
            self.update_visuals()
            human_playing = not human_playing
        if won:
            print('won')
            self.draw_winning_line(current_player)
        sleep(2)
        return True

    def get_position(self, current_player):
        b = self.board.get_board()
        for i, row in enumerate(b):
            if self.board.has_winner(row, current_player):
                return 'row', i

        for i, col in enumerate(b.transpose()):
            if self.board.has_winner(col, current_player):
                return 'col', i

        if self.board.has_winner([b[0, 0], b[1, 1], b[2, 2]], current_player):
            return 'dia', 0
        if self.board.has_winner([b[0, 2], b[1, 1], b[2, 0]], current_player):
            return 'dia', 1

    def draw_winning_line(self, current_player):
        line, n = self.get_position(current_player)
        print(line, n)
        if line == 'row':
            pg.draw.line(self.screen, (255, 0, 0), (self.width / 12, self.height / 6 + n * self.height / 3),
                         (self.width * 11 / 12, self.height / 6 + n * self.height / 3), 15)
        elif line == 'col':
            pg.draw.line(self.screen, (255, 0, 0), (self.width / 6 + n * self.width / 3, self.height / 12),
                         (self.width / 6 + n * self.width / 3, self.height * 11 / 12), 15)
        elif line == 'dia' and n == 0:
            pg.draw.line(self.screen, (255, 0, 0), (self.width / 12, self.height / 12),
                         (self.height * 11 / 12, self.height * 11 / 12), 15)
        elif line == 'dia' and n == 1:
            pg.draw.line(self.screen, (255, 0, 0), (self.width * 11 / 12, self.height / 12),
                         (self.height / 12, self.height * 11 / 12), 15)
        pg.display.update()

    def is_winner(self):
        if self.board.is_winner(self.human):
            return 1
        elif self.board.is_winner(self.ai):
            return 2
        elif self.board.is_full():
            return 0
        else:
            return -1

    def play(self, move, player):
        self.board.play_board(move, player)

    def reset_board(self):
        self.board.reset_board()


if __name__ == '__main__':
    app = App(600)
    while True:
        if not app.on_execute():
            break
        reset = app.yes_or_no('Would you like to play again?')
        if reset is None or not reset:
            break
        app.reset_board()
    pg.quit()
    print('Goodbye!')

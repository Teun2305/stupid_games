# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 22:26:59 2022

@author: teunh
"""

class Card:
    def __init__(self, suit=None, number=None, joker=False):
        self.joker = joker
        self.suit = suit
        self.number = number
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.suit == other.suit and self.number == other.number
   
    def __str__(self):
        suits_dict = {
            'hearts' : '♥',
            'diamonds' : '♦',
            'spades' : '♠',
            'clubs' : '♣'
            }
        string = '╔═══╗\n'
        if self.joker:
            string += '║Jo-║\n║ker║\n'
        else:
            string += '║ ' + suits_dict[self.suit] + ' ║\n'
            if self.number == '10':
                string += '║10 ║\n'
            else:
                string += '║ ' + str(self.number) + ' ║\n'
        return string + '╚═══╝'
    
    def back_of_card(self):
        return '╔═══╗\n║T  ║\n║  H║\n╚═══╝'

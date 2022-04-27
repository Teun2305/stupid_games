# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 21:24:18 2022

@author: teunh
"""

class PlayerInterface:
    names = []
    
    def __init__(self):
        self.name = self.ask_name()
        self.cards = []
        
    def receive_cards(self, card1, card2):
        self.cards = [card1, card2]
        
    def ask_name(self):
        name = input('What is your name? >> ')
        self.names.append(name)
        return name
    
    def get_move(self):
        pass
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name
    
    def __str__(self):
        pass       
        
        
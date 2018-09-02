#!/usr/bin/env python

# Baccarat Simulator
# @author Stuart Bain <gunfighter@gmail.com>
# 
# This is a quick, down and dirty script to build a baccarat simulator for 
# testing betting strategies and theories. It is for Banco Punto (also known as
# North American baccarat) and NOT Chemin de Fer (which is the version of 
# baccarat played in Europe and popularized by Ian Fleming's James Bond series.).

# This simulator will go off of the descriptions and rules as printed by the
# wizardofodds.com website. http://wizardofodds.com/baccarat

import random
import hashlib

class Deck:
    # This class will be used to create our eight decks of cards. Because
    # baccarat doesn't depend on suits at all, and tens and face cards are
    # all counted as zero we will simplify this by creating an array of the
    # following sequence:
    #       0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0
    # e.g. 10, A, 2, 3, 4, 5, 6, 7, 8, 9, J, Q, K 
    #
    # The sequence will be repeated four times into the list, once for each suit
    """Deck of 52 unsuited playing cards with face cards and tens equal to zero"""
    
    def __init__(self):
        """Create a new deck of cards"""
        self.stack = []
        
        for i in range(4): # Four suits
            for j in range(10): # First 10 cards including the ten as the 0
                self.stack.append(j)
            for k in range(3): # Three face cards, each worth 0
                self.stack.append(0)
    
    def __str__(self):
        """Spew forth a string representing the current stack of cards in the deck"""
        sputum = '' # start w/ a blank string
        for i in self.stack:
            sputum = sputum + str(i)
            
        return sputum

    def shuffle(self): # Can shuffle the entire shoe, but here for sanity's sake
        """Shuffle the deck of cards"""
        random.shuffle(self.stack)
        

    
class Shoe:
    """Baccarat shoe"""
    # TODO: Define number of decks as a constant for shoe creation
    
    def __init__(self, decks = 8): # Default to 8 decks
        self.decks = decks
        self.stack = [] # Start with an empty list
        
        for i in range(self.decks): # Add decks to list
            d = Deck()
            self.stack.extend(d.stack)
        
        # Prepare the shoe for play
        self.shuffle()
        self.hash = self.hexhash()
        self.burnt_hash = False
        self.results = [] # We will use this list to track results for this shoe
        self.burn() # Burn and get ready to roll
        
    
    def __str__(self):
        """Spew forth a string representing the current stack of cards in the deck"""
        sputum = '' # start w/ a blank string
        for i in self.stack:
            sputum = sputum + str(i)
            
        return sputum
        
    def shuffle(self):
        """Shuffle the deck of cards"""
        random.shuffle(self.stack)
    
    def hexhash(self):
        """Returns a 128 character SHA512 hash sum of the shoe. This can be
        used for tracking results and to prevent re-calculating shoes that have
        already been calculated."""
        
        stirrup = self.__str__()
        return hashlib.sha512(stirrup).hexdigest()
    
    def burn(self):
        """Draw the first card out of the shoe and burn the appropriate number of 
        burn cards."""
        first_card = self.stack.pop()
        if (first_card == 0):
            for i in range(10): # Tens and face cards = 10 cards burnt
                self.stack.pop()
        else:
            for i in range(first_card): # All other cards = value burnt (A=1)
                self.stack.pop()

        self.burnt_hash = self.hexhash()
                
    def deal(self, num_cards = 1):
        """Pop the given number of cards out of the shoe and return them"""
        
        if (num_cards == 1): # Single card, so just return the value
            return self.stack.pop()
        
        else: # More than one card requested, so we'll return a list
            cards = []
            for i in range(num_cards):
                cards.append(self.stack.pop())
                
            return(cards)
        
    def deal_hand(self):
        """Here goes a hand step by step
        
        p1, p2, p3 = player's cards
        b1, b2, b3 = banker's cards
        player = player's score
        banker = banker's score
        """
        
        # Check to make sure we still have over 16 cards in the shoe
        if (len(self.stack) < 16):
            return 0        
                
        
        ##After all bets are down, the dealer gives two cards each to the player and the 
        ##banker. Author's Note: My recollection from playing in casino is that the
        ##order of the deal is PBPB
        [p1, b1, p2, b2] = self.deal(4)
        
        # We'll start off p3 and b3 as None
        p3 = None
        b3 = None
        
        ## The score of the hand is the right digit of the total of the cards. For 
        ##example, if the two cards were an 8 and 7, then the total would be 15 and the 
        ##score would be a 5. The scores will always range from 0 to 9 and it is impossible 
        ##to bust.
        # For us, this means modulo 10
        
        player = (p1 + p2) % 10
        banker = (b1 + b2) % 10
        
        #print "Player: " + str(p1) + "+" + str(p2) + "=" + str(player)
        #print "Banker: " + str(b1) + "+" + str(b2) + "=" + str(banker)
        
        ##
        ##A third card may or may not be dealt to either the player or the dealer depending 
        ##on the following rules.
        ##
        ##If either the player or the banker has a total of an 8 or a 9 they both stand. 
        ##This rule overrides all other rules.
        
        if (player == 8 or player == 9 or banker == 8 or banker == 9): #Natural!
            pass
            
        else: # No naturals
            ##If the player's total is 5 or less, then the player hits, otherwise the player stands.
            ##If the player stands, then the banker hits on a total of 5 or less.
            if (player > 5 and banker <= 5):
                b3 = self.deal()
                banker = (b1 + b2 + b3) % 10
            elif (player <= 5):
                p3 = self.deal()
                player = (p1 + p2 + p3) % 10
                
                ## If the player does hit then use the chart below to determine 
                ## if the banker hits (H) or stands (S).
                ## Baccarat Drawing Rules
                ## Banker's
                ## Score                       Player's Third Card
                ##   0	 1	 2	 3	 4	 5	 6	 7	 8	 9
                
                ##   2	 H	 H	 H	 H	 H	 H	 H	 H	 H	 H
                ##   1	 H	 H	 H	 H	 H	 H	 H	 H	 H	 H
                ##   0	 H	 H	 H	 H	 H	 H	 H	 H	 H	 H
                if (banker < 3):
                    b3 = self.deal()
                    banker = (b1 + b2 + b3) % 10
                ##   3	 H	 H	 H	 H	 H	 H	 H	 H	 S	 H
                elif (banker == 3 and p3 != 8):
                    b3 = self.deal()
                    banker = (b1 + b2 + b3) % 10
                ##   4	 S	 S	 H	 H	 H	 H	 H	 H	 S	 S
                elif (banker == 4 and (p3 > 1 and p3 < 8)):
                    b3 = self.deal()
                    banker = (b1 + b2 + b3) % 10
                ##   5	 S	 S	 S	 S	 H	 H	 H	 H	 S	 S
                elif (banker == 5 and (p3 > 3 and p3 < 8)):
                    b3 = self.deal()
                    banker = (b1 + b2 + b3) % 10
                ##   6	 S	 S	 S	 S	 S	 S	 H	 H	 S	 S
                elif (banker == 6 and (p3 > 5 and p3 < 8)):
                    b3 = self.deal()
                    banker = (b1 + b2 + b3) % 10
                ##   7	 S	 S	 S	 S	 S	 S	 S	 S	 S	 S
                elif (banker == 7):
                    pass
        
        ##The score of the player and dealer are compared; the winner is the one that is 
        ##greater. 
        if (player > banker):
            outcome = "P"
        elif (banker > player):
            outcome = "B"
        elif (banker == player):
            outcome = "T"

        self.results.append(outcome)
        
        return outcome

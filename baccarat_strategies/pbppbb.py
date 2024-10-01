# PBPPBB Strategy

# This Baccarat strategy is based on an extended pattern of PBPPBB 
#
# Strategy details:
# - At the beginning, or after a win, the strategy starts the base bet on P
# - Any tie is considered a push and the hand is replayed with the same bet at the same 
#   poing in the PBPPBB pattern
# - Any winning bet resets to the base bet on P, and the pattern starts over
#
# Example of how this would be used with the Martingale system
# - Bets after a loss are doubled (Martingale system), and follow the pattern PBPPBB
# - For example, a loss at the start of the pattern will result in the next hand being
#   a bet on B for 2x the base bet. 
# - A second and third loss will move back to P for 4x and 8x the base bet
# - After a third loss, the fourth and fifth bets will be on B for 16x and 32x the base bet
# - After a fifth loss, the pattern starts over with 64x on P, then 128x on B

# Author: Stuart Bain
# Version: 0.1 
# Date: 2024-10-01

# TODO: Try with other betting systems and patterns:
#   - BPBBPP
#   - Flat betting
#   - Reverse Martingale 
#   - Fibonacci 
#   - D’Alembert 
#   - Reverse D'Alembert
#   - Paroli (three-win reset Reverse Martingale)

class PBPPBBStrategy:
    def __init__(self):
        self.pattern_position = 0
        self.name = 'pbppbb'

    def get_bet_side(self):
        return 'P' if self.pattern_position in [0, 2, 3] else 'B'

    def update(self, result):
        if result == 'win':
            self.pattern_position = 0
        elif result == 'loss':
            self.pattern_position = (self.pattern_position + 1) % 6
        # If it's a tie, we don't change the position

    def reset(self):
        self.pattern_position = 0

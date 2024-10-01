# betting_strategies/martingale.py

class MartingaleProgression:
    def __init__(self, base_bet=1):
        self.base_bet = base_bet
        self.current_bet = base_bet
        self.consecutive_losses = 0

    def get_bet(self):
        return self.current_bet

    def update(self, result):
        if result == 'win':
            self.current_bet = self.base_bet
            self.consecutive_losses = 0
        elif result == 'loss':
            self.current_bet *= 2
            self.consecutive_losses += 1
        # If it's a tie, we don't change anything

    def reset(self):
        self.current_bet = self.base_bet
        self.consecutive_losses = 0

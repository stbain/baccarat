# main.py or simulator.py

from baccarat_strategies.pbppbb import PBPPBBStrategy
from betting_strategies.martingale import MartingaleProgression

class CombinedStrategy:
    def __init__(self, pattern_strategy, betting_strategy):
        self.pattern_strategy = pattern_strategy
        self.betting_strategy = betting_strategy

    def get_bet(self):
        bet_side = self.pattern_strategy.get_bet_side()
        bet_amount = self.betting_strategy.get_bet()
        return bet_side, bet_amount

    def update(self, result):
        self.pattern_strategy.update(result)
        self.betting_strategy.update(result)

    def reset(self):
        self.pattern_strategy.reset()
        self.betting_strategy.reset()

# Usage
pattern_strategy = PBPPBBStrategy()
betting_strategy = MartingaleProgression(base_bet=1)
combined_strategy = CombinedStrategy(pattern_strategy, betting_strategy)

# Simulate a game
for _ in range(10):  # 10 rounds for example
    bet_side, bet_amount = combined_strategy.get_bet()
    print(f"Betting {bet_amount} on {bet_side}")
    
    # Simulate the game result (you'd replace this with your actual game logic)
    import random
    result = random.choice(['win', 'loss', 'tie'])
    print(f"Result: {result}")
    
    combined_strategy.update(result)
    print("---")

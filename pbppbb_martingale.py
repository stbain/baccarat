# Simulator to combine the following stratgies:
# 
# Baccarat Strategy: PBPPBB
# Betting Strategy: Martingale
#
import os
import csv

from baccarat_lib.baccarat import Shoe
from baccarat_strategies.pbppbb import PBPPBBStrategy
from betting_strategies.martingale import MartingaleProgression
from unittest import result

### LOGGING SETUP ###
# Create some log files for this simulation in the ./logs directory.
# and the hands 
# The other log will record the hexhash, the starting bankroll, and the ending bankroll of each shoe
if not os.path.exists('./logs'):
    os.makedirs('./logs')
    print("Created ./logs directory")

# shoes.csv log

# Create ./logs/shoes.csv if it doesn't exist, otherwise open for appending
# Format: hexhash, card_sequence, results
# 
# hexhash is the sha512 hash of the card_sequence and acts as a unique ID for the shoe
# card_sequence is a string of card values, e.g. "01098570394702347020197230"
# results is an array of the results from dealing out the shoe, e.g. ['P','P','B','T','P','B']

shoe_log_file_path = './logs/shoes.csv'
shoe_log_file_exists = os.path.isfile(shoe_log_file_path)
shoe_log_file = open(shoe_log_file_path, 'a', newline='')

if not shoe_log_file_exists:
    shoe_log_writer = csv.writer(shoe_log_file)
    shoe_log_writer.writerow(['hexhash', 'card_sequence','results'])
    print("Created ./logs/shoes.csv file")
else:
    shoe_log_writer = csv.writer(shoe_log_file)

# Create ./logs/simulations.csv if it doesn't exist, otherwise open for appending
simulations_log_file_path = './logs/simulations.csv'
simulations_log_file_exists = os.path.isfile(simulations_log_file_path)
simulations_log_file = open(simulations_log_file_path, 'a', newline='')

if not simulations_log_file_exists:
    simulations_log_writer = csv.writer(simulations_log_file)
    simulations_log_writer.writerow(['hexhash', 'betting_strategy', 'pattern_strategy', 'starting_bankroll', 'ending_bankroll', 'highest_bankroll', 'lowest_bankroll', 'wins', 'losses', 'ties'])
    print("Created ./logs/simulations.csv file")
else:
    simulations_log_writer = csv.writer(simulations_log_file)

# Create hands.csv log
# Format: hexhash, bet_side, bet_amount, result, my_bankroll, my_shoe_wins, my_shoe_losses, my_shoe_ties
hands_log_file_path = './logs/hands.csv'
hands_log_file_exists = os.path.isfile(hands_log_file_path)
hands_log_file = open(hands_log_file_path, 'a', newline='')
if not hands_log_file_exists:
    hands_log_writer = csv.writer(hands_log_file)
    hands_log_writer.writerow(['hexhash', 'bet_side', 'bet_amount', 'result', 'my_bankroll', 'my_shoe_wins', 'my_shoe_losses', 'my_shoe_ties'])
    print("Created ./logs/hands.csv file")
else:
    hands_log_writer = csv.writer(hands_log_file)

# Set up our strategy classes

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

# Set up our simulation
pattern_strategy = PBPPBBStrategy()
pattern_strategy_name = pattern_strategy.name

betting_strategy = MartingaleProgression(base_bet=1)
betting_strategy_name = betting_strategy.name

combined_strategy = CombinedStrategy(pattern_strategy, betting_strategy)
num_shoes = 100000 # Number of shoes to run this simulation for
starting_bankroll = 1000 # Starting bankroll for each shoe

print("Starting simulation...")

for _ in range(num_shoes):
    my_bankroll = starting_bankroll
    my_shoe = Shoe()
    my_shoe.shuffle()
    card_sequence = my_shoe.__str__()

    # Deal out the entire shoe to capture the results
    while len(my_shoe.stack) > 16:
        my_shoe.deal_hand()

    # Add this shoe to the shoe log file csv: hexhash, shoe card sequence
    shoe_log_writer.writerow([my_shoe.hexhash(), card_sequence, my_shoe.results]) 

    # Now we can use the my_shoe.results to run our combined strategy
    combined_strategy.reset()

    # Set up variables to count our wins, losses, and ties for the shoe
    my_shoe_wins = 0
    my_shoe_losses = 0
    my_shoe_ties = 0

    # Set up variables to track the highest and lowest bankroll for the shoe
    highest_bankroll = starting_bankroll
    lowest_bankroll = starting_bankroll

    # Run the combined strategy for each dealt hand result in the shoe
    for result in my_shoe.results:
        (bet_side, bet_amount) = combined_strategy.get_bet()

        # If our bankroll isn't big enough for our bet_amount, we are done with this shoe
        if my_bankroll < bet_amount:
            break

        if bet_side == result:
            my_result = 'win'
            my_shoe_wins += 1

            # If the banker bet wins, charge the commission and increase the bankroll
            if result == 'B':
                my_bankroll += bet_amount * 1.95
            else:
                my_bankroll += bet_amount * 2
            
            if my_bankroll > highest_bankroll:
                highest_bankroll = my_bankroll

        elif result == 'T':
            my_result = 'tie'
            my_shoe_ties += 1

        else:
            my_result = 'loss'
            my_shoe_losses += 1
            my_bankroll -= bet_amount

            if my_bankroll < lowest_bankroll:
                lowest_bankroll = my_bankroll

        # Log the hand to the hands.log
        # Format: hexhash, bet_side, bet_amount, result, my_bankroll
        hands_log_writer.writerow([my_shoe.hexhash(), bet_side, bet_amount, my_result, f"{my_bankroll:.2f}", my_shoe_wins, my_shoe_losses, my_shoe_ties])

        combined_strategy.update(my_result)
        
    # Log the shoe results to the simulations log
    simulations_log_writer.writerow([my_shoe.hexhash(), betting_strategy_name, pattern_strategy_name, f"{starting_bankroll:.2f}", f"{my_bankroll:.2f}", f"{highest_bankroll:.2f}", f"{lowest_bankroll:.2f}", my_shoe_wins, my_shoe_losses, my_shoe_ties])

        
    

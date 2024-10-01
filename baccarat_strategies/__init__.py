# This will initiate the baccarat_strategies module. It will load every strategy and create an array
# of the strategy names for the simulator to present to the user as options.

import importlib
import sys
import os

strategies = []

def init_strategies():
    global strategies
    strategies = []
    sys.path.append("baccarat_strategies")
    
    for strategy in os.listdir("baccarat_strategies"):
        if strategy.endswith(".py") and not strategy.startswith("__"):
            strategy_name = strategy[:-3]  # Remove the .py extension
            importlib.import_module(strategy_name)
            strategies.append(strategy_name)
    
    return strategies

# Call init_strategies when the module is imported
strategies = init_strategies()
# betting_strategies/__init__.py

import importlib
import sys
import os

betting_strategies = []

def init_betting_strategies():
    global betting_strategies
    betting_strategies = []
    sys.path.append("betting_strategies")
    
    for strategy in os.listdir("betting_strategies"):
        if strategy.endswith(".py") and not strategy.startswith("__"):
            strategy_name = strategy[:-3]  # Remove the .py extension
            importlib.import_module(strategy_name)
            betting_strategies.append(strategy_name)
    
    return betting_strategies

# Call init_betting_strategies when the module is imported
betting_strategies = init_betting_strategies()

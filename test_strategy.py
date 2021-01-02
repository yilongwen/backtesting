import pandas as pd
from template_strategy import *


def main():
    candles = pd.read_csv("BTC-USD.csv")
    candles.columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
    strategy = Strategy_Name()
    results = strategy.get_trades(
                  positions=strategy.get_positions(candles)
              )
    
    results.to_csv('test_results.csv')
    

if __name__=="__main__":
    main()
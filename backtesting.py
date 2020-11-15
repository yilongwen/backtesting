from numpy import array, nan, select, where, mean, std
from pandas import DataFrame, Grouper, to_datetime
from typing import List


class Backtesting:
    """
    Base class for vectorised backtesting
    """
    def __init__(
        self, 
        fee_percent: float=0.002
    ):
        self.fee = fee_percent
    
    def _get_features(self, dataframe: DataFrame) -> DataFrame:
        
        raise NotImplementedError
    
    
    def _get_buy(self, dataframe: DataFrame):
        
        raise NotImplementedError
    
    def _get_sell(self, dataframe: DataFrame):
        
        raise NotImplementedError
    
    
    def get_positions(self, dataframe: DataFrame) -> DataFrame:
        """
        Create dataframe with positions based on buys and sells. Max 1 position per pair
        @param dataframe: pandas dataframe with columns ['buy', 'sell']
        @return pandas dataframe, with column ['positions'], 1 = having a position, 0 = otherwise
        """
        positions = self._get_sell(
                        self._get_buy(
                            self._get_features(dataframe.copy())
                        )
                    )

        # Create column 'positions', 1 is long, 0 is exit long, nan is hold. Here we assume we can only buy once
        positions['positions'] = select(
                                     [(positions['buy']==1) & (positions['sell']!=1), (positions['sell']==-1)], 
                                     [1, 0], 
                                     default=nan
                                 )

        # Forward fill nan's, so we get all 1's and 0's. 1 represents that we have a long position 
        positions['positions'] = positions['positions'].fillna(method='ffill')
    
        return positions.reset_index()
    
    
    def get_trades(self, positions: DataFrame, buy_features: List[str]=None, sell_features: List[str]=None) -> DataFrame:
        """
        Create trades dataframe based on positions
        @param positions: pandas dataframe with column ['positions']
        @return pandas dataframe, the backtested trades with start/end date, profit/loss for that trade etc
        """
        # When position switches from 0 to 1, it means a buy. Same reverse logic holds for selling 
        buys = positions.loc[positions['positions'] > positions['positions'].shift()].copy()
        sells = positions.loc[positions['positions'] < positions['positions'].shift()].copy()
        
        # Ignore the last buy without sell/first sell without buy
        if len(buys) > len(sells):
            buys = buys.iloc[:-1]
        if len(buys) < len(sells):
            sells = sells.iloc[1:]

        # Build trades dataframe with buys and sells   
        buy_cols = ['date', 'close', 'volume'] + buy_features if buy_features else ['date', 'close', 'volume']
        trades_df = buys[buy_cols].copy()

        sell_cols =  ['date', 'close', 'volume'] + sell_features if sell_features else ['date', 'close', 'volume']
        trades_df[['close_' + s for s in sell_cols]] = sells[sell_cols].values
        
        # Get profit percentage, with fee's discounted(and a bit more for slippage/bid ask spread)
        trades_df['close_profit'] = trades_df['close_close'] / trades_df['close'] - (1 + self.fee)
        
        return trades_df
    

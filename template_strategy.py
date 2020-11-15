from backtesting import Backtesting

from numpy import array
from pandas import DataFrame
import random

class Strategy_Name(Backtesting):
    """
    Define strategy
    """
    def __init__(self,
                 ma_period: int
                 ):
        super().__init__()
        self.ma_period = ma_period
        
    def _get_features(self, dataframe: DataFrame) -> DataFrame:
        """
        Apply calculations on ohlcv dataframe
        @param dataframe: pandas dataframe with ['date', 'open', 'high', 'low', 'close', 'volume']
        @return pandas dataframe with calculations as added columns
        """

        dataframe['moving_average'] = dataframe['close'].rolling(100).mean()
        
        return dataframe
    
    
    def _get_buy(self, dataframe: DataFrame) -> DataFrame:
        """
        Define buy rules
        @param dataframe: pandas dataframe with candles and calculations
        @return pandas dataframe with column buy 
        """
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['moving_average'])
            ),
        'buy'] = 1
        
        return dataframe
    
    def _get_sell(self, dataframe: DataFrame) -> DataFrame:
        """
        Define sell rules
        @param dataframe: pandas dataframe with candles and calculations
        @return pandas dataframe with column sell 
        """
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['moving_average'])
            ),
        'sell'] = -1
        
        return dataframe
        
        
    
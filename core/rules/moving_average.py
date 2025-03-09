from .base import Rule
import pandas as pd
import numpy as np

class MovingAverageCrossoverRule(Rule):
    def __init__(self, short_window: int, long_window: int):
        self.short_window = short_window
        self.long_window = long_window

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:

        data['short_mavg'] = data['price'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        data['long_mavg'] = data['price'].rolling(window=self.long_window, min_periods=1, center=False).mean()
        
        data['signal'] = 0.0
        data.loc[data['short_mavg'] > data['long_mavg'], 'signal'] = 1
        data.loc[data['short_mavg'] < data['long_mavg'], 'signal'] = -1
        
        return data
    
    def get_parameters(self):
        return {
            "short_window": self.short_window,
            "long_window": self.long_window
        }

    @classmethod
    def from_config(cls, config: dict):
        return cls(config["short_window"], config["long_window"])
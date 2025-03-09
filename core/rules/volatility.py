from base import Rule
import pandas as pd

class VolatilityRule(Rule):
    def __init__(self, window: int, threshold: float):
        self.window = window
        self.threshold = threshold
    
    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        data['volatility'] = data["price"].pct_change().rolling(self.window).std()
        data['signal'] = (data['volatility'] > self.threshold).astype(int)
        return data

    @classmethod
    def from_config(cls, config: dict):
        return cls(config["window"], config["threshold"])
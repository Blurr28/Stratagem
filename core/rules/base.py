from abc import ABC, abstractmethod
import pandas as pd

class Rule(ABC):
    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_parameters(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: dict):
        pass


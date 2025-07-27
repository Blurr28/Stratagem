import pandas as pd
import numpy as np
import os

from system import System

class Data:
    def __init__(self, data_path = None):
        if data_path is not None:
            self._data_path = data_path
        else:
            self._data_path = os.path.join(os.path.dirname(__file__), './prices')
        
        self._keys = self.instruments
        self._cache = {}
        
    def prices(self, name, start_date = None, end_date = None):
        return self.get_prices_from_range(name, start_date, end_date)
    
    def get_prices_from_range(self, instrument, start_date = None, end_date = None):
        df = self.get_raw_prices(instrument)
        
        df['DATETIME'] = pd.to_datetime(df['DATETIME'], format="%d-%m-%Y %H:%M").dt.date
        df['DATETIME'] = pd.to_datetime(df['DATETIME'])

        if start_date and end_date and pd.to_datetime(start_date, dayfirst=True) > pd.to_datetime(end_date, dayfirst=True):
            raise ValueError("Start date must be before end date")
        
        if start_date:
            start_date = pd.to_datetime(start_date, format="%d-%m-%Y")
            df = df[df['DATETIME'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date, format="%d-%m-%Y")
            df = df[df['DATETIME'] <= end_date]
        
        return df

    def get_raw_prices(self, instrument):
        if instrument not in self._cache:
            
            if instrument not in self._keys:
                raise ValueError(f"Instrument {instrument} not found")
            
            df = pd.read_csv(f'{self._data_path}/{instrument}.csv')
            
            #df.set_index(df.columns[0], inplace=True)
            
            self._cache[instrument] = df
        
        return self._cache[instrument]
    
    @property
    def instruments(self):
        return [f.split('.')[0] for f in os.listdir(self._data_path) if f.endswith('.csv')]
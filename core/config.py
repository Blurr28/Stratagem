import yaml
import json

class Config:

    def __init__(self, config=None):
        
        if isinstance(config, ):
            for key, value in config.items():
                setattr(self, key, value)
        elif isinstance(config, str):
            self._load(config)
        elif config is None:
            pass
        else:
            raise ValueError("Invalid config type")
        

    def _load(self, path):
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
            if isinstance(config, dict):
                for key, value in config.items():
                    setattr(self, key, value)
            else:
                raise ValueError("YAML file must contain a dictionary")
    
    def save(self, path):
        with open(path, 'w') as f:
            yaml.dump(self.__dict__, f)
    
    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)
    
    def __iter__(self):
        return iter(self.__dict__.items())
    
    def add(self, key, value):
        if hasattr(self, key):
            raise ValueError(f"Key {key} already exists")
        setattr(self, key, value)
    
    def fetch(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise ValueError(f"Key {key} does not exist")
    
    def remove(self, key):
        if hasattr(self, key):
            delattr(self, key)
        else:
            raise ValueError(f"Key {key} does not exist")
    
    @property
    def keys(self):
        return list(self.__dict__.keys())
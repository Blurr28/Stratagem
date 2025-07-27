from data import Data
from config import Config
from rules_manager import RulesManager

class System:
    def __init__(self, config: Config = None):
        
        if config is None:
            self._config = Config()
        else:
            self._config = config
        
        self._data = Data()
        self._rules_manager = RulesManager()
    
    def list_configs(self):
        return self.config.keys
    
if __name__ == "__main__":
    config = Config()
    data = Data()
    rules_manager = RulesManager()
    system = System(config, data, rules_manager)
    print(system.list_configs())
import pandas as pd
from rules import MovingAverageCrossoverRule, VolatilityRule
from system import System

class RulesManager:
    RULE_CLASSES = {
        "MovingAverageCrossover": MovingAverageCrossoverRule,
        "Volatility": VolatilityRule
    }

    def __init__(self, config: dict = None):
        if config:
            self.config = config

            if config.get('rules'):
                self.rules = self.load_rules_from_config(config)
        
    
    def system_init(self, system: System):
        self._parent = system
        
    def load_rules_from_config(self, config: dict) -> list :
        rule_instances = []

        for rule_config in config.get('rules', []):
            rule_name = rule_config.get('name')
            params = rule_config.get('params', {})
            
            if rule_name in self.RULE_CLASSES:
                rule_instances.append(self.RULE_CLASSES[rule_name].from_config(params))
            else:
                raise ValueError(f"Unknown rule {rule_name}")
        
        return rule_instances
    
    def apply_rules(self, data: pd.DataFrame) -> pd.DataFrame:
        results = {}

        for rule in self.rules:
            results[rule.__class__.__name__] = rule.apply(data.copy())
        
        return results

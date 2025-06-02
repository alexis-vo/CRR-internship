from decimal import Decimal
from core.options import (
    EuropeanCall,
    EuropeanPut,
    AmericanCall,
    AmericanPut,
)

class OptionFactory:
    @staticmethod
    def create_option(option_type: str, spot: Decimal, strike: Decimal, maturity: Decimal, volatility: Decimal, rate: Decimal):
        option_classes = {
            'european_call': EuropeanCall,
            'european_put': EuropeanPut,
            'american_call': AmericanCall,
            'american_put': AmericanPut,
        }

        if option_type not in option_classes:
            raise ValueError(f"Type d'option inconnu : {option_type}")

        return option_classes[option_type](spot, strike, maturity, volatility, rate)

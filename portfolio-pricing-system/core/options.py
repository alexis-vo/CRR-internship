from decimal import Decimal
from abc import ABC, abstractmethod

class Option(ABC):
    def __init__(self, spot: Decimal, strike: Decimal, maturity: Decimal, volatility: Decimal, rate: Decimal):
        self.spot = spot
        self.strike = strike
        self.maturity = maturity
        self.volatility = volatility
        self.rate = rate

    @abstractmethod
    def payoff(self, spot: Decimal) -> Decimal:
        pass

class EuropeanCall(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))

class EuropeanPut(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(self.strike - spot, Decimal("0"))

class AmericanCall(Option):
    is_american = True

    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))

class AmericanPut(Option):
    is_american = True

    def payoff(self, spot: Decimal) -> Decimal:
        return max(self.strike - spot, Decimal("0"))
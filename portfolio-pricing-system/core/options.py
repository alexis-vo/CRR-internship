from decimal import Decimal
from abc import ABC, abstractmethod
from enum import Enum

class OptionType(Enum):
    CALL = "call"
    PUT = "put"
    BOND = "bond"
    SWAP = "swap"
    FUTURE = "future"
    FORWARD = "forward"

class Option(ABC):
    def __init__(self, option_type: OptionType, spot: Decimal, strike: Decimal, maturity: Decimal, volatility: Decimal, rate: Decimal):
        if volatility < Decimal("0") or rate < Decimal("0"):
            raise ValueError("Volatility and rate must be non-negative.")
        if maturity <= Decimal("0"):
            raise ValueError("Maturity must be positive.")
        if strike <= Decimal("0"):
            raise ValueError("Strike must be positive.")
        if spot <= Decimal("0"):
            raise ValueError("Spot must be positive.")
        if not isinstance(option_type, OptionType):
            raise ValueError("Invalid option type provided.")

        self.option_type = option_type
        self.spot = spot
        self.strike = strike
        self.maturity = maturity
        self.volatility = volatility
        self.rate = rate

    @abstractmethod
    def payoff(self, spot: Decimal) -> Decimal:
        pass

class EuropeanOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        if self.option_type == OptionType.CALL:
            return max(spot - self.strike, Decimal("0"))
        else:
            return max(self.strike - spot, Decimal("0"))

class AmericanOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        if self.option_type == OptionType.CALL:
            return max(spot - self.strike, Decimal("0"))
        else:
            return max(self.strike - spot, Decimal("0"))

###############
# TODO
###############

class ExoticOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        if self.option_type == OptionType.CALL:
            return max(spot - self.strike, Decimal("0"))
        else:
            return max(self.strike - spot, Decimal("0"))
    
class BarrierOption(Option):
    def __init__(self, option_type: OptionType, spot: Decimal, strike: Decimal, maturity: Decimal, volatility: Decimal, rate: Decimal, barrier_level: Decimal):
        super().__init__(option_type, spot, strike, maturity, volatility, rate)
        if barrier_level <= Decimal("0"):
            raise ValueError("Barrier level must be positive.")
        self.barrier_level = barrier_level

    def payoff(self, spot: Decimal) -> Decimal:
        if (self.option_type == OptionType.CALL and spot < self.barrier_level) or (self.option_type == OptionType.PUT and spot > self.barrier_level):
            return Decimal("0")
        return super().payoff(spot)

class BondOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))
    
class SwapOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))
    
class FutureOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))

class ForwardOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))
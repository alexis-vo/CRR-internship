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

class OptionOrigin:
    def __init__(self):
        self.origin = {
            'eur': False,  # Européennes
            'usa': False,  # Américaines
            'exo': False,  # Exotiques
            'bar': False   # Barrier'
        }
        self.true_keys = [key for key, value in self.origin.items() if value]

    def set_option(self, key, value):
        if key in self.origin:
            self.origin[key] = value
            if value and key not in self.true_keys:
                self.true_keys.append(key)
            elif not value and key in self.true_keys:
                self.true_keys.remove(key)
        else:
            print(f"Option {key} non trouvée.")

    def get_true_keys(self):
        return self.true_keys

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
        self.option_origin = OptionOrigin()
        self.spot = spot
        self.strike = strike
        self.maturity = maturity
        self.volatility = volatility
        self.rate = rate

    @abstractmethod
    def payoff(self, spot: Decimal) -> Decimal:
        pass

    @abstractmethod
    def origin(self):
        pass

class EuropeanOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        if self.option_type == OptionType.CALL:
            return max(spot - self.strike, Decimal("0"))
        else:
            return max(self.strike - spot, Decimal("0"))

    def origin(self):
        self.option_origin.set_option('eur', True)
        return self.option_origin.get_true_keys()

class AmericanOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        if self.option_type == OptionType.CALL:
            return max(spot - self.strike, Decimal("0"))
        else:
            return max(self.strike - spot, Decimal("0"))

    def origin(self):
        self.option_origin.set_option('usa', True)
        return self.option_origin.get_true_keys()

###############
# TODO
###############

class ExoticOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        if self.option_type == OptionType.CALL:
            return max(spot - self.strike, Decimal("0"))
        else:
            return max(self.strike - spot, Decimal("0"))

    def origin(self):
        self.option_origin.set_option('exo', True)
        return self.option_origin.get_true_keys()
    
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

    def origin(self):
        self.option_origin.set_option('bar', True)
        return self.option_origin.get_true_keys()

class BondOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))

    def origin(self):
        self.option_origin.set_option('eur', True)  # Assuming bond options are European
        return self.option_origin.get_true_keys()
    
class SwapOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))

    def origin(self):
        self.option_origin.set_option('exo', True)  # Assuming swap options are exotic
        return self.option_origin.get_true_keys()
    
class FutureOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))

    def origin(self):
        self.option_origin.set_option('exo', True)  # Assuming future options are exotic
        return self.option_origin.get_true_keys()

class ForwardOption(Option):
    def payoff(self, spot: Decimal) -> Decimal:
        return max(spot - self.strike, Decimal("0"))

    def origin(self):
        self.option_origin.set_option('exo', True)  # Assuming forward options are exotic
        return self.option_origin.get_true_keys()
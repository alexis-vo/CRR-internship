import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from decimal import Decimal
from core.options import Option
from models.binomial import binomial_option_pricing

class HedgingStrategy:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def compute_delta(self, option, steps=100):
        spot_up = option.spot * Decimal("1.01")
        spot_down = option.spot * Decimal("0.99")
        
        # Create new options with slightly adjusted spot prices
        # to compute the delta using finite difference method
        option_up = option.__class__(option.option_type, spot_up, option.strike, option.maturity, option.volatility, option.rate)
        option_down = option.__class__(option.option_type, spot_down, option.strike, option.maturity, option.volatility, option.rate)
        
        price_up = self.portfolio.pricing_model(option_up, steps=steps)
        price_down = self.portfolio.pricing_model(option_down, steps=steps)
        
        delta = (price_up - price_down) / (spot_up - spot_down)
        return delta

    def hedge_delta(self, steps=100):
        print("---- Delta Hedging ----")
        total_delta = Decimal("0")
        for position in self.portfolio.positions:
            delta = self.compute_delta(position.option, steps=steps)
            hedge = delta * Decimal(position.quantity)
            print(f"{position.quantity} x {position.option.__class__.__name__} → Delta ≈ {delta:.4f} → Hedge: {hedge:.4f} units of underlying asset")
            total_delta += hedge
        print(f"\nTotal net delta of portfolio ≈ {total_delta:.4f}")
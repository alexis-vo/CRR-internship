import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from decimal import Decimal
from typing import Callable
from dataclasses import dataclass
from core.options import Option

class Position:
    def __init__(self, option: Option, quantity: int):
        self.option = option
        self.quantity = quantity

    def value(self, spot: Decimal, pricing_model: Callable, steps=100) -> Decimal:
        return pricing_model(self.option, spot=spot, steps=steps) * self.quantity

class Portfolio:
    def __init__(self, pricing_model: Callable):
        self.positions: list[Position] = []
        self.pricing_model = pricing_model

    def add_position(self, position: Position):
        self.positions.append(position)

    def total_value(self, spot_dict: dict[str, Decimal], steps=100) -> Decimal:
        return sum(
            pos.value(spot=spot_dict[pos.option.asset_name], pricing_model=self.pricing_model, steps=steps)
            for pos in self.positions
        )

    def summary(self, spot_dict: dict[str, Decimal], steps=100):
        print("---- Portfolio Summary ----")
        for i, pos in enumerate(self.positions):
            asset = pos.option.asset_name
            val = pos.value(spot=spot_dict[asset], pricing_model=self.pricing_model, steps=steps)
            print(f"Position {i+1}: {pos.quantity} x {asset} {pos.option.__class__.__name__} "
                  f" ({pos.option.option_type.value}) → Value: {val:.4f}")
        total = self.total_value(spot_dict, steps=steps)
        print(f"Total Portfolio Value: {total:.4f}")
    

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from decimal import Decimal
from core.options import Option

class Position:
    def __init__(self, option: Option, quantity: int):
        self.option = option
        self.quantity = quantity

    def value(self, spot: Decimal, pricing_model) -> Decimal:
        return self.quantity * pricing_model(self.option)

class Portfolio:
    def __init__(self, pricing_model):
        self.positions = []
        self.pricing_model = pricing_model

    def add_position(self, option, quantity):
        self.positions.append(Position(option, quantity))

    def total_value(self, steps=100):
        return sum(self.pricing_model(pos.option, steps=steps) * pos.quantity for pos in self.positions)

    def summary(self, spot: Decimal, pricing_model):
        print("---- Portfolio Summary ----")
        for i, pos in enumerate(self.positions):
            val = pos.value(spot, pricing_model)
            print(f"Position {i+1}: {pos.quantity} x {pos.option.__class__.__name__} ({pos.option.option_type.value}) → Value: {val}")
        print(f"Total Portfolio Value: {self.total_value(spot, pricing_model)}")
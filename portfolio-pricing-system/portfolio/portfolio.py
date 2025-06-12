import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from decimal import Decimal
from core.options import Option

class Position:
    def __init__(self, option: Option, quantity: int):
        self.option = option
        self.quantity = quantity

    def value(self, spot: Decimal, pricing_model, steps=100):
        return pricing_model(self.option, steps=steps) * self.quantity

class Portfolio:
    def __init__(self, pricing_model):
        self.positions = []
        self.pricing_model = pricing_model

    def add_position(self, position: Position):
        self.positions.append(position)

    def total_value(self, spot: Decimal):
        return sum(pos.value(spot, self.pricing_model) for pos in self.positions)

    def summary(self, spot: Decimal):
        print("---- Portfolio Summary ----")
        for i, pos in enumerate(self.positions):
            val = pos.value(spot, self.pricing_model)
            print(f"Position {i+1}: {pos.quantity} x {pos.option.__class__.__name__} ({pos.option.option_type.value}) → Value: {val}")
        print(f"Total Portfolio Value: {self.total_value(spot, self.pricing_model)}")
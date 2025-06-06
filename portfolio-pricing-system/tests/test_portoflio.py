import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from decimal import Decimal
from core.options import EuropeanOption, AmericanOption, OptionType
from models.binomial import binomial_option_pricing
from portfolio.portfolio import Portfolio, Position

class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.call_eur = EuropeanOption(
            option_type=OptionType.CALL,
            spot=Decimal("100"),
            strike=Decimal("100"),
            maturity=Decimal("1"),
            volatility=Decimal("0.2"),
            rate=Decimal("0.05")
        )
        self.put_amer = AmericanOption(
            option_type=OptionType.PUT,
            spot=Decimal("100"),
            strike=Decimal("105"),
            maturity=Decimal("1"),
            volatility=Decimal("0.25"),
            rate=Decimal("0.05")
        )
        self.portfolio = Portfolio(pricing_model=binomial_option_pricing)
        self.portfolio.add_position(Position(self.call_eur, quantity=10))
        self.portfolio.add_position(Position(self.put_amer, quantity=5))

    def test_total_value(self):
        value = self.portfolio.total_value(spot=Decimal("100"), pricing_model=binomial_option_pricing)
        self.assertGreater(value, 0)

    def test_summary_runs(self):
        # This test only checks if the summary method runs without errors (not the output)
        self.portfolio.summary(spot=Decimal("100"), pricing_model=binomial_option_pricing)
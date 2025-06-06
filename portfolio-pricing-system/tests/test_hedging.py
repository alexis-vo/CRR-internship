import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from decimal import Decimal
from core.options import EuropeanOption, OptionType
from models.binomial import binomial_option_pricing
from portfolio.portfolio import Portfolio, Position
from portfolio.hedging import HedgingStrategy

class TestHedging(unittest.TestCase):
    def setUp(self):
        self.option = EuropeanOption(
            option_type=OptionType.CALL,
            spot=Decimal("100"),
            strike=Decimal("100"),
            maturity=Decimal("1"),
            volatility=Decimal("0.2"),
            rate=Decimal("0.05")
        )
        self.portfolio = Portfolio()
        self.portfolio.add_position(Position(self.option, quantity=1))
        self.hedger = HedgingStrategy(self.portfolio)

    def test_delta_computation(self):
        delta = self.hedger.compute_delta(self.option)
        self.assertIsInstance(delta, Decimal)
        self.assertTrue(-1 <= float(delta) <= 1)  # Delta borné pour les options

    def test_hedge_output(self):
        # Check if the hedge_delta method runs without errors
        self.hedger.hedge_delta()
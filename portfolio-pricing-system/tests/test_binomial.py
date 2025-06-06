import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from decimal import Decimal
from core.options import OptionType, OptionOrigin, Option
from core.options import EuropeanOption, AmericanOption, ExoticOption, BarrierOption
from models.binomial import binomial_option_pricing

class TestBinomialModel(unittest.TestCase):
    def setUp(self):
        self.call_euro = EuropeanOption(
            option_type=OptionType.CALL,
            spot=Decimal("100"),
            strike=Decimal("100"),
            maturity=Decimal("1"),
            volatility=Decimal("0.2"),
            rate=Decimal("0.05")
        )
        self.call_amer = AmericanOption(
            option_type=OptionType.CALL,
            spot=Decimal("100"),
            strike=Decimal("100"),
            maturity=Decimal("1"),
            volatility=Decimal("0.2"),
            rate=Decimal("0.05")
        )
        self.put_euro = EuropeanOption(
            option_type=OptionType.PUT,
            spot=Decimal("100"),
            strike=Decimal("100"),
            maturity=Decimal("1"),
            volatility=Decimal("0.2"),
            rate=Decimal("0.05")
        )
        self.put_amer = AmericanOption(
            option_type=OptionType.PUT,
            spot=Decimal("100"),
            strike=Decimal("100"),
            maturity=Decimal("1"),
            volatility=Decimal("0.2"),
            rate=Decimal("0.05")
        )
        self.put_bar = BarrierOption(
            option_type=OptionType.PUT,
            spot=Decimal("100"),
            strike=Decimal("100"),
            maturity=Decimal("1"),
            volatility=Decimal("0.2"),
            rate=Decimal("0.05"),
            barrier_level=Decimal("90")  # spot = 100 > 90, donc put barré KO si spot > bar
        )

    def test_european_call_value(self):
        value = binomial_option_pricing(self.call_euro, steps=100)
        self.assertAlmostEqual(float(value), 10.45, places=1)

    def test_american_call_value(self):
        value = binomial_option_pricing(self.call_amer, steps=100)
        self.assertGreaterEqual(value, binomial_option_pricing(self.call_euro, steps=100))

    def test_american_put_value(self):
        value = binomial_option_pricing(self.put_amer, steps=100)
        self.assertTrue(value > Decimal("5.5"))
    
    def test_european_put_value(self):
        value = binomial_option_pricing(self.put_euro, steps=100)
        self.assertAlmostEqual(float(value), 5.57, places=1)

if __name__ == '__main__':
    unittest.main()

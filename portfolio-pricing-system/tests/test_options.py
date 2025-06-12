import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from decimal import Decimal
from core.options import OptionType, EuropeanOption, AmericanOption, ExoticOption, BarrierOption

class TestOptions(unittest.TestCase):
    def setUp(self):
        self.spot = Decimal('100')
        self.strike = Decimal('100')
        self.maturity = Decimal('1')
        self.volatility = Decimal('0.2')
        self.rate = Decimal('0.05')
        self.barrier_level = Decimal("95")

    def test_european_option_call(self):
        option = EuropeanOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        self.assertEqual(option.payoff(Decimal('120')), Decimal('20'))
        self.assertEqual(option.payoff(Decimal('80')), Decimal('0'))

    def test_european_option_put(self):
        option = EuropeanOption(OptionType.PUT, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        self.assertEqual(option.payoff(Decimal('80')), Decimal('20'))
        self.assertEqual(option.payoff(Decimal('120')), Decimal('0'))

    def test_american_option_call(self):
        option = AmericanOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        self.assertEqual(option.payoff(Decimal('120')), Decimal('20'))
        self.assertEqual(option.payoff(Decimal('80')), Decimal('0'))

    def test_american_option_put(self):
        option = AmericanOption(OptionType.PUT, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        self.assertEqual(option.payoff(Decimal('80')), Decimal('20'))
        self.assertEqual(option.payoff(Decimal('120')), Decimal('0'))

    def test_exotic_option_call(self):
        option = ExoticOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        self.assertEqual(option.payoff(Decimal('120')), Decimal('20'))
        self.assertEqual(option.payoff(Decimal('80')), Decimal('0'))

    def test_exotic_option_put(self):
        option = ExoticOption(OptionType.PUT, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        self.assertEqual(option.payoff(Decimal('80')), Decimal('20'))
        self.assertEqual(option.payoff(Decimal('120')), Decimal('0'))

    def test_barrier_initialization(self):
        option = BarrierOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate, self.barrier_level)
        self.assertEqual(option.barrier_level, self.barrier_level)

        with self.assertRaises(ValueError):
            BarrierOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate, Decimal("-1"))

    def test_barrier_payoff_call_option(self):
        option = BarrierOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate, self.barrier_level)
        spot_above_barrier = Decimal("96")
        self.assertNotEqual(option.payoff(spot_above_barrier), Decimal("0"))

        spot_below_barrier = Decimal("94")
        self.assertEqual(option.payoff(spot_below_barrier), Decimal("0"))

    def test_barrier_payoff_put_option(self):
        option = BarrierOption(OptionType.PUT, self.spot, self.strike, self.maturity, self.volatility, self.rate, self.barrier_level)
        spot_below_barrier = Decimal("94")
        self.assertNotEqual(option.payoff(spot_below_barrier), Decimal("0"))

        spot_above_barrier = Decimal("96")
        self.assertEqual(option.payoff(spot_above_barrier), Decimal("0"))
    
if __name__ == '__main__':
    unittest.main()



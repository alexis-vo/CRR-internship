import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from decimal import Decimal
from core.options import OptionType, OptionOrigin, Option
from core.options import EuropeanOption, AmericanOption, ExoticOption, BarrierOption


class TestOptions(unittest.TestCase):
    def setUp(self):
        self.spot = Decimal('100')
        self.strike = Decimal('100')
        self.maturity = Decimal('1')
        self.volatility = Decimal('0.2')
        self.rate = Decimal('0.05')

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

    def test_barrier_option_call(self):
        barrier_level = Decimal('110')
        option = BarrierOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate, barrier_level)
        self.assertEqual(option.payoff(Decimal('120')), Decimal('20'))
        self.assertEqual(option.payoff(Decimal('100')), Decimal('0'))
        self.assertEqual(option.payoff(Decimal('90')), Decimal('0'))
        self.assertEqual(option.payoff(Decimal('110')), Decimal('0'))
        self.assertEqual(option.payoff(Decimal('130')), Decimal('30'))
    
    def test_barrier_option_put(self):
        barrier_level = Decimal('90')
        option = BarrierOption(OptionType.PUT, self.spot, self.strike, self.maturity, self.volatility, self.rate, barrier_level)
        self.assertEqual(option.payoff(Decimal('80')), Decimal('20'))
        self.assertEqual(option.payoff(Decimal('100')), Decimal('0'))
        self.assertEqual(option.payoff(Decimal('110')), Decimal('0'))
        self.assertEqual(option.payoff(Decimal('90')), Decimal('0'))
        self.assertEqual(option.payoff(Decimal('70')), Decimal('20'))
    
    def test_barrier_option_invalid_level(self):
        with self.assertRaises(ValueError):
            BarrierOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate, Decimal('0'))
    
    def test_option_origin(self):
        option = EuropeanOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        origin = option.origin()
        self.assertIn('eur', origin)
        self.assertNotIn('usa', origin)
        self.assertNotIn('exo', origin)
        self.assertNotIn('bar', origin)

        option = AmericanOption(OptionType.PUT, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        origin = option.origin()
        self.assertIn('usa', origin)
        self.assertNotIn('eur', origin)
        self.assertNotIn('exo', origin)
        self.assertNotIn('bar', origin)

        option = ExoticOption(OptionType.CALL, self.spot, self.strike, self.maturity, self.volatility, self.rate)
        origin = option.origin()
        self.assertIn('exo', origin)
        self.assertNotIn('eur', origin)
        self.assertNotIn('usa', origin)
        self.assertNotIn('bar', origin)

        option = BarrierOption(OptionType.PUT, self.spot, self.strike, self.maturity, self.volatility, self.rate, Decimal('110'))
        origin = option.origin()
        self.assertIn('bar', origin)
        self.assertNotIn('eur', origin)
        self.assertNotIn('usa', origin)
        self.assertNotIn('exo', origin)
    
if __name__ == '__main__':
    unittest.main()



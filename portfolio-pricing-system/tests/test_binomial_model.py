# Exemple de test pour binomial_model.py
import unittest
from decimal import Decimal
from core.options import EuropeanCall
from models.binomial_model import binomial_option_pricing

class TestBinomialModel(unittest.TestCase):
    def setUp(self):
        self.spot = Decimal('100')
        self.strike = Decimal('100')
        self.maturity = Decimal('1')
        self.volatility = Decimal('0.2')
        self.rate = Decimal('0.05')
        self.option = EuropeanCall(self.spot, self.strike, self.maturity, self.volatility, self.rate)

    def test_binomial_option_pricing(self):
        price = binomial_option_pricing(self.option, steps=3)
        self.assertAlmostEqual(price, Decimal('10.037'), places=3)

if __name__ == '__main__':
    unittest.main()

from decimal import Decimal, getcontext
from core.options import EuropeanCall, EuropeanPut
from models.binomial_model import binomial_option_pricing
from portfolio.portfolio import Portfolio

def get_context():
    getcontext().prec = 8 # Précision pour les calculs décimaux
    spot = Decimal('100.0')
    strike_call = Decimal('100.0')
    strike_put = Decimal('95.0')
    maturity = Decimal('1.0')
    volatility = Decimal('0.2')
    rate = Decimal('0.05')
    steps = 3
    return spot, strike_call, strike_put, maturity, volatility, rate, steps

def print_context(spot, strike_call, strike_put, maturity, volatility, rate, steps):
    print(f"Spot : {spot:.4f} €")
    print(f"Strike Call : {strike_call:.4f} €")
    print(f"Strike Put : {strike_put:.4f} €")
    print(f"Maturité : {maturity:.4f} an(s)")
    print(f"Volatilité : {volatility:.4f}")
    print(f"Taux d'intérêt : {rate:.4f}")
    print(f"Pas de temps : {steps}")

def main():
    spot, strike_call, strike_put, maturity, volatility, rate, steps = get_context()
    print_context(spot, strike_call, strike_put, maturity, volatility, rate, steps)

    # Création des options
    call = EuropeanCall(spot, strike_call, maturity, volatility, rate)
    put = EuropeanPut(spot, strike_put, maturity, volatility, rate)

    # Calcul des prix des options
    call_price = binomial_option_pricing(option=call, steps=steps)
    put_price = binomial_option_pricing(option=put, steps=steps)

    print(f"Valeur du call européen : {call_price:.4f} €")
    print(f"Valeur du put européen : {put_price:.4f} €")

    # Création et affichage du portefeuille
    p = Portfolio()
    p.add_position("Call Européen", 1, float(call_price))
    p.add_position("Put Européen", 1, float(put_price))
    p.add_position("Action XYZ", 100, 98.5)  # Exemple d'une position en actions
    p.add_position("Cash", 1, 1000.0)  # Exemple d'une position en cash
    p.summary()

if __name__ == "__main__":
    main()

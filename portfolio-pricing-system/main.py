from decimal import Decimal
from core.options import EuropeanOption, AmericanOption, OptionType
from models.binomial import binomial_option_pricing
from portfolio.portfolio import Portfolio, Position
from portfolio.hedging import HedgingStrategy
from utils.visualization import plot_hedging_deltas, plot_portfolio_values_over_time, plot_binomial_tree

def display_option_data(option, quantity):
    print(f"- {option.option_type.name} ({'American' if isinstance(option, AmericanOption) else 'European'}) x{quantity}")
    print(f"  Spot     : {option.spot}")
    print(f"  Strike   : {option.strike}")
    print(f"  Maturity : {option.maturity}")
    print(f"  Volatility: {option.volatility}")
    print(f"  Rate     : {option.rate}")
    print("")

def example_of_portfolio_with_crr_model():
    call_eur = EuropeanOption(
        option_type=OptionType.CALL,
        spot=Decimal("100"),
        strike=Decimal("100"),
        maturity=Decimal("1"),
        volatility=Decimal("0.2"),
        rate=Decimal("0.05")
    )

    put_amer = AmericanOption(
        option_type=OptionType.PUT,
        spot=Decimal("100"),
        strike=Decimal("105"),
        maturity=Decimal("1"),
        volatility=Decimal("0.25"),
        rate=Decimal("0.05")
    )

    # Build the portfolio
    portfolio = Portfolio(pricing_model=binomial_option_pricing)
    portfolio.add_position(call_eur, quantity=10)
    portfolio.add_position(put_amer, quantity=5)

    spot = Decimal("100")

    print("=== Initial Option Data ===")
    for pos in portfolio.positions:
        display_option_data(pos.option, pos.quantity)

    print("=== Individual Option Prices ===")
    for pos in portfolio.positions:
        price = binomial_option_pricing(pos.option)
        print(f"- {pos.option.option_type.name} ({'American' if isinstance(pos.option, AmericanOption) else 'European'}) x{pos.quantity}: {price:.4f}")

    # Total portfolio value
    total_value = portfolio.total_value()
    print(f"\n=== Total Portfolio Value ===\n${total_value:.4f}")

    # Delta hedging
    hedger = HedgingStrategy(portfolio)
    print("\n=== Delta of Each Option ===")
    for pos in portfolio.positions:
        delta = hedger.compute_delta(pos.option)
        print(f"- {pos.option.option_type.name} ({'American' if isinstance(pos.option, AmericanOption) else 'European'}): Δ = {delta:.4f}")

    print("\n=== Recommended Delta Hedge ===")
    hedger.hedge_delta()

def example_of_visualization():
    my_option = EuropeanOption(
        option_type=OptionType.CALL,
        spot=Decimal("100"),
        strike=Decimal("100"),
        maturity=Decimal("1"),
        volatility=Decimal("0.2"),
        rate=Decimal("0.05")
    )
    price, tree = binomial_option_pricing(my_option, steps=5, return_tree=True)
    # plot_binomial_tree(tree)

    portfolio_values = [100, 105, 102, 107, 110]
    plot_portfolio_values_over_time(portfolio_values)

    deltas = {
        "Option A": [0.2, 0.3, 0.4, 0.35, 0.25],
        "Option B": [-0.1, -0.05, 0.0, 0.05, 0.1]
    }
    plot_hedging_deltas(deltas)

def main():
    # example_of_portfolio_with_crr_model()
    example_of_visualization()

if __name__ == "__main__":
    main()
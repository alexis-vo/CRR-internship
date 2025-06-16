from decimal import Decimal, localcontext
from math import exp, sqrt
from core.options import AmericanOption
from graphviz import Digraph


def binomial_option_pricing(option, spot=None, steps=3, return_tree=False, visualize_g=False, visualize_t=False, filename="option_tree"):
    spot = option.spot
    with localcontext() as ctx:
        ctx.prec = 28

        dt = option.maturity / Decimal(steps)
        u = Decimal(exp(float(option.volatility) * sqrt(float(dt))))
        d = Decimal(1) / u
        R = Decimal(exp(float(option.rate) * float(dt)))
        discount = Decimal(1) / R
        p = (R - d) / (u - d)

        if not (Decimal(0) <= p <= Decimal(1)):
            raise ValueError("Invalid risk-neutral probability p. Check input parameters.")

        price_tree = [[Decimal(0) for _ in range(i + 1)] for i in range(steps + 1)]
        option_tree = [[Decimal(0) for _ in range(i + 1)] for i in range(steps + 1)]
        exercise_tree = [[False for _ in range(i + 1)] for i in range(steps + 1)]

        for t in range(steps + 1):
            for i in range(t + 1):
                price_tree[t][i] = spot * (u ** i) * (d ** (t - i))

        for i in range(steps + 1):
            S = price_tree[steps][i]
            option_tree[steps][i] = option.payoff(S)

        for t in reversed(range(steps)):
            for i in range(t + 1):
                continuation = discount * (p * option_tree[t + 1][i + 1] + (1 - p) * option_tree[t + 1][i])
                S = price_tree[t][i]

                if isinstance(option, AmericanOption):
                    exercise = option.payoff(S)
                    if exercise > continuation:
                        option_tree[t][i] = exercise
                        exercise_tree[t][i] = True
                    else:
                        option_tree[t][i] = continuation
                else:
                    option_tree[t][i] = continuation

        if visualize_t:
            # Print the price tree
            for t in range(steps + 1):
                level = "" * (steps - t) * 4  # Adjust indentation for visual representation
                for i in range(t + 1):
                    level += f"{price_tree[t][i]:.2f} "
                print(level)

            print()

            # Print the option tree
            for t in range(steps + 1):
                level = "" * (steps - t) * 4  # Adjust indentation for visual representation
                for i in range(t + 1):
                    level += f"{option_tree[t][i]:.2f} "
                print(level)

        if visualize_g:
            #TODO
            pass

        return (option_tree[0][0], option_tree) if return_tree else option_tree[0][0]
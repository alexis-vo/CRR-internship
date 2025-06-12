from decimal import Decimal, localcontext
from math import exp, sqrt
from core.options import AmericanOption


def binomial_option_pricing(option, steps=1000, return_tree=False):
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

        option_tree = [[Decimal(0) for _ in range(i + 1)] for i in range(steps + 1)]

        # Terminal nodes
        for i in range(steps + 1):
            S = option.spot * (u ** i) * (d ** (steps - i))
            option_tree[steps][i] = option.payoff(S)

        # Backward induction
        for t in reversed(range(steps)):
            for i in range(t + 1):
                continuation = discount * (p * option_tree[t + 1][i + 1] + (1 - p) * option_tree[t + 1][i])
                if isinstance(option, AmericanOption):
                    S = option.spot * (u ** i) * (d ** (t - i))
                    exercise = option.payoff(S)
                    option_tree[t][i] = max(continuation, exercise)
                else:
                    option_tree[t][i] = continuation

        return (option_tree[0][0], option_tree) if return_tree else option_tree[0][0]
from decimal import Decimal, getcontext
from math import exp, sqrt

def binomial_option_pricing(option, steps=100, return_tree=False):
    getcontext().prec = 28

    dt = Decimal(option.maturity) / Decimal(steps)
    u = Decimal(exp(option.volatility * (dt ** Decimal(0.5))))
    d = Decimal(1) / u
    R = Decimal(exp(option.rate * dt))
    discount = Decimal(1) / R
    p = (R - d) / (u - d)

    # Initialisation de l'arbre
    option_tree = [[Decimal(0) for _ in range(i + 1)] for i in range(steps + 1)]

    # Valeur terminale
    for i in range(steps + 1):
        S = option.spot * (u ** i) * (d ** (steps - i))
        option_tree[steps][i] = option.payoff(S)

    # Backward
    for t in reversed(range(steps)):
        for i in range(t + 1):
            continuation = discount * (p * option_tree[t + 1][i + 1] + (1 - p) * option_tree[t + 1][i])
            if hasattr(option, "is_american") and option.is_american:
                S = option.spot * (u ** i) * (d ** (t - i))
                exercise = option.payoff(S)
                option_tree[t][i] = max(continuation, exercise)
            else:
                option_tree[t][i] = continuation

    return (option_tree[0][0], option_tree) if return_tree else option_tree[0][0]

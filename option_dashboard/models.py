# le code n'est pas bien structuré mais reste fonctionnel
# je le factoriserai prochainement... 
# je me suis cependant efforcé de commenter le code pour que ce soit assez clair
# de plus j'essaie de respecter les normes de la PEP
# je détaillerai davantage les algos à chaque relecture

import numpy as np
from scipy.stats import norm

# fonction de pricing pour B-S
def price_bs(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# fonction de pricing pour CRR
def price_crr(S, K, T, r, sigma, N, option_type="call"):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Arbre des prix
    prices = np.zeros(N + 1)
    for i in range(N + 1):
        prices[i] = S * (u ** (N - i)) * (d ** i)

    # Valeurs à maturité
    if option_type == "call":
        values = np.maximum(prices - K, 0)
    else:
        values = np.maximum(K - prices, 0)

    # Remonter l'arbre = backward induction
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            values[j] = np.exp(-r * dt) * (p * values[j] + (1 - p) * values[j + 1])

    return values[0]

# fonction de pricing pour Bachelier
def price_bachelier(S, K, T, r, sigma, option_type="call"):
    sigma_hat = sigma * S  # Échelle absolue
    d = (S - K) / (sigma_hat * np.sqrt(T))
    discount = np.exp(-r * T)
    if option_type == "call":
        return discount * ((S - K) * norm.cdf(d) + sigma_hat * np.sqrt(T) * norm.pdf(d))
    else:
        return discount * ((K - S) * norm.cdf(-d) + sigma_hat * np.sqrt(T) * norm.pdf(d))
    
def delta_bs(S, K, T, r, sigma, option_type="call"):
    from scipy.stats import norm
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    if option_type == "call":
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1

# j'écris une fonction pour Monte-Carlo plus tard dans le code...


# bien sûr on n'oublie pas les greeks (et oui pour voir les risques que je prends)
# je pense écrire un cours dessus pour que la théorie soit bien claire
def greeks_bs(S, K, T, r, sigma, option_type="call"):
    from scipy.stats import norm

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    delta = norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta_call = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                  - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    theta = theta_call if option_type == "call" else theta_put
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
    rho = rho_call if option_type == "call" else rho_put

    return {
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega,
        "Theta": theta,
        "Rho": rho
    }

def prob_profit_bs(S, K_low, K_high, T, r, sigma):
    """
    Approxime la proba que le prix spot à maturité soit entre K_low et K_high.
    Pour une stratégie rentable dans [K_low, K_high].
    """
    mu = np.log(S) + (r - 0.5 * sigma**2) * T
    sigma_adj = sigma * np.sqrt(T)

    # Cas borne inf
    if K_low == 0:
        prob = norm.cdf((np.log(K_high) - mu) / sigma_adj)
    elif np.isinf(K_high):
        prob = 1 - norm.cdf((np.log(K_low) - mu) / sigma_adj)
    else:
        prob = norm.cdf((np.log(K_high) - mu) / sigma_adj) - norm.cdf((np.log(K_low) - mu) / sigma_adj)

    return prob

# comme promis plus haut, la voici donc la fonction de Monte-Carlo
def monte_carlo_strategy(
    S0, T, r, sigma, N, strategy, params
):
    """
    Simule le PnL à maturité pour une stratégie donnée.

    strategy: "straddle", "bull_call", "iron_condor"
    params: dictionnaire contenant strike(s)
    """
    np.random.seed(42)
    Z = np.random.randn(N)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    PnLs = np.zeros(N)

    if strategy == "straddle":
        K = params["K"]
        payoff = np.maximum(ST - K, 0) + np.maximum(K - ST, 0)
        cost = price_bs(S0, K, T, r, sigma, "call") + price_bs(S0, K, T, r, sigma, "put")

    elif strategy == "bull_call":
        K1, K2 = params["K1"], params["K2"]
        payoff = np.maximum(ST - K1, 0) - np.maximum(ST - K2, 0)
        cost = price_bs(S0, K1, T, r, sigma, "call") - price_bs(S0, K2, T, r, sigma, "call")

    elif strategy == "iron_condor":
        K1, K2, K3, K4 = params["K1"], params["K2"], params["K3"], params["K4"]
        payoff = (
            np.maximum(K2 - ST, 0) - np.maximum(K1 - ST, 0)
            + np.maximum(ST - K3, 0) - np.maximum(ST - K4, 0)
        )
        cost = (
            price_bs(S0, K1, T, r, sigma, "put") - price_bs(S0, K2, T, r, sigma, "put")
            + price_bs(S0, K4, T, r, sigma, "call") - price_bs(S0, K3, T, r, sigma, "call")
        )

    else:
        raise ValueError("Stratégie inconnue")

    PnLs = payoff - cost
    return ST, PnLs


def hedging_simulation(S0, K, T, r, sigma, N, option_type="call"):
    """
    Simule la couverture dynamique d'une option européenne avec hedging par le delta BS.

    Renvoie :
    - le chemin des S
    - la position delta à chaque pas
    - la valeur du portefeuille couvert
    - le PnL final vs payoff
    """
    dt = T / N
    np.random.seed(42)

    # Simuler un chemin du sous-jacent
    Z = np.random.randn(N)
    S_path = np.zeros(N + 1)
    S_path[0] = S0
    for t in range(1, N + 1):
        S_path[t] = S_path[t - 1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[t - 1])

    # Initialisation
    portfolio = np.zeros(N + 1)
    deltas = np.zeros(N + 1)
    cash = 0

    for t in range(N):
        time_to_maturity = T - t * dt
        S_t = S_path[t]

        # Calcul du delta
        d1 = (np.log(S_t / K) + (r + 0.5 * sigma**2) * time_to_maturity) / (sigma * np.sqrt(time_to_maturity))
        delta = norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1
        deltas[t] = delta

        if t == 0:
            # Achat initial de l’option
            option_price = price_bs(S_t, K, time_to_maturity, r, sigma, option_type)
            cash = option_price - delta * S_t
        else:
            delta_change = delta - deltas[t - 1]
            cash -= delta_change * S_t

        # Mise à jour avec intérêts
        cash *= np.exp(r * dt)
        portfolio[t] = cash + delta * S_t

    # Dernier delta inutile, mais pour la forme
    deltas[-1] = deltas[-2]
    portfolio[-1] = cash + deltas[-1] * S_path[-1]

    # Payoff réel de l'option
    if option_type == "call":
        payoff = max(S_path[-1] - K, 0)
    else:
        payoff = max(K - S_path[-1], 0)

    pnl = portfolio[-1] - payoff
    return S_path, portfolio, deltas, pnl, payoff


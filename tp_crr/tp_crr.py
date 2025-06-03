"""
TP sur le modèle binomial de Cox-Ross-Rubinstein (CRR) - MAP 552
"""
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Prix initial de l'actif
S0 = 100

# (1a) Fonction Sn : prix des actifs à la date j
def Sn(T, n, mu, sigma, j):
    """
    Calcule les prix des actifs à la date j.
    T : maturité
    n : nombre de pas
    mu : drift
    sigma : volatilité
    j : date à laquelle on veut les prix
    @return : tableau des prix des actifs à la date j
    """
    h = T / n # durée d'une période
    u = np.exp(mu * h + sigma * np.sqrt(h))
    d = np.exp(mu * h - sigma * np.sqrt(h))
    return np.array([S0 * u**(j - i) * d**i for i in range(j + 1)])

# (1b) Payoff d'une option call européenne à maturité
def Payoff(T, n, mu, sigma, K):
    """
    Calcule le payoff d'une option call européenne à maturité.
    T : maturité
    n : nombre de pas
    mu : drift
    sigma : volatilité
    K : prix d'exercice
    @return : tableau des payoffs à maturité
    """
    prices = Sn(T, n, mu, sigma, n)
    return np.maximum(prices - K, 0)

# (1c) Prix de l'option à la date 0 avec évaluation backward
def Calln(T, n, r, mu, sigma, K):
    """
    Calcule le prix d'une option call européenne à la date 0
    T : maturité
    n : nombre de pas
    r : taux d'intérêt sans risque
    mu : drift
    sigma : volatilité
    K : prix d'exercice
    @return : prix de l'option call à la date 0
    """
    h = T / n
    u = np.exp(mu * h + sigma * np.sqrt(h))
    d = np.exp(mu * h - sigma * np.sqrt(h))

    # Probabilité risque neutre
    q = (np.exp(r * h) - d) / (u - d)

    # Initialisation à la maturité
    V = Payoff(T, n, mu, sigma, K)
    
    # Backward induction
    for j in range(n - 1, -1, -1):
        V = np.exp(-r * h) * (q * V[:-1] + (1 - q) * V[1:])

    return V[0]

# (1d) Calcul du vecteur de stratégie de couverture à la date j
def Deltan(T, n, r, mu, sigma, K, j):
    h = T / n
    u = np.exp(mu * h + sigma * np.sqrt(h))
    d = np.exp(mu * h - sigma * np.sqrt(h))
    q = (np.exp(r * h) - d) / (u - d)

    # Initialisation à la maturité
    V = [Payoff(T, n, mu, sigma, K)]

    # Backward jusqu'à j+1 (pour obtenir V_{j+1})
    for k in range(n, j + 1, -1):
        V_k = np.exp(-r * h) * (q * V[0][:-1] + (1 - q) * V[0][1:])
        V = [V_k] + V

    if len(V[0]) < 2:
        return np.array([])  # Pas assez d'éléments pour calculer un delta

    # Valeurs de l'actif aux noeuds à j+1
    Sj1 = Sn(T, n, mu, sigma, j + 1)

    V_up = V[0][:-1]
    V_down = V[0][1:]
    delta = (V_up - V_down) / (Sj1[:-1] - Sj1[1:])
    return delta

# (1e) Étude numérique
def plot_Calln_Deltan_vs_K():
    """
    Étude numérique du prix de l'option Calln
    et du delta à j=0 en fonction de K.
    """
    K_vals = np.arange(80, 121)
    prices = []
    deltas = []

    for K in K_vals:
        prices.append(Calln(2, 50, 0.05, 0.1, 0.3, K))
        delta_vec = Deltan(2, 50, 0.05, 0.1, 0.3, K, 0)
        deltas.append(delta_vec[0])  # delta à j=0

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(K_vals, prices)
    plt.title("Prix de l'option Call vs Strike")
    plt.xlabel("K")
    plt.ylabel("Calln")

    plt.subplot(1, 2, 2)
    plt.plot(K_vals, deltas)
    plt.title("Delta à j=0 vs Strike")
    plt.xlabel("K")
    plt.ylabel("Delta0")

    plt.tight_layout()
    plt.show()

# (2a) Formule de Black-Scholes
def Call(T, r, sigma, K):
    """
    Calcule le prix d'une option call européenne
    selon la formule de Black-Scholes.
    T : maturité
    r : taux d'intérêt sans risque
    sigma : volatilité
    K : prix d'exercice
    @return : prix de l'option call
    """
    d1 = (np.log(S0 / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# (2b) Erreur relative entre CRR et Black-Scholes
def error_vs_n(T, r, mu, sigma, K):
    """
    Étudie l'erreur relative entre le prix CRR et le prix Black-Scholes
    en fonction du nombre de périodes n.
    T : maturité
    r : taux d'intérêt sans risque
    mu : drift
    sigma : volatilité
    K : prix d'exercice
    """
    n_vals = np.arange(1, 200)
    bs_price = Call(T, r, sigma, K)
    errors = []

    # Calcul des prix CRR pour chaque n
    for n in n_vals:
        binomial_price = Calln(T, n, r, mu, sigma, K)
        error = binomial_price / bs_price - 1
        errors.append(error)

    plt.plot(n_vals, errors)
    plt.title("Erreur relative CRR / Black-Scholes")
    plt.xlabel("n (nombre de périodes)")
    plt.ylabel("Erreur relative")
    plt.grid(True)
    plt.show()

# Exécution des études demandées
if __name__ == "__main__":
    print("Prix Calln:", Calln(2, 50, 0.05, 0.1, 0.3, 100))
    delta_0 = Deltan(2, 50, 0.05, 0.1, 0.3, 100, 0)

    if delta_0.size > 0:
        print("Delta à j=0:", delta_0[0])
    else:
        print("Erreur : aucun delta calculable à j=0.")
    
    print("Sn j=0 :", Sn(2, 50, 0.1, 0.3, 0))     # Devrait retourner [100]
    print("Sn j=1 :", Sn(2, 50, 0.1, 0.3, 1))     # Devrait retourner [S_up, S_down]

    plot_Calln_Deltan_vs_K()
    error_vs_n(T=2, r=0.05, mu=0.1, sigma=0.3, K=105)
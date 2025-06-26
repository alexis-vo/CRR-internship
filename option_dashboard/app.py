# la partie streamlit esthétique qui rend le projet sexy
# (plus que dans un terminal eh oui)

# TODO : pour la partie police d'écriture, trop petite il faut revoir ça dans un second temps
# c'est un premier jet après beaucoup de tentatives en local
# aucun test n'a été fait, c'est la prochaine étape à suivre...

import streamlit as st
from models import price_bs, price_crr, price_bachelier, delta_bs, greeks_bs, prob_profit_bs, monte_carlo_strategy, hedging_simulation
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="Dashboard Options", layout="wide")
st.title("📊 Dashboard - Modèles de Pricing d'Options Vanille 🍦")

with st.sidebar:
    st.header("Paramètres ⚙️")
    S = st.number_input("Prix spot (S)", value=100.0)
    K = st.number_input("Strike (K)", value=100.0)
    T = st.number_input("Maturité (T, en années)", value=1.0, min_value=0.01)
    r = st.number_input("Taux sans risque (r)", value=0.05)
    sigma = st.number_input("Volatilité (sigma)", value=0.2)
    N = st.slider("Nombre d'étapes (CRR)", 10, 500, 50)
    option_type = st.selectbox("Type d'option", ["call", "put"])

st.subheader("💰 Prix calculés")

col1, col2, col3 = st.columns(3) # TODO rajouter monte-carlo / voire supprimer Bachelier ? à réfléchir...

with col1:
    st.markdown("### Black-Scholes")
    bs_price = price_bs(S, K, T, r, sigma, option_type)
    st.metric(label="Prix BS", value=f"{bs_price:.2f}")

with col2:
    st.markdown("### Cox-Ross-Rubinstein")
    crr_price = price_crr(S, K, T, r, sigma, N, option_type)
    st.metric(label="Prix CRR", value=f"{crr_price:.2f}")

with col3:

    st.markdown("### Bachelier")
    bachelier_price = price_bachelier(S, K, T, r, sigma, option_type)
    st.metric(label="Prix Bachelier", value=f"{bachelier_price:.2f}")

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Payoff & Convergence", "🛡️ Hedging (Delta)", "🇬🇷 Greeks", "📦 Stratégies", "🧪 Simulation Monte Carlo du PnL", "💯 Récap'"])

with tab1:
    st.subheader("Courbes de payoff & convergence")
    S_range = np.linspace(0.5 * K, 1.5 * K, 100)
    payoff = np.maximum(S_range - K, 0) if option_type == "call" else np.maximum(K - S_range, 0)

    fig_payoff = go.Figure()
    fig_payoff.add_trace(go.Scatter(x=S_range, y=payoff, mode='lines', name='Payoff'))
    fig_payoff.update_layout(title="Payoff à maturité", xaxis_title="Prix spot", yaxis_title="Profit")
    st.plotly_chart(fig_payoff, use_container_width=True, key="payoff_chart")
    N_range = np.arange(10, 200, 10)
    crr_prices = [price_crr(S, K, T, r, sigma, n, option_type) for n in N_range]
    bs_ref = price_bs(S, K, T, r, sigma, option_type)

    fig_conv = go.Figure()
    fig_conv.add_trace(go.Scatter(x=N_range, y=crr_prices, mode='lines+markers', name='Prix CRR'))
    fig_conv.add_trace(go.Scatter(x=N_range, y=[bs_ref]*len(N_range), mode='lines', name='Prix BS (réf)', line=dict(dash='dash')))
    fig_conv.update_layout(title="Convergence CRR vers BS", xaxis_title="Nombre d'étapes N", yaxis_title="Prix")
    st.plotly_chart(fig_conv, use_container_width=True, key="convergence_chart")

with tab2:
    st.subheader("🛡️ Couverture dynamique d'une option")

    hedge_N = st.slider("Nombre de pas pour le hedge (N)", 10, 200, 50, key="hedge_n")
    S_path, portfolio, deltas, pnl, payoff = hedging_simulation(S, K, T, r, sigma, hedge_N, option_type)

    st.success(f"💼 Résultat de la couverture : PnL = `{pnl:.2f}`, Payoff option = `{payoff:.2f}`")

    # Tracé prix et portefeuille
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(y=S_path, mode="lines", name="Prix sous-jacent"))
    fig1.add_trace(go.Scatter(y=portfolio, mode="lines", name="Valeur portefeuille"))
    fig1.update_layout(title="Évolution du prix et du portefeuille couvert", xaxis_title="Temps", yaxis_title="Valeur")
    st.plotly_chart(fig1, use_container_width=True)

    # Tracé delta
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=deltas, mode="lines", name="Delta (BS)"))
    fig2.update_layout(title="Delta à chaque pas (BS)", xaxis_title="Temps", yaxis_title="Delta")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("📐 Greeks - Modèle Black-Scholes")

    greeks = greeks_bs(S, K, T, r, sigma, option_type)
    greeks = {k: round(v, 4) for k, v in greeks.items()}

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5 = st.columns(1)[0]

    with col1:
        st.metric("Delta", value=greeks["Delta"])
    with col2:
        st.metric("Gamma", value=greeks["Gamma"])
    with col3:
        st.metric("Vega", value=greeks["Vega"])
    with col4:
        st.metric("Theta (par jour)", value=greeks["Theta"])
    with col5:
        st.metric("Rho", value=greeks["Rho"])

    st.subheader("📊 Courbes des Greeks en fonction de S")

    S_range = np.linspace(0.5 * K, 1.5 * K, 100)
    greek_data = {g: [] for g in ["Delta", "Gamma", "Vega", "Theta", "Rho"]}

    for s in S_range:
        g = greeks_bs(s, K, T, r, sigma, option_type)
        for key in greek_data:
            greek_data[key].append(g[key])


    param_to_vary = st.selectbox(
    "Paramètre à faire varier pour visualiser les Greeks :",
    ["Prix spot (S)", "Temps à maturité (T)", "Volatilité (σ)"]
    )

    greek_data = {g: [] for g in ["Delta", "Gamma", "Vega", "Theta", "Rho"]}

    if param_to_vary == "Prix spot (S)":
        x_range = np.linspace(0.5 * K, 1.5 * K, 100)
        x_label = "Prix spot (S)"
        for s in x_range:
            g = greeks_bs(s, K, T, r, sigma, option_type)
            for key in greek_data:
                greek_data[key].append(g[key])

    elif param_to_vary == "Temps à maturité (T)":
        x_range = np.linspace(0.01, 2.0, 100)  # de 0.01 à 2 ans
        x_label = "Temps à maturité (T)"
        for t in x_range:
            g = greeks_bs(S, K, t, r, sigma, option_type)
            for key in greek_data:
                greek_data[key].append(g[key])

    elif param_to_vary == "Volatilité (σ)":
        x_range = np.linspace(0.01, 1.0, 100)  # de 1% à 100%
        x_label = "Volatilité (σ)"
        for vol in x_range:
            g = greeks_bs(S, K, T, r, vol, option_type)
            for key in greek_data:
                greek_data[key].append(g[key])

    # Fonction pour tracer un graphique
    def plot_greek(name):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_range, y=greek_data[name], mode="lines", name=name))
        fig.update_layout(title=f"{name} en fonction de {x_label}", xaxis_title=x_label, yaxis_title=name)
        st.plotly_chart(fig, use_container_width=True, key=f"{name}_{param_to_vary}")

    # Affichage en 2 colonnes
    col1, col2 = st.columns(2)

    with col1:
        plot_greek("Delta")
        plot_greek("Gamma")
        plot_greek("Vega")

    with col2:
        plot_greek("Theta")
        plot_greek("Rho")

with tab4:
    st.subheader("📦 Visualisation de stratégies d’options")

    strategy = st.selectbox("Choisir une stratégie :", ["Straddle", "Bull Call Spread", "Iron Condor"])
    params = {}

    if strategy == "Straddle":
        stgy_key = "straddle"
        strike = st.number_input("Strike (K)", value=K, key="straddle_strike")
        params["K"] = strike
    elif strategy == "Bull Call Spread":
        stgy_key = "bull_call"
        K1 = st.number_input("Strike K1 (long call)", value=K - 10.0, key="bull_k1")
        K2 = st.number_input("Strike K2 (short call)", value=K + 10.0, key="bull_k2")
        params.update({"K1": K1, "K2": K2})
    elif strategy == "Iron Condor":
        stgy_key = "iron_condor"
        K1 = st.number_input("Put Long (K1)", value=K - 20.0, key="ic_k1")
        K2 = st.number_input("Put Short (K2)", value=K - 10.0, key="ic_k2")
        K3 = st.number_input("Call Short (K3)", value=K + 10.0, key="ic_k3")
        K4 = st.number_input("Call Long (K4)", value=K + 20.0, key="ic_k4")
        params.update({"K1": K1, "K2": K2, "K3": K3, "K4": K4})
    
    S_range = np.linspace(0.5 * K, 1.5 * K, 300)
    payoff = np.zeros_like(S_range)

    if strategy == "Straddle":
        payoff = np.maximum(S_range - strike, 0) + np.maximum(strike - S_range, 0)
        cost = price_bs(S, strike, T, r, sigma, "call") + price_bs(S, strike, T, r, sigma, "put")

    elif strategy == "Bull Call Spread":
        payoff = np.maximum(S_range - K1, 0) - np.maximum(S_range - K2, 0)
        cost = price_bs(S, K1, T, r, sigma, "call") - price_bs(S, K2, T, r, sigma, "call")

    elif strategy == "Iron Condor":
        payoff = (
            np.maximum(K2 - S_range, 0) - np.maximum(K1 - S_range, 0)  # Put short - Put long
            + np.maximum(S_range - K3, 0) - np.maximum(S_range - K4, 0)  # Call short - Call long
        )
        cost = (
            price_bs(S, K1, T, r, sigma, "put") - price_bs(S, K2, T, r, sigma, "put")
            + price_bs(S, K4, T, r, sigma, "call") - price_bs(S, K3, T, r, sigma, "call")
        )

    net_payoff = payoff - cost

    # Calcul probabilité de profit (approximative)
    if strategy == "Straddle":
        K_low = 0
        K_high = strike - cost  # côté put
        prob_left = prob_profit_bs(S, 0, K_high, T, r, sigma)

        K_low2 = strike + cost
        K_high2 = np.inf
        prob_right = prob_profit_bs(S, K_low2, np.inf, T, r, sigma)

        prob_profit = prob_left + prob_right

    elif strategy == "Bull Call Spread":
        prob_profit = prob_profit_bs(S, K1 + cost, K2, T, r, sigma)

    elif strategy == "Iron Condor":
        prob_profit = prob_profit_bs(S, K2, K3, T, r, sigma)

    st.success(f"📊 Probabilité estimée de profit à maturité : `{100 * prob_profit:.2f}%`")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_range, y=net_payoff, mode="lines", name="Profit net"))
    fig.update_layout(
        title=f"📉 Payoff net - {strategy}",
        xaxis_title="Prix spot (S)",
        yaxis_title="Profit / Perte",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"💰 Coût total estimé de la stratégie : `{cost:.2f}`")

    with st.expander("📘 Légende de la stratégie"):
        if strategy == "Straddle":
            st.markdown(f"""
            **Straddle**  
            ➕ Achat simultané :
            - d’un **Call** à strike `{strike}`
            - d’un **Put** à strike `{strike}`

            🔍 Parie sur une **forte volatilité** (haussier ou baissier)  
            📈 Gains si le marché bouge fort dans un sens ou l'autre  
            📉 Perte max = coût total = `{cost:.2f}`  
            🧮 Break-even ≈ `{strike - cost:.2f}` et `{strike + cost:.2f}`
            """)

        elif strategy == "Bull Call Spread":
            st.markdown(f"""
            **Bull Call Spread**  
            ➕ Achat d’un **Call K1 = {K1}**  
            ➖ Vente d’un **Call K2 = {K2}**

            🎯 Objectif : profiter d’une **hausse modérée** du sous-jacent  
            📉 Perte limitée, profit limité  
            💰 Coût net = `{cost:.2f}`  
            🧮 Profit max ≈ `{K2 - K1 - abs(cost):.2f}`
            """)

        elif strategy == "Iron Condor":
            st.markdown(f"""
            **Iron Condor**  
            ➕ Achat Put `{K1}`, ➖ Vente Put `{K2}`  
            ➖ Vente Call `{K3}`, ➕ Achat Call `{K4}`

        🎯 Objectif : **parier sur un marché stable**  
        ✅ Gains maximaux entre `{K2}` et `{K3}`  
        📉 Perte max = `{cost:.2f}` si le marché sort des bornes `{K1}` ou `{K4}`
        """)
            
with tab5:
    st.subheader("🧪 Simulation Monte Carlo du PnL")

    N_sim = st.slider("Nombre de simulations", 1000, 20000, 5000, step=1000)

    # Préparer les paramètres
    params = {}
    if strategy == "Straddle":
        stgy_key = "straddle"
        params = {"K": strike}
        cost = price_bs(S, strike, T, r, sigma, "call") + price_bs(S, strike, T, r, sigma, "put")

    elif strategy == "Bull Call Spread":
        stgy_key = "bull_call"
        params = {"K1": K1, "K2": K2}
        cost = price_bs(S, K1, T, r, sigma, "call") - price_bs(S, K2, T, r, sigma, "call")

    elif strategy == "Iron Condor":
        stgy_key = "iron_condor"
        params = {"K1": K1, "K2": K2, "K3": K3, "K4": K4}
        cost = (
            price_bs(S, K1, T, r, sigma, "put") - price_bs(S, K2, T, r, sigma, "put")
            + price_bs(S, K4, T, r, sigma, "call") - price_bs(S, K3, T, r, sigma, "call")
        )

    ST, PnLs = monte_carlo_strategy(S, T, r, sigma, N_sim, stgy_key, params)
    expected = np.mean(PnLs)
    std_dev = np.std(PnLs)
    prob_profit_mc = np.mean(PnLs > 0)

    # Affichage histogramme
    fig_mc = go.Figure()
    fig_mc.add_trace(go.Histogram(x=PnLs, nbinsx=50))
    fig_mc.update_layout(
        title="Histogramme des profits / pertes (Monte Carlo)",
        xaxis_title="PnL",
        yaxis_title="Fréquence"
    )
    st.plotly_chart(fig_mc, use_container_width=True)
    st.success(f"📊 Probabilité empirique de gain : `{100 * prob_profit_mc:.2f}%`")

def get_legs_description(strategy_key, params):
    if strategy_key == "straddle":
        return [("BUY", "Call", params["K"]), ("BUY", "Put", params["K"])]
    elif strategy_key == "bull_call":
        return [("BUY", "Call", params["K1"]), ("SELL", "Call", params["K2"])]
    elif strategy_key == "iron_condor":
        return [
            ("BUY", "Put", params["K1"]),
            ("SELL", "Put", params["K2"]),
            ("SELL", "Call", params["K3"]),
            ("BUY", "Call", params["K4"]),
        ]
    else:
        return []

with tab6:
    st.subheader("🧾 Récapitulatif global de la stratégie")

    if "PnLs" in locals():
        # Legs
        legs = get_legs_description(stgy_key, params)
        legs_table = [{"Action": action, "Instrument": opt_type, "Strike": k} for action, opt_type, k in legs]

        st.write("#### Statistiques de performance")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="💰 Coût total", value=f"{cost:.2f}")
            st.metric(label="📉 Écart type PnL", value=f"{std_dev:.2f}")

        with col2:
            st.metric(label="📈 Profit moyen", value=f"{expected:.2f}")
            st.metric(label="✅ Probabilité de gain", value=f"{100 * prob_profit_mc:.2f} %")

        with col3:
            st.metric(label="🔢 Nb simulations", value=f"{N_sim}")

        st.metric("📈 Profit moyen", value=f"{expected:.2f}", delta=f"{expected:.2f}")
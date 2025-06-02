import streamlit as st
from decimal import Decimal, getcontext
from core.option_factory import OptionFactory
from models.binomial_model import binomial_option_pricing

st.title("Valuation d'options d'après CRR Model")

option_type = st.selectbox("Type d'option", [
    'european_call', 'european_put',
    'american_call', 'american_put',
])

spot = Decimal(str(st.number_input("Prix spot de l'actif sous-jacent", value=100.0)))
strike = Decimal(str(st.number_input("Prix d'exercice (strike)", value=100.0)))
maturity = Decimal(str(st.number_input("Maturité (en années)", value=1.0)))
volatility = Decimal(str(st.number_input("Volatilité (σ)", value=0.2)))
rate = Decimal(str(st.number_input("Taux sans risque (r)", value=0.05)))
steps = st.slider("Nombre d'étapes de l'arbre binomial", min_value=1, max_value=200, value=50)

if st.button("Calculer la valeur de l'option"):
    try:
        option = OptionFactory.create_option(
            option_type=option_type,
            spot=spot,
            strike=strike,
            maturity=maturity,
            volatility=volatility,
            rate=rate
        )

        value, tree = binomial_option_pricing(option, steps=steps, return_tree=True)
        st.success(f"Valeur de l'option ({option_type}) : {round(float(value), 4)}")

    except Exception as e:
        st.error(f"Erreur lors de la valorisation : {e}")

# TODO
# Afficher l'arbre des options par une checkbox
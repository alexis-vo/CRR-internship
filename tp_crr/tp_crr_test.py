import numpy as np
from scipy.stats import norm
from tp_crr import Sn, Payoff, Calln, Deltan, Call

def test_Sn():
    print("Test Sn :")
    s0 = Sn(2, 4, 0.1, 0.3, 0)
    s1 = Sn(2, 4, 0.1, 0.3, 1)
    s4 = Sn(2, 4, 0.1, 0.3, 4)
    print("Sn j=0 :", s0)
    print("Sn j=1 :", s1)
    print("Sn j=4 :", s4)
    assert s0.shape == (1,)
    assert s1.shape == (2,)
    assert s4.shape == (5,)

def test_Payoff():
    print("Test Payoff :")
    payoff = Payoff(2, 4, 0.1, 0.3, 105)
    print("Payoff at maturity (j=n):", payoff)
    assert (payoff >= 0).all()

def test_Calln():
    print("Test Calln :")
    call_price = Calln(2, 50, 0.05, 0.1, 0.3, 100)
    print("Calln (CRR, n=50) :", call_price)
    assert call_price > 0

def test_Deltan():
    print("Test Deltan :")
    delta0 = Deltan(2, 50, 0.05, 0.1, 0.3, 100, 0)
    if delta0.size > 0:
        print("Delta à j=0 :", delta0[0])
    else:
        print("Erreur : delta vide à j=0")
    assert delta0.size > 0

def test_Call_vs_BlackScholes():
    print("Comparaison CRR vs Black-Scholes :")
    crr_price = Calln(2, 500, 0.05, 0.1, 0.3, 100)
    bs_price = Call(2, 0.05, 0.3, 100)
    print(f"Calln (n=500): {crr_price:.4f}")
    print(f"Black-Scholes: {bs_price:.4f}")
    rel_error = abs(crr_price - bs_price) / bs_price
    print(f"Erreur relative : {rel_error:.4%}")
    assert rel_error < 0.01  # < 1% d'erreur attendue

if __name__ == "__main__":
    print("=========== STARTING TESTS ===========")
    test_Sn()
    test_Payoff()
    test_Calln()
    test_Deltan()
    test_Call_vs_BlackScholes()
    print("=========== ALL TESTS OK ===========")
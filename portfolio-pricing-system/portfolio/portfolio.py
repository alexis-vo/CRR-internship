"""
Gestion de portefeuille
"""

class Portfolio:
    def __init__(self):
        self.positions = [] # contient les positions telles que calls, puts, actions, cash

    def add_position(self, name, quantity, value, kind="option"):
        self.positions.append({"name": name, "qty": quantity, "value": value, "type": kind})

    def summary(self):
        total = 0
        print("\nPortefeuille :")
        for p in self.positions:
            val = p['qty'] * p['value']
            total += val
            print(f"- {p['qty']} x {p['name']} ({p['type']}) = {val:.2f} €")
        print(f"Valeur totale : {total:.2f} €\n")
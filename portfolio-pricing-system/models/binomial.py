from decimal import Decimal, localcontext
from math import exp, sqrt
from core.options import AmericanOption
from graphviz import Digraph


def binomial_option_pricing(option, spot=None, steps=3, return_tree=False, print_tree=False, visualize=False, filename="option_tree"):
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

        if visualize:
            dot = Digraph(comment='Option Tree')
            dot.attr(rankdir='LR', nodesep='0.5', ranksep='0.75')

            for t in range(steps + 1):
                for i in range(t + 1):
                    node_id = f"{t}_{i}"
                    S = float(price_tree[t][i])
                    V = float(option_tree[t][i])
                    exercised = exercise_tree[t][i]

                    label = f"t={t}\nS={S:.2f}\nV={V:.2f}"
                    color = "lightcoral" if exercised else "lightblue"

                    dot.node(node_id, label=label, shape="circle", style="filled", fillcolor=color, fontcolor="black")

            for t in range(steps):
                for i in range(t + 1):
                    dot.edge(f"{t}_{i}", f"{t+1}_{i+1}", label="u", fontsize="10")
                    dot.edge(f"{t}_{i}", f"{t+1}_{i}", label="d", fontsize="10")


            with dot.subgraph(name='cluster_legend') as legend:
                legend.attr(label='Légende', fontsize='12', fontname='Helvetica')
                legend.attr(style='dashed', color='gray')

                node_attrs = {
                    "style": "filled",
                    "shape": "circle",
                    "width": "0.25",
                    "height": "0.25",
                    "fixedsize": "true",
                    "fontsize": "12"
                }

                legend.node('legend_exercise', label="", fillcolor="lightcoral", **node_attrs)
                legend.node('legend_hold', label="", fillcolor="lightblue", **node_attrs)

                legend.node('legend_exercise_label', label="Exercice anticipé", shape="plaintext", fontsize="12")
                legend.node('legend_hold_label', label="Conservation (valeur future)", shape="plaintext", fontsize="12")

                legend.edge('legend_exercise', 'legend_exercise_label', style='invis')
                legend.edge('legend_hold', 'legend_hold_label', style='invis')
                legend.edge('legend_exercise_label', 'legend_hold', style='invis')
            
            # Ajouter les labels de temps (t = 0, t = 1, ...) en bas du graphe
            with dot.subgraph(name='cluster_time_labels') as time_labels:
                time_labels.attr(label='', style='invis', rank='same')

                for t in range(steps+1):
                    label_node = f"time_label_{t}"
                    time_labels.node(label_node, label=f"t = {t}", shape="plaintext", fontsize="12")

                    mid_node = f"{t}_{(t // 2)}"
                    dot.edge(mid_node, label_node, style="invis")

                for t in range(steps):
                    dot.edge(f"time_label_{t}", f"time_label_{t+1}", style="invis")

            dot.render(filename=filename, format='svg', cleanup=True)
            dot.save(f"{filename}.dot")
            print(f"\nArbre SVG généré : {filename}.svg")

        return (option_tree[0][0], option_tree) if return_tree else option_tree[0][0]
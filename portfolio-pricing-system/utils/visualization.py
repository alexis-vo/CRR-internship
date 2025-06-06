import matplotlib.pyplot as plt
import numpy as np

def plot_binomial_tree(tree, title="Binomial Pricing Tree"):
    steps = len(tree) - 1
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(steps + 1):
        for j in range(i + 1):
            ax.plot(i, tree[i][j], 'bo')
            ax.text(i, tree[i][j], f"{tree[i][j]:.2f}", fontsize=8, ha='center', va='bottom')
    ax.set_title(title)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Option Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_portfolio_values_over_time(portfolio_values, title="Portfolio Value Over Time"):
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(portfolio_values)), portfolio_values, marker='o')
    plt.title(title)
    plt.xlabel("Time step")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_hedging_deltas(deltas, title="Delta Hedge Over Time"):
    plt.figure(figsize=(10, 5))
    for label, delta_list in deltas.items():
        plt.plot(range(len(delta_list)), delta_list, label=label, marker='x')
    plt.title(title)
    plt.xlabel("Time step")
    plt.ylabel("Delta")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
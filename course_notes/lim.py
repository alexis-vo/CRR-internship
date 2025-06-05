import matplotlib.pyplot as plt
import numpy as np

n_periods = np.arange(1, 21)
n_nodes = 2**(n_periods + 1) - 1

figure, ax = plt.subplots(figsize=(15, 8))

ax.plot(n_periods, n_nodes, marker='o', color='orange')

ax.set_title("Échelle jusqu'à 1000 nœuds", fontsize=16)
ax.set_xlabel("Nombre de périodes (n)", fontsize=14)
ax.set_ylabel("Nombre de nœuds", fontsize=14)

ax.tick_params(axis='both', which='major', labelsize=12)

ax.grid(True)

ax.set_ylim(0, 1000)
ax.set_xlim(0, 10)

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

df = pd.DataFrame(
    {
        "name": [
            "S_CarSharingPlus",
            "S_Basic",
            "S_Standard",
            "S_Komfort",
            "W_Flex",
            "W_Komfort",
            "Eigenes",
        ],
        "preis_kilometer": [0.23, 0.23, 0.23, 0.23, 0.28, 0.22, 0],
        "preis_stunde": [2.75, 2.5, 1.9, 1.6, 2.4, 1.8, 0],
        "grundgebuehr": [0, 5, 8.5, 15, 0, 5, 400],
    }
)

# fülle Zeit/Strecken-Matrix mit Minima der jeweiligen Kostenfunktion
max_t = 120
max_s = 1300

time = [t for t in range(max_t)]
route = [s for s in range(max_s)]


def cost_func(t, s, _df):
    return (
        (_df["preis_stunde"] * t) + (_df["preis_kilometer"] * s) + _df["grundgebuehr"]
    )


def best_rate_index(t, s, _df):
    cost_per_rate = cost_func(t, s, _df)
    return cost_per_rate.index[np.argmin(cost_per_rate)]


# calculate the matrix that contains the indices of the best tariffe per time/way combination
best_rate_matrix = np.array(
    [best_rate_index(t, s, df) for t in time for s in route]
).reshape((max_t, max_s))

# do the same, but ignoring Wuddi
best_rate_matrix_stadtteilauto = np.array(
    [best_rate_index(t, s, df.iloc[[0, 1, 2, 3, 6]]) for t in time for s in route]
).reshape((max_t, max_s))

colors = ["red", "blue", "yellow", "green", "purple", "orange", "grey"]


def create_plot(
    _max_t: int,
    _max_s: int,
    target_file: str,
    _best_rate_matrix: np.ndarray,
    title: str,
):
    fig, ax = plt.subplots()
    legend_handles = {}
    ax.plot([0, 0])
    for t in range(_max_t):
        for s in range(_max_s):
            best_idx = _best_rate_matrix[t, s]
            patch = Rectangle((t, s), 1, 1, color=colors[best_idx])

            if best_idx not in legend_handles:
                legend_handles[best_idx] = patch

            ax.add_patch(patch)

    plt.suptitle(title)
    plt.xlabel("Gebuchte Zeit [h]")
    plt.ylabel("Gefahrenen Stecke [km]")
    plt.legend(
        legend_handles.values(),
        [df["name"][x] for x in legend_handles.keys()],
        bbox_to_anchor=(1, 1),
        loc="upper left",
    )
    plt.tight_layout()
    plt.savefig(target_file)


create_plot(
    max_t, max_s, "big.png", best_rate_matrix, "Bester Tarif nach Zeit und Strecke"
)
create_plot(12, 30, "small.png", best_rate_matrix, "Bester Tarif nach Zeit und Strecke")

create_plot(
    max_t,
    max_s,
    "big_sa.png",
    best_rate_matrix_stadtteilauto,
    "Bester Tarif nach Zeit und Strecke, nur Stadtteilauto",
)

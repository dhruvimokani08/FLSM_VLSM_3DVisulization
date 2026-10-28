
import matplotlib.pyplot as plt
import numpy as np
import os

# ------------------------------------------
# PROJECT SETTINGS
# ------------------------------------------

departments = [
    "Computer Science",
    "Electrical",
    "Mechanical",
    "Central Library",
    "Data Center"
]

demand = np.array([70, 35, 18, 9, 5])

# Total IPv4 addresses allocated to each department
vlsm = np.array([128, 64, 32, 16, 8])
flsm = np.array([128, 128, 128, 128, 128])

# Measured Packet Tracer results:
# 11 packets received out of 12 for each method
methods = ["FLSM", "VLSM"]
packet_loss = [8.33, 8.33]

# Output folder
os.makedirs("results", exist_ok=True)

# Consistent professional graph style
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 15,
    "axes.labelsize": 11,
    "figure.facecolor": "white",
    "axes.facecolor": "#F8FAFC",
    "axes.titleweight": "bold"
})

x = np.arange(len(departments))


def add_labels(ax, bars, suffix=""):
    """Display values above bars."""
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:g}{suffix}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9
        )


def finish_graph(filename):
    """Apply layout and save the graph."""
    plt.tight_layout()
    plt.savefig(
        os.path.join("results", filename),
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    plt.close()


# ------------------------------------------
# GRAPH 1: ADDRESS ALLOCATION
# ------------------------------------------

fig, ax = plt.subplots(figsize=(13, 6.5))

width = 0.25

bars_demand = ax.bar(
    x - width, demand, width,
    label="Host Demand"
)

bars_vlsm = ax.bar(
    x, vlsm, width,
    label="VLSM Allocated"
)

bars_flsm = ax.bar(
    x + width, flsm, width,
    label="FLSM Allocated"
)

add_labels(ax, bars_demand)
add_labels(ax, bars_vlsm)
add_labels(ax, bars_flsm)

ax.set_xticks(x)
ax.set_xticklabels(departments, rotation=12, ha="right")
ax.set_ylabel("Number of IPv4 Addresses")
ax.set_title("FLSM vs VLSM: Address Allocation by Department", pad=18)
ax.legend(ncol=3, loc="upper right", frameon=False)
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)
ax.set_ylim(0, 155)

finish_graph("department_address_allocation.png")


# ------------------------------------------
# GRAPH 2: ADDRESS UTILISATION
# ------------------------------------------

vlsm_efficiency = demand / vlsm * 100
flsm_efficiency = demand / flsm * 100

fig, ax = plt.subplots(figsize=(13, 6.5))

width = 0.35

bars_vlsm_eff = ax.bar(
    x - width / 2,
    vlsm_efficiency,
    width,
    label="VLSM Utilisation"
)

bars_flsm_eff = ax.bar(
    x + width / 2,
    flsm_efficiency,
    width,
    label="FLSM Utilisation"
)

add_labels(ax, bars_vlsm_eff, "%")
add_labels(ax, bars_flsm_eff, "%")

ax.set_xticks(x)
ax.set_xticklabels(departments, rotation=12, ha="right")
ax.set_ylabel("Host Demand / Allocated Addresses (%)")
ax.set_title("Department-wise Address Utilisation Efficiency", pad=18)
ax.set_ylim(0, 100)
ax.legend(frameon=False)
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

finish_graph("department_utilization_efficiency.png")


# ------------------------------------------
# GRAPH 3: PACKET LOSS
# ------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5.5))

bars = ax.bar(
    methods,
    packet_loss,
    width=0.5
)

add_labels(ax, bars, "%")

ax.set_ylabel("Packet Loss (%)")
ax.set_title("FLSM vs VLSM: Measured Packet Loss", pad=18)
ax.set_ylim(0, 12)
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

finish_graph("packet_loss_comparison.png")


# ------------------------------------------
# SUMMARY
# ------------------------------------------

print("\n" + "=" * 50)
print("GRAPH GENERATION COMPLETED")
print("=" * 50)

print("1. results/department_address_allocation.png")
print("2. results/department_utilization_efficiency.png")
print("3. results/packet_loss_comparison.png")

print("\nAll three graphs saved successfully.")
print("Packet loss values are based on your recorded tests.")

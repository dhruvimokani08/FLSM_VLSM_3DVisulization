
import ipaddress

departments = [
    ("DEP-1 Computer Science", 70),
    ("DEP-2 Electrical", 35),
    ("DEP-3 Mechanical", 18),
    ("DEP-4 Central Library", 9),
    ("DEP-5 Data Center", 5)
]

# Actual FLSM configuration from Packet Tracer
flsm_networks = [
    "192.168.0.0/25",
    "192.168.0.128/25",
    "192.168.1.0/25",
    "192.168.1.128/25",
    "192.168.2.0/25"
]

# Actual VLSM configuration from Packet Tracer
vlsm_networks = [
    "10.0.1.0/25",
    "10.0.1.128/26",
    "10.0.1.192/27",
    "10.0.1.224/28",
    "10.0.1.240/29"
]


def calculate_subnets(title, networks):
    print("\n" + "=" * 115)
    print(title.center(115))
    print("=" * 115)

    print(
        f"{'Department':<25}"
        f"{'Required':>9}"
        f"{'Network/CIDR':>20}"
        f"{'Subnet Mask':>18}"
        f"{'Usable Range':>29}"
        f"{'Broadcast':>18}"
        f"{'Allocated':>11}"
        f"{'Usable':>9}"
    )
    print("-" * 115)

    total_addresses = 0
    total_usable = 0
    total_required = 0
    all_networks = []

    for (name, required), network_text in zip(
        departments, networks
    ):
        network = ipaddress.ip_network(network_text)
        usable_count = network.num_addresses - 2

        first_usable = network.network_address + 1
        last_usable = network.broadcast_address - 1

        if usable_count < required:
            raise ValueError(
                f"{name}: {network} cannot support "
                f"{required} hosts"
            )

        # Check that the subnet doesn't overlap previous subnets
        for previous in all_networks:
            if network.overlaps(previous):
                raise ValueError(
                    f"Subnet overlap detected: {network} "
                    f"and {previous}"
                )

        all_networks.append(network)

        usable_range = f"{first_usable} - {last_usable}"

        print(
            f"{name:<25}"
            f"{required:>9}"
            f"{str(network):>20}"
            f"{str(network.netmask):>18}"
            f"{usable_range:>29}"
            f"{str(network.broadcast_address):>18}"
            f"{network.num_addresses:>11}"
            f"{usable_count:>9}"
        )

        total_addresses += network.num_addresses
        total_usable += usable_count
        total_required += required

    print("-" * 115)
    print("Total required hosts:       ", total_required)
    print("Total allocated addresses:  ", total_addresses)
    print("Total usable host addresses:", total_usable)
    print("Unused usable capacity:     ", total_usable - total_required)
    print(
        "Address utilisation:        ",
        f"{total_required / total_addresses * 100:.2f}%"
    )
    print("Host capacity validation:    PASSED")
    print("Overlap validation:          PASSED")

    return total_addresses, total_usable


# Calculate both subnetting methods
flsm_total, flsm_usable = calculate_subnets(
    "FLSM ADDRESS ALLOCATION", flsm_networks
)

vlsm_total, vlsm_usable = calculate_subnets(
    "VLSM ADDRESS ALLOCATION", vlsm_networks
)

# Final comparison
required_hosts = sum(hosts for _, hosts in departments)
saved = flsm_total - vlsm_total
saving_percent = saved / flsm_total * 100

print("\n" + "=" * 60)
print("FINAL FLSM vs VLSM COMPARISON".center(60))
print("=" * 60)

print(f"{'Measurement':<35}{'FLSM':>12}{'VLSM':>12}")
print("-" * 60)
print(f"{'Allocated addresses':<35}{flsm_total:>12}{vlsm_total:>12}")
print(f"{'Usable addresses':<35}{flsm_usable:>12}{vlsm_usable:>12}")
print(f"{'Required hosts':<35}{required_hosts:>12}{required_hosts:>12}")
print(
    f"{'Unused usable capacity':<35}"
    f"{flsm_usable - required_hosts:>12}"
    f"{vlsm_usable - required_hosts:>12}"
)
print("-" * 60)
print("Addresses saved using VLSM:", saved)
print(f"Address space saved: {saving_percent:.2f}%")
print("=" * 60)

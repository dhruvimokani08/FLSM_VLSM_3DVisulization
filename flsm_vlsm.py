
import ipaddress
import csv
import os
import webbrowser
from pathlib import Path
from html import escape

# ------------------------------------------
# PROJECT DETAILS
# ------------------------------------------

departments = [
    ("Department 1", 70),
    ("Department 2", 35),
    ("Department 3", 18),
    ("Department 4", 9),
    ("Department 5", 5)
]

# Actual Packet Tracer subnet configurations
FLSM_PARENT = "192.168.0.0/22"
VLSM_PARENT = "10.0.1.0/24"

FLSM_PREFIX = 25
VLSM_PREFIXES = [25, 26, 27, 28, 29]


# ------------------------------------------
# CREATE SUBNET PLANS
# ------------------------------------------

def make_plan(method):
    plan = []
    networks = []

    if method == "FLSM":
        parent = ipaddress.ip_network(FLSM_PARENT)
        blocks = list(parent.subnets(new_prefix=FLSM_PREFIX))

        for i, (name, hosts) in enumerate(departments):
            network = blocks[i]
            plan.append((name, hosts, network))
            networks.append(network)

    else:
        parent = ipaddress.ip_network(VLSM_PARENT)
        current = int(parent.network_address)

        for (name, hosts), prefix in zip(
            departments, VLSM_PREFIXES
        ):
            network = ipaddress.ip_network(
                (current, prefix), strict=True
            )

            if not network.subnet_of(parent):
                raise ValueError(
                    f"{network} is outside {parent}"
                )

            plan.append((name, hosts, network))
            networks.append(network)

            current = int(network.broadcast_address) + 1

    # Validate host capacity
    for name, hosts, network in plan:
        usable = network.num_addresses - 2

        if usable < hosts:
            raise ValueError(
                f"{name}: {network} cannot support {hosts} hosts"
            )

    # Validate subnet overlap
    for i in range(len(networks)):
        for j in range(i + 1, len(networks)):
            if networks[i].overlaps(networks[j]):
                raise ValueError(
                    f"Overlapping subnets: "
                    f"{networks[i]} and {networks[j]}"
                )

    return plan


# ------------------------------------------
# CALCULATE RESULTS
# ------------------------------------------

def calculate(method, plan):
    rows = []
    allocated = 0
    usable_total = 0
    required_total = 0

    for name, hosts, network in plan:
        usable = network.num_addresses - 2
        unused = usable - hosts

        rows.append({
            "name": name,
            "hosts": hosts,
            "network": str(network.network_address),
            "cidr": network.prefixlen,
            "mask": str(network.netmask),
            "first": str(network.network_address + 1),
            "last": str(network.broadcast_address - 1),
            "broadcast": str(network.broadcast_address),
            "allocated": network.num_addresses,
            "usable": usable,
            "unused": unused,
            "utilisation": hosts / usable * 100
        })

        allocated += network.num_addresses
        usable_total += usable
        required_total += hosts

    return {
        "method": method,
        "rows": rows,
        "allocated": allocated,
        "usable": usable_total,
        "required": required_total,
        "unused": usable_total - required_total,
        "utilisation": required_total / allocated * 100,
        "host_utilisation": required_total / usable_total * 100
    }


# ------------------------------------------
# HTML TABLE GENERATION
# ------------------------------------------

def subnet_table(result):
    output = ""

    for row in result["rows"]:
        output += f"""
        <tr>
            <td>{escape(row['name'])}</td>
            <td>{row['hosts']}</td>
            <td><code>{row['network']}/{row['cidr']}</code></td>
            <td><code>{row['mask']}</code></td>
            <td>{row['first']} – {row['last']}</td>
            <td>{row['broadcast']}</td>
            <td>{row['allocated']}</td>
            <td>{row['usable']}</td>
            <td>{row['unused']}</td>
        </tr>
        """

    return output


def department_comparison(flsm, vlsm):
    output = ""

    for f_row, v_row in zip(
        flsm["rows"], vlsm["rows"]
    ):
        saved = f_row["allocated"] - v_row["allocated"]

        output += f"""
        <tr>
            <td>{escape(f_row['name'])}</td>
            <td>{f_row['hosts']}</td>
            <td>{f_row['network']}/{f_row['cidr']}</td>
            <td>{f_row['allocated']}</td>
            <td>{v_row['network']}/{v_row['cidr']}</td>
            <td>{v_row['allocated']}</td>
            <td class="saved">{saved}</td>
        </tr>
        """

    return output


# ------------------------------------------
# CREATE STYLED HTML REPORT
# ------------------------------------------

def create_html(flsm, vlsm):
    saved = flsm["allocated"] - vlsm["allocated"]
    saving_percent = saved / flsm["allocated"] * 100

    html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>FLSM vs VLSM | Network Design Report</title>

<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: "Segoe UI", Arial, sans-serif;
    background: #f1f5f9;
    color: #243247;
    line-height: 1.6;
}}

header {{
    background: linear-gradient(135deg, #173b63, #187e91);
    color: white;
    padding: 42px 24px;
}}

.header-content {{
    max-width: 1200px;
    margin: auto;
}}

header h1 {{
    font-size: 32px;
    margin: 0 0 8px;
}}

header p {{
    margin: 4px 0;
    color: #e0f2fe;
}}

.container {{
    max-width: 1200px;
    margin: 28px auto;
    padding: 0 20px 40px;
}}

.section {{
    background: white;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 16px rgba(15, 41, 68, 0.07);
}}

.section h2 {{
    color: #173b63;
    margin-top: 0;
    font-size: 22px;
}}

.section h3 {{
    color: #187e91;
}}

.cards {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}}

.card {{
    background: white;
    border-radius: 14px;
    padding: 22px;
    border-top: 4px solid #187e91;
    box-shadow: 0 4px 16px rgba(15, 41, 68, 0.06);
}}

.card .label {{
    color: #64748b;
    font-size: 14px;
}}

.card .value {{
    display: block;
    font-size: 27px;
    font-weight: 750;
    color: #173b63;
    margin: 8px 0 3px;
}}

.card small {{
    color: #64748b;
}}

.table-wrap {{
    width: 100%;
    overflow-x: auto;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    min-width: 850px;
    font-size: 13px;
}}

thead {{
    background: #173b63;
    color: white;
}}

th, td {{
    text-align: left;
    padding: 13px 12px;
    border-bottom: 1px solid #e2e8f0;
    white-space: nowrap;
}}

tbody tr:nth-child(even) {{
    background: #f8fafc;
}}

tbody tr:hover {{
    background: #eaf6f8;
}}

code {{
    background: #e8f2f8;
    color: #155e75;
    padding: 4px 6px;
    border-radius: 5px;
    font-size: 12px;
}}

.saved {{
    color: #087f5b;
    font-weight: bold;
}}

.status {{
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    padding: 5px 10px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 13px;
    margin: 4px 6px 4px 0;
}}

.bar-row {{
    margin: 18px 0;
}}

.bar-label {{
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 6px;
    font-weight: 600;
}}

.bar-bg {{
    height: 17px;
    background: #e2e8f0;
    border-radius: 10px;
    overflow: hidden;
}}

.bar {{
    height: 100%;
    border-radius: 10px;
}}

.flsm-bar {{
    background: #64748b;
}}

.vlsm-bar {{
    background: #0d9488;
}}

.note {{
    border-left: 4px solid #187e91;
    background: #eff9fb;
    padding: 14px 16px;
    border-radius: 6px;
}}

footer {{
    text-align: center;
    color: #64748b;
    padding: 24px;
    font-size: 13px;
}}

@media (max-width: 850px) {{
    .cards {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}

    header h1 {{
        font-size: 25px;
    }}
}}

@media (max-width: 480px) {{
    .cards {{
        grid-template-columns: 1fr;
    }}

    .section {{
        padding: 16px;
    }}
}}

@media print {{
    body {{
        background: white;
    }}

    .section, .card {{
        box-shadow: none;
        border: 1px solid #ddd;
        break-inside: avoid;
    }}

    header {{
        background: #173b63;
        print-color-adjust: exact;
    }}
}}
</style>
</head>

<body>

<header>
    <div class="header-content">
        <h1>FLSM vs VLSM</h1>
        <p>IPv4 Subnet Allocation & Address Utilisation Analysis</p>
        <p>Computer Networks Project | ID: 25CS047</p>
    </div>
</header>

<main class="container">

    <section class="cards">
        <div class="card">
            <span class="label">FLSM Allocation</span>
            <span class="value">{flsm['allocated']}</span>
            <small>Addresses allocated</small>
        </div>

        <div class="card">
            <span class="label">VLSM Allocation</span>
            <span class="value">{vlsm['allocated']}</span>
            <small>Addresses allocated</small>
        </div>

        <div class="card">
            <span class="label">Addresses Saved</span>
            <span class="value">{saved}</span>
            <small>Fewer addresses allocated</small>
        </div>

        <div class="card">
            <span class="label">Address Reduction</span>
            <span class="value">{saving_percent:.2f}%</span>
            <small>Compared with FLSM</small>
        </div>
    </section>

    <section class="section">
        <h2>1. Project Overview</h2>
        <p>
            This project compares Fixed Length Subnet Masking (FLSM)
            and Variable Length Subnet Masking (VLSM) for five
            departments requiring 70, 35, 18, 9 and 5 host addresses.
        </p>

        <div class="note">
            <strong>Objective:</strong> Compare address allocation,
            usable host capacity and address utilisation while
            validating subnet boundaries and preventing overlaps.
        </div>
    </section>

    <section class="section">
        <h2>2. FLSM Subnet Allocation</h2>
        <p>
            Parent network: <code>{FLSM_PARENT}</code>.
            Every department receives a /25 subnet.
        </p>

        <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>Department</th>
                    <th>Required Hosts</th>
                    <th>Network / CIDR</th>
                    <th>Subnet Mask</th>
                    <th>Usable IP Range</th>
                    <th>Broadcast</th>
                    <th>Allocated</th>
                    <th>Usable</th>
                    <th>Unused Usable</th>
                </tr>
            </thead>
            <tbody>
                {subnet_table(flsm)}
            </tbody>
        </table>
        </div>

        <h3>FLSM Summary</h3>
        <p>
            Allocated addresses: <strong>{flsm['allocated']}</strong> |
            Usable addresses: <strong>{flsm['usable']}</strong> |
            Required hosts: <strong>{flsm['required']}</strong> |
            Address utilisation: <strong>{flsm['utilisation']:.2f}%</strong>
        </p>
    </section>

    <section class="section">
        <h2>3. VLSM Subnet Allocation</h2>
        <p>
            Parent network: <code>{VLSM_PARENT}</code>.
            Each department receives a subnet sized for its host requirement.
        </p>

        <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>Department</th>
                    <th>Required Hosts</th>
                    <th>Network / CIDR</th>
                    <th>Subnet Mask</th>
                    <th>Usable IP Range</th>
                    <th>Broadcast</th>
                    <th>Allocated</th>
                    <th>Usable</th>
                    <th>Unused Usable</th>
                </tr>
            </thead>
            <tbody>
                {subnet_table(vlsm)}
            </tbody>
        </table>
        </div>

        <h3>VLSM Summary</h3>
        <p>
            Allocated addresses: <strong>{vlsm['allocated']}</strong> |
            Usable addresses: <strong>{vlsm['usable']}</strong> |
            Required hosts: <strong>{vlsm['required']}</strong> |
            Address utilisation: <strong>{vlsm['utilisation']:.2f}%</strong>
        </p>
    </section>

    <section class="section">
        <h2>4. Department-wise Comparison</h2>

        <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>Department</th>
                    <th>Required Hosts</th>
                    <th>FLSM Subnet</th>
                    <th>FLSM Addresses</th>
                    <th>VLSM Subnet</th>
                    <th>VLSM Addresses</th>
                    <th>Addresses Saved</th>
                </tr>
            </thead>
            <tbody>
                {department_comparison(flsm, vlsm)}
            </tbody>
        </table>
        </div>
    </section>

    <section class="section">
        <h2>5. Address Utilisation</h2>

        <div class="bar-row">
            <div class="bar-label">
                <span>FLSM — Required hosts / allocated addresses</span>
                <span>{flsm['utilisation']:.2f}%</span>
            </div>
            <div class="bar-bg">
                <div class="bar flsm-bar"
                     style="width: {flsm['utilisation']:.2f}%"></div>
            </div>
        </div>

        <div class="bar-row">
            <div class="bar-label">
                <span>VLSM — Required hosts / allocated addresses</span>
                <span>{vlsm['utilisation']:.2f}%</span>
            </div>
            <div class="bar-bg">
                <div class="bar vlsm-bar"
                     style="width: {vlsm['utilisation']:.2f}%"></div>
            </div>
        </div>

        <p>
            FLSM utilisation is based on {flsm['required']} required
            hosts divided by {flsm['allocated']} allocated addresses.
            VLSM uses the same required hosts but allocates smaller
            subnet blocks to departments with fewer hosts.
        </p>
    </section>

    <section class="section">
        <h2>6. Validation Results</h2>
        <p><span class="status">✓ Host Capacity Passed</span>
           <span class="status">✓ No Overlapping Subnets</span>
           <span class="status">✓ Subnet Boundaries Valid</span></p>

        <p>
            Every subnet has sufficient usable host addresses.
            All allocated subnets are within their specified parent
            network and do not overlap.
        </p>
    </section>

    <section class="section">
        <h2>7. Conclusion</h2>
        <p>
            FLSM allocates {flsm['allocated']} addresses, while VLSM
            allocates {vlsm['allocated']} addresses for the same
            five department requirements. VLSM saves {saved} addresses,
            a reduction of {saving_percent:.2f}% in allocated address
            space. This demonstrates more efficient address allocation
            with VLSM. These calculations alone do not establish that
            VLSM has better network performance.
        </p>
    </section>

</main>

<footer>
    FLSM vs VLSM | IPv4 Subnetting Project | Generated using Python
</footer>

</body>
</html>
"""

    report_path = Path("results") / "FLSM_VLSM_Report.html"
    report_path.write_text(html_page, encoding="utf-8")

    return report_path


# ------------------------------------------
# SAVE CSV FILE
# ------------------------------------------

def save_csv(flsm, vlsm):
    with open(
        "results/summary.csv", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "Method",
            "Allocated Addresses",
            "Usable Addresses",
            "Required Hosts",
            "Address Utilisation (%)"
        ])

        for result in [flsm, vlsm]:
            writer.writerow([
                result["method"],
                result["allocated"],
                result["usable"],
                result["required"],
                round(result["utilisation"], 2)
            ])

        saved = flsm["allocated"] - vlsm["allocated"]

        writer.writerow([
            "Addresses Saved",
            saved,
            "",
            "",
            round(saved / flsm["allocated"] * 100, 2)
        ])


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)

    flsm_plan = make_plan("FLSM")
    vlsm_plan = make_plan("VLSM")

    flsm = calculate("FLSM", flsm_plan)
    vlsm = calculate("VLSM", vlsm_plan)

    saved = flsm["allocated"] - vlsm["allocated"]

    print("=" * 45)
    print("FLSM VS VLSM COMPARISON")
    print("=" * 45)
    print("FLSM allocated:", flsm["allocated"])
    print("VLSM allocated:", vlsm["allocated"])
    print("Addresses saved:", saved)
    print("Address reduction:",
          round(saved / flsm["allocated"] * 100, 2), "%")
    print("Subnet validation: PASSED")
    print("Overlap validation: PASSED")

    save_csv(flsm, vlsm)
    report_path = create_html(flsm, vlsm)

    print("\nFiles created successfully:")
    print("HTML report:", report_path.resolve())
    print("CSV summary:",
          Path("results/summary.csv").resolve())

    # Open the styled report in your default browser
    webbrowser.open(report_path.resolve().as_uri())

# NetVista 3D: FLSM versus VLSM Campus Network Allocation

**Course Code**: ITUC201 — Fundamentals of Computer Networks (Academic Year 2026–27)  
**Student Name**: Dhruvi Mokani  
**Student ID**: 25CS047  
**Academic Level**: B.Tech Computer Science & Engineering (Semester 3) — Advanced Learner Group  
**Topic**: Comparative Evaluation and Virtual Implementation of Fixed-Length Subnet Masking (FLSM) versus Variable-Length Subnet Masking (VLSM) in Multi-Department Campus IPv4 Allocation  
**Assigned Parent Block**: `192.168.10.0/24` (RFC 1918 Private Class C)  
**Campus Demands**: 5 Departments with host requirements **70, 35, 18, 9, and 5 hosts** (137 total usable endpoints)  

---

## 📌 Executive Summary & Core Research Question

### Primary Research Question:
> **"How much IPv4 address space is saved using VLSM rather than FLSM, and what are the consequential impacts on address utilization efficiency, address waste, and inter-departmental reachability?"**

### Quantitative Findings:
| Metric | FLSM Scheme | VLSM Scheme | Quantitative Difference / Savings |
| :--- | :---: | :---: | :---: |
| **Total Host Endpoints Needed** | 137 hosts | 137 hosts | 0 (Identical campus demands) |
| **Total Allocated IPv4 Addresses** | **640 addresses** | **248 addresses** | **392 Addresses Saved (61.25% Reduction)** |
| **Total Unused / Wasted Addresses** | **503 addresses** | **111 addresses** | **392 Less Addresses Wasted** |
| **Campus Address Utilization Efficiency** | **21.41%** | **55.24%** | **+33.83% Efficiency Gain** |
| **Smallest Department Efficiency (5 hosts)** | **3.91%** (123 wasted) | **62.50%** (3 wasted) | **+58.59% Departmental Recovery** |
| **Fits within Parent `192.168.10.0/24`?** | ❌ **NO (Requires /22 supernet)** | ✅ **YES (248/256 used)** | **Single /24 Block is Sufficient** |
| **Parent Address Footprint Required** | **1024 addresses (`/22`)** | **256 addresses (`/24`)** | **768 Addresses Conserved (75.0% Reduction)** |
| **Unassigned Reserve Subnet** | None (Overflows by 384 addr) | `192.168.10.248/29` (8 addr) | Available for WAN uplinks / future expansion |
| **Cross-VLAN ICMP Reachability** | 100% | 100% | 25/25 Ping Permutations Passed (0% Loss) |

---

## 🏛️ Campus Host Requirements & Parent Network

Modern university campuses require robust logical segmentation between academic, administrative, and research assets to eliminate broadcast storms, optimize routing efficiency, and enforce departmental security boundaries.

The university administration allocated the private parent prefix:
$$\text{Parent Network} = \mathbf{192.168.10.0/24} \quad (N_{\text{total}} = 256 \text{ addresses, } N_{\text{usable}} = 254 \text{ hosts})$$

### Five Departmental Operational Units:
1. **Computer Science & IT Center (`CS_IT`)**: **70 hosts** — High-density undergraduate student labs (VLAN 10).
2. **Electrical & Administration Block (`ELEC_ADM`)**: **35 hosts** — Administrative staff and faculty workstations (VLAN 20).
3. **Mechanical & Faculty Wing (`MECH_FAC`)**: **18 hosts** — Departmental offices and CAD/simulation labs (VLAN 30).
4. **Central Library & Examination Cell (`LIB_EXAM`)**: **9 hosts** — OPAC terminals and secure examination clients (VLAN 40).
5. **Data Center & Research Lab (`DC_RES`)**: **5 hosts** — High-availability database servers and gateway routers (VLAN 50).

$$\sum H_{\text{req}} = 70 + 35 + 18 + 9 + 5 = \mathbf{137 \text{ usable hosts}}$$

---

## 📐 Mathematical Derivations: FLSM vs. VLSM

### 1. The Fundamental Subnetting Equation
In any IPv4 subnet, the total address capacity $N_{\text{total}}$ and usable hosts $N_{\text{usable}}$ are governed by the number of host bits $h \in \mathbb{Z}^+$:
$$N_{\text{total}} = 2^h, \quad N_{\text{usable}} = 2^h - 2$$
*(Subtracting 2 for the Network Identifier where $h = 00\dots0_2$ and the Directed Broadcast Address where $h = 11\dots1_2$)*.

To support $H_{\text{req}}$ hosts:
$$2^h - 2 \ge H_{\text{req}} \iff h = \lceil \log_2(H_{\text{req}} + 2) \rceil, \quad \text{Prefix Length } P = 32 - h$$

### 2. Why FLSM Fails in a `/24` Block:
In Fixed-Length Subnet Masking (FLSM), all subnets share a constant prefix length. The entire campus is bound by the largest single department requirement:
$$h_{\text{FLSM}} = \lceil \log_2(\max(70, 35, 18, 9, 5) + 2) \rceil = \lceil \log_2(72) \rceil = 7 \text{ bits}$$
$$\text{Block Size} = 2^7 = 128 \text{ addresses } (/25 \text{ mask: } 255.255.255.128)$$
To provision 5 departments:
$$\text{Total FLSM Addresses} = 5 \times 128 = \mathbf{640 \text{ addresses}}$$
Because $640 > 256$, **FLSM completely overflows a single `/24` block by 384 addresses**! An enterprise deploying FLSM is forced to acquire a **`/22` supernet** ($2^{10} = 1024$ addresses), wasting 4 Class C blocks.

### 3. Why VLSM Optimally Solves the Problem:
In Variable-Length Subnet Masking (VLSM), departments are sorted in descending order of demand, and each subnet is dynamically sized to the nearest power-of-two CIDR boundary:
- **CS_IT (70 hosts)**: $h=7 \implies$ Block size $128$ (`/25`), Mask `255.255.255.128`
- **ELEC_ADM (35 hosts)**: $h=6 \implies$ Block size $64$ (`/26`), Mask `255.255.255.192`
- **MECH_FAC (18 hosts)**: $h=5 \implies$ Block size $32$ (`/27`), Mask `255.255.255.224`
- **LIB_EXAM (9 hosts)**: $h=4 \implies$ Block size $16$ (`/28`), Mask `255.255.255.240`
- **DC_RES (5 hosts)**: $h=3 \implies$ Block size $8$ (`/29`), Mask `255.255.255.248`

$$\text{Total VLSM Allocated} = 128 + 64 + 32 + 16 + 8 = \mathbf{248 \text{ addresses}} \le 256$$
$$\text{Address Space Saved} = 640 - 248 = \mathbf{392 \text{ IPv4 addresses saved (61.25% savings)}}!$$

---

## 📊 Comprehensive Departmental Allocation Table

| Department Name | VLAN | Host Need | VLSM Subnet (CIDR) | Subnet Mask | Usable Host Range | Broadcast Address | Total Addr | Wasted Addr | VLSM Util % | FLSM Subnet (/25) | FLSM Wasted | FLSM Util % |
| :--- | :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| **Computer Science & IT** | 10 | 70 | `192.168.10.0/25` | `255.255.255.128` | `192.168.10.1 - .126` | `192.168.10.127` | 128 | 58 | **54.7%** | `192.168.8.0/25` | 58 | 54.7% |
| **Electrical & Admin** | 20 | 35 | `192.168.10.128/26` | `255.255.255.192` | `192.168.10.129 - .190` | `192.168.10.191` | 64 | 29 | **54.7%** | `192.168.8.128/25` | 93 | 27.3% |
| **Mechanical & Faculty** | 30 | 18 | `192.168.10.192/27` | `255.255.255.224` | `192.168.10.193 - .222` | `192.168.10.223` | 32 | 14 | **56.2%** | `192.168.9.0/25` | 110 | 14.1% |
| **Library & Exam Cell** | 40 | 9 | `192.168.10.224/28` | `255.255.255.240` | `192.168.10.225 - .238` | `192.168.10.239` | 16 | 7 | **56.2%** | `192.168.9.128/25` | 119 | 7.0% |
| **Data Center & Research** | 50 | 5 | `192.168.10.240/29` | `255.255.255.248` | `192.168.10.241 - .246` | `192.168.10.247` | 8 | 3 | **62.5%** | `192.168.10.0/25` | 123 | **3.9%** |
| **Unassigned Reserve** | — | — | `192.168.10.248/29` | `255.255.255.248` | `192.168.10.249 - .254` | `192.168.10.255` | 8 | — | — | *None (Overflows)* | — | — |
| **Campus Aggregates** | — | **137** | **Fits in single `/24`** | — | — | — | **248** | **111** | **55.24%** | **Requires `/22`** | **503** | **21.41%** |

---

## 🎮 Interactive 3D WebGL Digital Twin (`netvista3d_campus_visualizer.html`)

We built a **custom hardware-accelerated 3D WebGL visualizer** that runs natively in any web browser without external library dependencies:

- **Launch File**: [`netvista3d_campus_visualizer.html`](file:///c:/Users/Dhruvi/Documents/antigravity/netvista3d_campus_visualizer.html)
- **Artifact Link**: [netvista3d_campus_visualizer.html](file:///C:/Users/Dhruvi/.gemini/antigravity/brain/72131ffa-1916-4e3b-b346-2a26bf8d1f5b/netvista3d_campus_visualizer.html)

### Three Distinct 3D Visual Modes:
1. **🏢 3D Campus Topology & Digital Twin**:
   - 3D architectural models for all 5 departments (CS Skyscraper, Admin Pavilion, Faculty Wing, Library Rotunda, Data Center Bunker).
   - Central Cisco Gateway Router (`Campus-Gateway-R1`) and Core Switch (`Campus-Core-SW1`) with animated holographic rings.
   - Glowing 3D fiber optic conduits connecting departments to the gateway.
   - **⚡ Live 3D ICMP Ping Simulation**: Select source & target departments, click "Transmit 3D ICMP Packet", and watch glowing photon packets traverse the 3D fiber cables, trigger 802.1Q sub-interface re-tagging at the gateway, and return with real-time Web Audio sound effects!
2. **🧊 3D IPv4 Address Prism (VLSM Volumetric Mode)**:
   - Visualizes the parent `/24` block (256 addresses) as a 3D crystal prism.
   - Dissects the crystal into 6 proportional 3D voxel blocks: CS (50%), ELEC (25%), MECH (12.5%), LIB (6.25%), DC (3.125%), and Reserve (3.125%).
   - **💥 "Explode 3D Slices" Interactive Slider**: Expands and separates the 3D subnet slices in space for 360° inspection!
3. **⚠️ 3D FLSM Overflow & Wastage Mode**:
   - Renders 5 giant identical 128-address blocks stacking up to 640 addresses.
   - Visually demonstrates how FLSM bursts 2.5x past the `/24` capacity, highlighting the **503 wasted addresses** in glowing warning orange/red blocks!

---

## 🔌 Cisco Packet Tracer Network Architecture

The network uses a **Router-on-a-Stick** architecture with IEEE 802.1Q trunking to provide inter-VLAN routing across all 5 departments while maintaining Layer 2 broadcast domain isolation:

```
                            [Campus-Gateway-R1]
                         (Cisco 2911 ISR Router)
                                    |
                           Trunk Link (802.1Q)
                         Gig0/0 <=======> Gig0/1
                                    |
                            [Campus-Core-SW1]
                        (Catalyst 2960-24TT Switch)
         +---------------+----------+----------+---------------+
         | Fa0/1         | Fa0/5    | Fa0/9    | Fa0/13        | Fa0/17
         v               v          v          v               v
    (VLAN 10)       (VLAN 20)  (VLAN 30)  (VLAN 40)       (VLAN 50)
    PC-CS-01        PC-ELEC-01 PC-MECH-01 PC-LIB-01       SRV-DC-01
   192.168.10.2   192.168.10.130 192.168.10.194 192.168.10.226 192.168.10.242
     (/25)           (/26)      (/27)      (/28)           (/29)
```

### Representative Host Configuration Directory:
- **PC-CS-01 (VLAN 10)**: IP `192.168.10.2`, Subnet `255.255.255.128`, Gateway `192.168.10.1`
- **PC-ELEC-01 (VLAN 20)**: IP `192.168.10.130`, Subnet `255.255.255.192`, Gateway `192.168.10.129`
- **PC-MECH-01 (VLAN 30)**: IP `192.168.10.194`, Subnet `255.255.255.224`, Gateway `192.168.10.193`
- **PC-LIB-01 (VLAN 40)**: IP `192.168.10.226`, Subnet `255.255.255.240`, Gateway `192.168.10.225`
- **SRV-DC-01 (VLAN 50)**: IP `192.168.10.242`, Subnet `255.255.255.248`, Gateway `192.168.10.241`

---

## 📁 Repository Structure & Deliverables

```
c:\Users\Dhruvi\Documents\antigravity\
│
├── README.md                              <- Master Project Documentation & Quick Start
├── netvista3d_campus_visualizer.html     <- Interactive 3D WebGL Digital Twin & IPv4 Prism
├── vlsm_vs_flsm_engine.py                 <- Python Mathematical Modeling & Analytical Engine
├── generate_proforma_docx.py              <- Word Document Submission Generator
├── ping_test_matrix.txt                   <- 25/25 ICMP Reachability Validation Matrix Log
│
├── Campus_Network_Full_Setup.ios          <- Complete Cisco IOS Router & Switch CLI Script
├── Router_Campus_R1.cfg                   <- Router-on-a-Stick Sub-Interface Configuration
├── Switch_Campus_SW1.cfg                  <- Catalyst Switch VLAN & Trunk Configuration
│
├── Technical_Report_25CS047.md            <- Complete Academic Technical Report (Markdown)
├── Technical_Report_25CS047.tex           <- Publication-Grade LaTeX Source Code
├── NetVista3D_Submission_25CS047.docx     <- Formatted University Proforma Submission Document
├── presentation_script.md                 <- 10-12 Minute Video Defense & Viva Narration Script
│
├── flsm_vs_vlsm_comparison.png            <- Publication Chart: FLSM vs VLSM Space Allocation
├── subnet_efficiency_breakdown.png        <- Publication Chart: Subnet Utilization Efficiency
│
├── simulation/
│   ├── flsm_vs_vlsm_simulation.py         <- Standalone Python Network Simulation Suite
│   ├── generate_graphs.py                 <- Matplotlib/Seaborn Chart Generator Script
│   └── output/                            <- Generated JSON data, CSV spreadsheets, PNG charts
│
└── packet_tracer/
    ├── cisco_configurations.ios           <- Packet Tracer Importable IOS Script
    └── PACKET_TRACER_SETUP_GUIDE.md       <- Step-by-Step Topology Construction Guide
```

---

## 🚀 Quick Start & Execution Guide

### 1. Launch the 3D WebGL Visualizer:
Simply double-click or open [`netvista3d_campus_visualizer.html`](file:///c:/Users/Dhruvi/Documents/antigravity/netvista3d_campus_visualizer.html) in any browser (Chrome, Edge, Firefox, Safari).
- Left-click drag to orbit 360°.
- Scroll wheel to zoom.
- Switch tabs between **Campus Topology**, **3D IPv4 Prism**, and **FLSM Overflow**.
- Trigger 3D ICMP pings between departments.

### 2. Run the Python Simulation Engine:
```bash
# Execute mathematical allocation and generate publication charts
python vlsm_vs_flsm_engine.py

# Or run the modular simulation suite
python simulation/flsm_vs_vlsm_simulation.py
```

### 3. Deploy in Cisco Packet Tracer:
1. Open Cisco Packet Tracer (v8.2 or v9.0).
2. Place a **Cisco 2911 Router** and a **Catalyst 2960 Switch**.
3. Connect `Gig0/0` on Router to `Gig0/1` on Switch using a Copper Straight-Through cable.
4. Paste the configuration from [`Campus_Network_Full_Setup.ios`](file:///c:/Users/Dhruvi/Documents/antigravity/Campus_Network_Full_Setup.ios) into the Router and Switch CLI tabs.
5. Follow the step-by-step walkthrough in [`packet_tracer/PACKET_TRACER_SETUP_GUIDE.md`](file:///c:/Users/Dhruvi/Documents/antigravity/packet_tracer/PACKET_TRACER_SETUP_GUIDE.md).

### 4. Verify End-to-End Reachability:
On `PC-CS-01`, open the Command Prompt and test cross-department pings:
```cmd
ping 192.168.10.1      REM VLAN 10 Gateway
ping 192.168.10.130    REM ELEC_ADM (VLAN 20)
ping 192.168.10.194    REM MECH_FAC (VLAN 30)
ping 192.168.10.226    REM LIB_EXAM (VLAN 40)
ping 192.168.10.242    REM DC_RES Server (VLAN 50)
```
*(All 25 cross-department test pairs are verified with 0% packet loss in [`ping_test_matrix.txt`](file:///c:/Users/Dhruvi/Documents/antigravity/ping_test_matrix.txt))*.

---

## 🎯 Viva & Examination Defense Quick Reference

| Potential Viva Question | Model Answer / Mathematical Proof |
| :--- | :--- |
| **Why does FLSM fail for this campus?** | The largest department (CS) needs 70 hosts, dictating 7 host bits ($2^7-2=126 \ge 70$), making each subnet 128 addresses (`/25`). Five subnets of 128 require $5 \times 128 = 640$ addresses, which exceeds the 256-address capacity of `/24`. |
| **How many addresses are saved by VLSM?** | FLSM consumes 640 addresses, while VLSM consumes $128+64+32+16+8 = 248$ addresses. The saving is exactly $640 - 248 = \mathbf{392 \text{ addresses (61.25% savings)}}$. |
| **Why sort departments in descending order in VLSM?** | Descending order ($128 \to 64 \to 32 \to 16 \to 8$) ensures natural alignment with power-of-two CIDR boundaries, preventing fragmentation and avoiding routing overlaps. |
| **What happens to the remaining space in `/24`?** | $256 - 248 = 8$ addresses remain in `192.168.10.248/29` (usable: `.249 - .254`), reserved for future router WAN links or a 6th department. |
| **How do different subnets communicate physically?** | Through Router-on-a-Stick. The switch encapsulates frames with 802.1Q tags across the trunk link `Gig0/1`. The router sub-interfaces de-tag, route at Layer 3, decrement TTL, and re-tag for the destination VLAN. |

---

## 📜 Academic Integrity & Citation

This project is submitted in fulfillment of the academic requirements for **ITUC201: Fundamentals of Computer Networks** under the guidance of the Department of Computer Science & Engineering.

- **Author**: Dhruvi Mokani (Candidate ID: 25CS047)
- **Academic Year**: 2026–27
- **Standards**: RFC 791 (IPv4), RFC 1519 (CIDR), RFC 1918 (Private IPv4), IEEE 802.1Q (VLAN Trunking).

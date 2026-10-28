
# Packet Tracer Performance Summary

tests = {
    "FLSM": {
        "sent": 12,
        "received": 11,
        "average_rtt": 0
    },
    "VLSM": {
        "sent": 12,
        "received": 11,
        "average_rtt": 0
    }
}

print("=" * 45)
print("       FLSM vs VLSM PERFORMANCE")
print("=" * 45)

for method, result in tests.items():
    sent = result["sent"]
    received = result["received"]
    lost = sent - received
    packet_loss = (lost / sent) * 100

    print("\n{} RESULTS".format(method))
    print("-" * 30)
    print("Packets sent       :", sent)
    print("Packets received   :", received)
    print("Packets lost       :", lost)
    print("Packet loss        : {:.2f}%".format(packet_loss))
    print("Displayed average RTT: {} ms".format(
        result["average_rtt"]
    ))

print("\n" + "=" * 45)
print("CONCLUSION")
print("=" * 45)
print("Both methods had the same measured ping results.")
print("Each method received 11 out of 12 packets.")
print("Both methods had 8.33% packet loss.")
print("VLSM allocated 248 addresses, while FLSM")
print("allocated 640 addresses.")
print("VLSM saved 392 addresses (61.25%).")
print("VLSM used IP address space more efficiently.")
print("=" * 45)

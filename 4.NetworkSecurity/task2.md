## Environment Setup

The Example Voting App was deployed using Docker Compose. The environment consists of two isolated networks: front-tier  for user-facing traffic and back-tier for internal data processing.
Front-tier Subnet: 172.20.0.0/16
    
Back-tier Subnet: 172.19.0.0/16
 ### **Q1: Getting started with**  `nmap`
I identified the subnets and performed host discovery followed by service fingerprinting.
nmap -sn 172.20.0.0/16  for front end
nmap -sn 172.19.0.0/16  for back end
Due to environment restrictions, I used the TCP connect scan with version detection:
nmap -sT -sV --unprivileged 172.20.0.2 172.20.0.3
nmap -sT -sV --unprivileged 172.19.0.2-6


### Q2: Capturing the voting traffic

Front-tier : Primarily HTTP and TCP. All browser interactions occur over standard port 80.

Back-tier : Includes PostgreSQL protocol (port 5432) for data persistence and RESP (Redis Serialization Protocol) for the message queue (port 6379).

### Q3: Unique votes?

The server issues a Set-Cookie: voter_id=737c85d3fe74580; Path=/ header upon the first visit.
Uniqueness is determined client-side by this browser cookie. When a vote is cast, the browser sends the voter_id back in the POST request.
If an attacker intercepts this, they can use a script to strip or randomize the voter_id.
Since the system trusts the client-provided ID, an attacker can generate thousands of unique IDs to stuff the ballot box completely skewing the voting results.

### Q4:  `nmap`  aggressive?


The-A option enables OS fingerprinting, version detection, and script scanning. It is noisy because it sends a flood of probes, which are visible in Wireshark as a spike in TCP packets with unusual flags and rapid HTTP GET requests. This can be disturbing to services as it may trigger security alerts, exhaust connection limits, or crash fragile applications.

### Q5: Promiscuous mode?


Promiscuous mode allows a network interface to capture all traffic on a segment, even if it isn't addressed to your specific MAC address. It is essential for network engineers because, without it, you cannot see the internal communication happening between other containers on the same virtual bridge.
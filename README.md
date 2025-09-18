# VPN Tunnel Demo with Python and Docker (vpn_tun_demo_readme)

This project demonstrates a simple **encrypted VPN tunnel** built in Python using TUN/TAP interfaces inside Docker containers.

---

## How It Works
- The **server** creates a TUN interface (`tun0` at `10.8.0.1/24`) and listens on UDP port `9090`.
- The **client** creates a TUN interface (`tun0` at `10.8.0.2/24`), encrypts packets with Fernet, and sends them to the server.
- The server decrypts, writes packets into its TUN, and sends responses back encrypted.
- Result: packets sent through the client’s `tun0` reach the server’s `tun0` over an encrypted UDP channel.
- Verified by running `ping -I tun0 10.8.0.1` from the client container and receiving replies.

---

## Requirements
- Docker Desktop (Mac, Windows, or Linux)
- Internet connection to build the image

All dependencies (`python3`, `pip`, `pytun`, `cryptography`) are installed automatically inside the container.

---

## Project Structure
```
vpn-tun-demo/
├── Dockerfile
├── share/
│   ├── vpn_server.py
│   └── vpn_client.py
```

---

## Usage

### 1. Build the Docker image
```bash
docker build -t vpnlab .
docker network create vpnnet
```

### 2. Run the VPN server
Open **Terminal A**:
```bash
docker run -it --rm --name vpnserver --network vpnnet \
  --cap-add=NET_ADMIN --device /dev/net/tun \
  -v "$PWD/share":/home/app vpnlab bash

# Inside container:
python3 vpn_server.py
```

### 3. Run the VPN client
Open **Terminal B**:
```bash
docker run -it --rm --name vpnclient --network vpnnet \
  --cap-add=NET_ADMIN --device /dev/net/tun \
  -v "$PWD/share":/home/app vpnlab bash

# Inside container:
python3 vpn_client.py
```

### 4. Test the tunnel
Open a **second shell** into the client:
```bash
docker exec -it vpnclient bash
ping -I tun0 10.8.0.1
```

You should see `64 bytes from 10.8.0.1 ...` replies, proving the tunnel works.

---

## Notes
- This is a **toy VPN**, not production-ready:
  - Only supports one client
  - Uses a static symmetric key
  - No authentication or TLS
- Purpose: demonstrate how encrypted traffic can flow through TUN interfaces in Docker with Python.

---

## What I Did
I built a working demo of a **Python-based VPN tunnel** that:
- Uses Docker containers to isolate client and server
- Creates TUN devices with `pytun`
- Encrypts all packets with `cryptography.Fernet`
- Successfully routes ICMP traffic (`ping`) across the tunnel

This shows how low-level networking (TUN/TAP) and encryption can be combined to implement a basic VPN.


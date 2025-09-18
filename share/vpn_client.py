import socket
import pytun
from cryptography.fernet import Fernet
import os

# Use the same key as the server (copy once)
KEY = b'Put your key here'
cipher_suite = Fernet(KEY)

# 1. Create a TUN device
tun = pytun.TunTapDevice(name='tun0', flags=pytun.IFF_TUN)
tun.addr = '10.8.0.2'
tun.dstaddr = '10.8.0.1'
tun.netmask = '255.255.255.0'
tun.up()

# 2. Set up UDP socket
# Take SERVER_IP from environment variable, default to 'vpnserver'
server_ip = os.getenv("SERVER_IP", "vpnserver")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"VPN client is running, connecting to {server_ip}:9090...")

# 3. Handle traffic
while True:
    ip_packet = tun.read(4096)

    encrypted_data = cipher_suite.encrypt(ip_packet)
    client_socket.sendto(encrypted_data, (server_ip, 9090))

    encrypted_response, _ = client_socket.recvfrom(4096)
    response_packet = cipher_suite.decrypt(encrypted_response)
    tun.write(response_packet)

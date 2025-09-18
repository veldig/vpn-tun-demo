import socket
import pytun
from cryptography.fernet import Fernet

# Generate key and print it so client can use it
KEY = Fernet.generate_key()
print("SERVER KEY:", KEY.decode())
cipher_suite = Fernet(KEY)

# 1. Create TUN
tun = pytun.TunTapDevice(name='tun0', flags=pytun.IFF_TUN)
tun.addr = '10.8.0.1'
tun.netmask = '255.255.255.0'
tun.up()

# 2. UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 9090))
print("VPN server listening on port 9090...")

client_address = None

while True:
    encrypted_data, addr = server_socket.recvfrom(4096)
    if not client_address:
        client_address = addr
    
    ip_packet = cipher_suite.decrypt(encrypted_data)
    tun.write(ip_packet)

    response_packet = tun.read(4096)
    encrypted_response = cipher_suite.encrypt(response_packet)
    server_socket.sendto(encrypted_response, client_address)

import network
import rp2
import time
import socket
import json
# noinspection PyPackageRequirements
from machine import Pin

led = Pin("LED", Pin.OUT)
led.on()

# set your Wi-Fi Country
rp2.country('US')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# set power mode to get Wi-Fi power-saving off (if needed)
wlan.config(pm=0xa11140)

wlan.connect('A-Net', 'Sam2Curly')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print(wlan.ifconfig())

# create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = ("", 31335)
server_socket.bind(addr)
server_socket.listen()
(client_socket, address) = server_socket.accept()
print((client_socket, address))
led.off()

print('i am here')
count = 0
while True:
    payload = {'pico_data': count}
    count += 1
    packed = json.dumps(payload).encode()
    print(packed)
    client_socket.sendall(packed)
    time.sleep(.1)
    print(f'sending {count}')

import socket
import select
import rp2
from machine import Pin
import network
import time
import umsgpack


led = Pin("LED", Pin.OUT)
led.on()


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# set power mode to get Wi-Fi power-saving off (if needed)
wlan.config(pm=0xa11140)

wlan.connect('A-Net', 'Sam2Curly')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print(wlan.ifconfig())
    
count = 0
host = ""
port = 31335

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setblocking(0)
    # bind the socket to the port
    sock.bind((host, port))
    # listen for incoming connections
    sock.listen(1)
    print("Server started...")

    # sockets from which we expect to read
    inputs = [sock]
    outputs = []

    while inputs:
        # wait for at least one of the sockets to be ready for processing
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            if s is sock:
                conn, addr = s.accept()
                inputs.append(conn)
            else:
                # data = s.recv(1024)
                # get the size of the message
                length = s.recv(1)
                length = int.from_bytes(length, "big")
                if length:
                    data = s.recv(length)
                    data = msgpack.loads(data)
                    print(data)

                    payload = {'from pico_data': count}
                    count += 1
                    packed = msgpack.dumps(payload)

                    # get the length of the payload and express as a bytearray
                    p_length = bytearray(len(packed).to_bytes(1, 'big'))

                    # append the length to the packed bytarray
                    p_length.extend(packed)

                    # convert from bytearray to bytes
                    packed = bytes(p_length)

                    s.sendall(packed)
                else:
                    inputs.remove(s)
                    s.close()
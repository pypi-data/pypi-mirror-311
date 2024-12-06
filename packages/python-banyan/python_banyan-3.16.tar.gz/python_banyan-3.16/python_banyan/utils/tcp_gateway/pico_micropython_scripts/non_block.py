import time
import network, rp2, time
import socket
import umsgpack
from machine import Pin


from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from select import select


def with_select(ip="0.0.0.0", port=31335, stype=SOCK_STREAM):
    interval = 1.0
    
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


    s = socket(AF_INET, stype)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

    print("Opening port")

    s.bind((ip, port))

    s.setblocking(False)
    s.listen()

    while True:
        recv_sockets, *_ = select([s], [], [], interval)

        for read in recv_sockets:
            data = read.recv(1024)

            if not data:
                read.close()
                return
            z = umsgpack.loads(data)
            print(z)
            # print(addr, data.decode().rstrip())

        # print("Doing other stuff...")

    print("Done")
    s.setblocking(True)
    s.close()


async def _alive():
    while True:
        print("Alive")
        await asyncio.sleep(1)



with_select()

# does not work completly
# run_with_async_stream()


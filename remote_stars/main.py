import matplotlib.pyplot as plt
import numpy as np
import socket
from skimage.measure import label, regionprops

host = "84.237.21.36" # белый ip выдается регистратором (как пример)
port = 5152 # 0 - 65000

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
    return data

def coords(region):
    cy, cx = region.centroid

    return cy, cx

def distance(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

plt.figure()
plt.ion()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b'nope'

    while beat != b'yep':
        sock.send(b"get")
        bts = recvall(sock, 40002)

        im1 = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])
        im1[im1 > 0] = 1
        im1 = label(im1)
        regions = regionprops(im1)

        res = []

        for region in regions:
            cy, cx = coords(region)
            res.append([cy, cx])

        print(res)
        d = distance(res[0], res[1])
        d_rounded = round(d, 1)
        print(d_rounded)

        sock.send(f"{d_rounded}".encode())
        print(sock.recv(6))

        plt.imshow(im1)
        plt.pause(10)

        sock.send(b'beat')
        beat = sock.recv(6)

print('Done')

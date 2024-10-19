import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_closing, binary_opening, binary_dilation, binary_erosion

def neighbours2(y, x):
    return (y, x - 1), (y - 1, x)

def exist(B, nbs):
    left, top = nbs
    if (left[0] >= 0 and left[0] < B.shape[1] and
        left [1] >= 0 and left[1] < B.shape[0]):
        if B[left] == 0:
            left = None
    else:
        left = None

    if (top[0] >= 0 and top[0] < B.shape[1] and
        top [1] >= 0 and top[1] < B.shape[0]):
        if B[top] == 0:
            top = None
    else:
        top = None

    return left, top

def find(label, linked):
    j = label
    while linked[j] != 0:
        j = linked[j]
    return j

def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)

    if j != k:
        linked[k] = j

def two_pass(B):
    LB = np.zeros_like(B)
    linked = np.zeros(B.size // 2 + 1, dtype="uint")
    label = 1

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                nbs = neighbours2(y, x)
                existed = exist(B, nbs)
                if existed[0] is None and existed[1] is None:
                    m = label
                    label += 1
                else:
                    lbs = [LB[n] for n in existed if n is not None]
                    m = min(lbs)

                LB[y, x] = m

                for n in existed:
                    if n is not None:
                        lb = LB[n]
                        if lb != m:
                            union(m, lb, linked)

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                new_label = find(LB[y, x], linked)
                if new_label != LB[y, x]:
                    LB[y, x] = new_label

    unique_LB = np.unique(LB)

    j = 0

    for i in unique_LB:
        LB[LB == i] = j
        j += 1

    return LB

def split_wires(B):
    num_wires = np.unique(B)
    struct = np.ones((3, 1))
    result = []

    for i in num_wires:
        if i == 0:
            continue

        else:
            wire = B == i
            eroded_wire = binary_erosion(wire, struct)
            result.append(eroded_wire)

    return result

def count_splitted(wire):
    wire = np.array(wire, dtype="uint8")
    marked_wire = two_pass(wire)

    count = marked_wire.max()

    return count

image1 = two_pass(np.load("wires1npy.txt").astype("uint8"))
image2 = two_pass(np.load("wires2npy.txt").astype("uint8"))
image3 = two_pass(np.load("wires3npy.txt").astype("uint8"))
image4 = two_pass(np.load("wires4npy.txt").astype("uint8"))
image5 = two_pass(np.load("wires5npy.txt").astype("uint8"))
image6 = two_pass(np.load("wires6npy.txt").astype("uint8"))

splitted_wire = split_wires(image1)
i = 0
parts = count_splitted(splitted_wire[i])

if (parts == 1):
    print("Провод целый")

elif (parts == 0):
    print("Провод уничтожен")

else:
    print(f"Провод {i + 1} на изображении разделен на {parts} частей")

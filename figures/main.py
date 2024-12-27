import numpy as np
from scipy.ndimage import binary_opening, binary_erosion, binary_closing, binary_dilation, label
from skimage.measure import label

struct_rect = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1]
])

struct_right = np.array([
    [1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 0],
    [1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 0]
])

struct_left = np.array([
    [0, 0, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1]
])

struct_up = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1]
])

struct_down = np.array([
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

image = (np.load("ps.npy.txt")).astype(int)

counting = label(image)

rects = label(binary_erosion(image, struct_rect)).max()

right = label(binary_erosion(image, struct_right)).max()
left = label(binary_erosion(image, struct_left)).max()

up_and_rects = label(binary_erosion(image, struct_up)).max()
up = up_and_rects - rects

down_and_rects = label(binary_erosion(image, struct_down)).max()
down = down_and_rects - rects

print("Прямоугольники: ", rects)
print("Направо: ", right)
print("Налево: ", left)
print("Вверх: ", up)
print("Вниз: ", down)

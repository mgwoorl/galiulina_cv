import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_closing, binary_opening, binary_dilation, binary_erosion
from skimage.measure import label

def count_all_figures(B):
    num_figures = np.unique(label(B)).max()

    return num_figures

image = np.load("ps.npy").astype("uint8")

struct1 = np.array([[1, 1, 1],
                    [1, 0, 1]])

struct2 = np.array([[1, 0, 1],
                    [1, 1, 1]])

struct3 = np.array([[1, 1],
                    [1, 0],
                    [1, 1]])

struct4 = np.array([[1, 1],
                    [0, 1],
                    [1, 1]])

struct5 = np.array([[1, 1, 1],
                    [1, 1, 1]])

plt.imshow(image)
plt.show()

res_all = count_all_figures(image)
print("Общее кол-во фигур:", res_all)

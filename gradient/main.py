import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

def gradient_linear(image):
    for i, v in enumerate(np.linspace(0, 1, image.shape[0])):
        r = lerp(color1[0], color2[0], v)
        g = lerp(color1[1], color2[1], v)
        b = lerp(color1[2], color2[2], v)

        image[i, :, :] = [r, g, b]

    return image

def diagonal_gradient(image):
    for i in range(image.shape[0]):
        for j in range(image.shape[0]):
            v = (i + j) / 2

            r = lerp(color1[0], color2[0], v)
            g = lerp(color1[1], color2[1], v)
            b = lerp(color1[2], color2[2], v)

            image[i, j] = [r, g, b]

    return image

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

image2 = image.copy()

color1 = [255, 128, 0]
color2 = [0, 128, 255]

lin_grad = gradient_linear(image)
diag_grad = diagonal_gradient(image2)

plt.subplot(121)
plt.imshow(lin_grad)
plt.subplot(122)
plt.imshow(diag_grad)
plt.show()

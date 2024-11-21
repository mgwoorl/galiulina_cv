import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
from collections import defaultdict

def recognize(region):
    length = region.image.shape[0]
    width = region.image.shape[1]
    area = length * width

    if area == region.area:
        return "Rectangle"
    else:
        return "Circle"

def color_difference(color1, color2):
    return abs(color1 - color2)

im = plt.imread("balls_and_rects.png")

binary = im.mean(2)
binary[binary > 0] = 1
labeled = label(binary)
regions = regionprops(labeled)

result = defaultdict(lambda: 0)
color_counts = {
    'Rectangle': defaultdict(lambda: 0),
    'Circle': defaultdict(lambda: 0)
}

im_hsv = rgb2hsv(im)

unique_colors = []

for region in regions:
    shape = recognize(region)
    result[shape] += 1

    cy, cx = region.centroid
    color = im_hsv[int(cy), int(cx)][0]

    flag = False

    for unique_color in unique_colors:
        if color_difference(color, unique_color) < 0.05:
            flag = True
            color_counts[shape][unique_color] += 1
            break

    if not flag:
        unique_colors.append(color)
        color_counts[shape][color] += 1

print("Общее количество фигур по форме:")
print(result)

print("\nКоличество фигур определенных форм по цветам:")

for shape, colors in color_counts.items():
    print(f"{shape}:")
    for color, count in colors.items():
        print(f"  Для цвета {color}: {count} фигур")

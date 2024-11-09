import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops, euler_number
from collections import defaultdict
from pathlib import Path

def recognize(region):
    if region.image.mean() == 1.0:
        return "-"
    else:
        enumber = euler_number(region.image)
        if enumber == -1: # B or 8
            have_vl = np.sum(np.mean(region.image[:, :region.image.shape[1] // 2], 0) == 1) > 3
            if have_vl:
                return "B"
            else:
                return "8"
        # elif enumber == 0: # A or 0
        #     # cy, cx = region.centroid_local
        #     # cy /= region.image.shape[0]
        #     # cx /= region.image.shape[1]
        #     #
        #     # print(cy, cx)
        #
        #     image = region.image.copy()
        #     image[-1, :] = 1
        #     enumber = euler_number(image)
        #
        #     if enumber == -1:
        #         return "A"
        #     else:
        #         return "0"

        elif enumber == 0:  # A or 0
            image = region.image.copy()
            image[-1, :] = 1
            enumber = euler_number(image)

            if enumber == -1:
                return "A"
            else:
                have_vl = np.sum(np.mean(region.image[:, :region.image.shape[1] // 2], 0) == 1) > 3

                if have_vl:
                    image = region.image.copy()

                    num_rows = image.shape[0]
                    mid_index = num_rows // 2

                    upper_half = image[:mid_index]
                    lower_half = image[mid_index:]

                    lower_half = np.flipud(lower_half)

                    if np.array_equal(upper_half, lower_half):
                        return "D"
                    else:
                        return "P"

                else:
                    return "0"

        else:
            have_vl = np.sum(np.mean(region.image, 0) == 1) > 3
            if have_vl:
                return "1"
            else:
                if region.eccentricity < 0.4:
                    return "*"
                else:
                    image = region.image.copy()
                    image[0, :] = 1
                    image[-1, :] = 1
                    image[:, 0] = 1
                    image[:, -1] = 1

                    enumber = euler_number(image)

                    if enumber == -1:
                        return "/"
                    if enumber == -3:
                        return "X"
                    else:
                        return "W"

    return "@"

im = plt.imread('symbols.png')[:, :, :3].mean(2)
im[im > 0] = 1
labeled = label(im)
regions = regionprops(labeled)
result = defaultdict(lambda: 0)

for region in regions:
    symbol = recognize(region)
    result[symbol] += 1

print(result)
plt.imshow(labeled)
plt.show()

print(np.unique(labeled).max())

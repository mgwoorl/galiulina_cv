import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import cv2

def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

directory = Path("out")
orig_files = list(directory.glob("*.npy"))
images = []
trajectories = {"f": [], "s": [], "t": []}

for file in orig_files:
    img = np.load(file).astype("uint8")
    images.append(img)

for i, image in enumerate(images):
    cnts, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    coords = []

    for j in cnts:
        (x, y), r = cv2.minEnclosingCircle(j)
        coords.append((x, y))

    if i == 0:
        trajectories["f"].append(list(coords[0]))
        trajectories["s"].append(list(coords[1]))
        trajectories["t"].append(list(coords[2]))

    else:
        for j in trajectories.keys():
            trajectory = trajectories[j]
            next_point = None
            min_dist = 100000000
            last_point = trajectory[-1]

            for p2 in coords:
                curr_dist = distance(last_point, p2)
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    next_point = p2

            trajectory.append(list(next_point))
            coords.remove(next_point)

for key, trajectory in trajectories.items():
    x_points = [point[0] for point in trajectory]
    y_points = [point[1] for point in trajectory]

    plt.plot(x_points, y_points)

plt.show()

import os
from pathlib import Path
import cv2

directory = Path("img_with_pencils")

lower = (0, 140, 70)
upper = (110, 255, 255)

res_for_all = 0

for i in range(1, 13):
    file = os.path.join(directory, f"img ({i}).jpg")
    img = cv2.imread(file)

    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count_for_image = 0

    if len(cnts) > 0:
        for contour in cnts:
            area = cv2.contourArea(contour)
            if area > 150000:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count_for_image += 1

    res_for_all += count_for_image

    print(f"Кол-во карандашей на {i} изображении: {count_for_image}")

print(f"\nВсего карандашей: {res_for_all}")

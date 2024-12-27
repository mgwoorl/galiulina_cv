import cv2
import os
import shutil

# это использовалось для проверки того, все ли изображения были найдены
# MATCH_FOLDER = "match"
# MISMATCH_FOLDER = "mismatch"
#
# for folder in [MATCH_FOLDER, MISMATCH_FOLDER]:
#     if os.path.exists(folder):
#         shutil.rmtree(folder)
#     os.makedirs(folder)

count = 0
cap = cv2.VideoCapture('output.avi')

frame_num = 0

while cap.isOpened():
    ret,frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    objects = {"circles": 0, "oval": 0, "rects": 0}
    result_of_my_image = {"circles": 3, "oval": 1, "rects": 4}

    for cnt in contours:
        eps = 0.03 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, eps, True)

        if len(approx) == 4:
            objects["rects"] += 1
        elif len(approx) >= 8:
            objects["circles"] += 1
        elif len(approx) == 5:
            objects["oval"] += 1

        for p in approx:
            cv2.circle(frame, tuple(p[0]), 6, (255, 0, 0), 2)

        cv2.putText(frame, f"{len(approx)}", tuple(cnt[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    # frame_filename = os.path.join(MATCH_FOLDER if objects == result_of_my_image else MISMATCH_FOLDER,
    #                               f"frame_{frame_num}.png")
    # cv2.imwrite(frame_filename, frame)

    if objects == result_of_my_image:
        count += 1

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    #frame_num += 1

# я нашла 61 изображение, перепроверила по теи, которые попали в мои папки, там все так же
print(f"Количество совпадений: {count}")
cap.release()
cv2.destroyAllWindows()

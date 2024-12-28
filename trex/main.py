
import mss
import cv2
import numpy as np
import pyautogui

monitor = -1
dino = cv2.imread('dino.png')
cactus = cv2.imread('t-rex/cactus1.png')

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

CACTUS_THRESHOLD = 0.6  # Нижний порог корреляции для отображения кактуса
CACTUS_JUMP_THRESHOLD = 0.85  # Порог для прыжка
CACTUS_X_OFFSET = 50  # Допустимое расстояние по x от левого края

while True:
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[monitor] if monitor != -1 else sct.monitors[0])

        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

        # Поиск динозавра
        res_dino = cv2.matchTemplate(img, dino, cv2.TM_CCORR_NORMED)
        min_val_dino, max_val_dino, min_loc_dino, max_loc_dino = cv2.minMaxLoc(res_dino)
        if max_val_dino > 0.7:
            top_left_dino = max_loc_dino
            bottom_right_dino = (top_left_dino[0] + dino.shape[1],
                                 top_left_dino[1] + dino.shape[0])
            cv2.rectangle(img, top_left_dino, bottom_right_dino, (255, 0, 255), 2)

        # Поиск кактуса
        res_cactus = cv2.matchTemplate(img, cactus, cv2.TM_CCORR_NORMED)
        min_val_cactus, max_val_cactus, min_loc_cactus, max_loc_cactus = cv2.minMaxLoc(res_cactus)

        if max_val_cactus > CACTUS_THRESHOLD:
            top_left_cactus = max_loc_cactus
            bottom_right_cactus = (top_left_cactus[0] + cactus.shape[1],
                                   top_left_cactus[1] + cactus.shape[0])
            cv2.rectangle(img, top_left_cactus, bottom_right_cactus, (0, 255, 255), 2)

            # Проверяем только кактус и его зону, а не динозавра
            if max_val_cactus > CACTUS_JUMP_THRESHOLD and top_left_cactus[
                0] > CACTUS_X_OFFSET:  # Добавляем проверку на положение x, чтобы прыжок не был слишком рано.
                pyautogui.press('space')

        # Изменяем размер изображения для показа
        resized_img = cv2.resize(img, (WINDOW_WIDTH, WINDOW_HEIGHT))

        cv2.imshow("Game", resized_img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cv2.destroyAllWindows()

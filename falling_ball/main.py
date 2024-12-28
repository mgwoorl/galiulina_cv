import os
import time
import cv2
import pymunk.pygame_util
import pygame
import numpy as np
from falling_ball.get_img import get_img

# # Константы
WIDTH, HEIGHT = 1580, 960
FPS = 30
# #= "output_image.png"
CONTOUR_UPDATE_INTERVAL = 1

vcap = cv2.VideoCapture("rtsp://192.168.43.1:8080/h264_ulaw.sdp")
ret, frame_raw = vcap.read()
if not vcap.isOpened():
    print("Error: Cannot open RTSP stream.")
    exit()

height, width = frame_raw.shape[:2]
crop_height = int(height * 0.5)
crop_width = int(width * 0.4)

start_x = (width - crop_width) // 2
start_y = (height - crop_height) // 2
frame = frame_raw[start_y:start_y+crop_height, start_x:start_x+crop_width]

IMAGE_PATH = get_img(frame)
#cv2.imshow("frame", IMAGE_PATH)

dest_pts = np.float32([[890.0, 420.0],[1260.0,420.0], [1270.0, 650.0], [890.0,645.0]])
rect_width = 800
rect_height = 600
src_pts = np.float32([[0.0, 0.0], [rect_width, 0.0], [rect_width, rect_height], [0.0, rect_height]])

M = cv2.getPerspectiveTransform(dest_pts, src_pts)

# Функция для извлечения контуров с учетом преобразования
def extract_all_contours(warped, scale_factor=1):
    if frame is None:
        return []


    warped = cv2.flip(warped, 0)

    original_height, original_width = warped.shape
    warped = cv2.resize(warped, None, fx=scale_factor, fy=scale_factor)

    contours, _ = cv2.findContours(warped, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    scale_x = WIDTH / original_width
    scale_y = HEIGHT / original_height
    scale = min(scale_x, scale_y)

    all_contours = [
        [(point[0][0] * scale + (WIDTH - rect_width * scale) // 2,
          HEIGHT - point[0][1] * scale - (HEIGHT - rect_height * scale) // 2)
         for point in contour]
        for contour in contours
    ]

    return all_contours


# Инициализация Pygame и Pymunk
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 900)

# Визуализация
draw_options = pymunk.pygame_util.DrawOptions(screen)

widths = [WIDTH // 2, WIDTH // 4, WIDTH // 4 * 3]

def create_ball(mouse_x, mouse_y):
    # Параметры шарика
    ball_radius = 15
    ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, ball_radius))
    ball_body.position = (mouse_x, mouse_y)
    ball_body.velocity = (0, 0)
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.friction = 0.9
    ball_shape.elasticity = 0.1
    space.add(ball_body, ball_shape)



# Загрузка начальных контуров

contours = extract_all_contours(get_img(frame))
static_bodies = []


# Функция для обновления контуров
def update_contours():
    global contours, static_bodies
    # Удаление старых объектов
    for body in static_bodies:
        space.remove(body)
    static_bodies = []

    #contours = extract_all_contours(get_img(frame))
    # Добавление новых объектов
    for contour in contours:
        for i in range(len(contour) - 1):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            segment = pymunk.Segment(body, contour[i], contour[i + 1], 5)
            segment.friction = 0.9
            space.add(body, segment)
            static_bodies.append(body)

update_contours()

# Основной цикл
running = True
while running:
    current_time = time.time()

    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            create_ball(mouse_x, mouse_y) # Вызов create_ball()

    #update_contours()

    # Обновление физики
    space.step(1 / FPS)

    # Отображение
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

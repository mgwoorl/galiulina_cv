import zmq
import cv2
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")

port = 5555
socket.connect("tcp://192.168.0.100:%s" % port)
cv2.namedWindow("Client recv", cv2.WINDOW_GUI_NORMAL)

count = 0

lower = (0, 4, 0)
upper = (255, 50, 255)

cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

while True:
    msg = socket.recv()
    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)

    count = 0

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # contours = cv2.Canny(gray, flimit, slimit)
    # fcontours, hierarchy = cv2.findContours(contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    # for cnt in fcontours:
    #     cv2.drawContours(frame, fcontours, -1, (255, 255, 255), 3)

    # ret, thresh = cv2.threshold(gray, 110, 200, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(gray, 140, 200, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(hsv, flimit, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        contour = contours[i]
        area = cv2.contourArea(contour)
        if area > 300 and area < 80000:
            cv2.drawContours(frame, contours, i, (0, 255, 0), 3)
            count += 1

    key = cv2.waitKey(100)
    if key == ord('q'):
        break

    cv2.putText(frame, f"Count {count}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0))

    cv2.imshow("Client recv", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("HSV", hsv)

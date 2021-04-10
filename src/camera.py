
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Запуск видео по кадрам
    ret, captured_frame = cap.read()
    output_frame = captured_frame.copy()

    # Конвертация ориганальной картинки 
    captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
    # Первый blur 
    captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
    # Поиск в альфа канале
    captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
    # Минимальный желтый и голубой цвет для нахождения хеленого и красного цвета
    captured_frame_lab_green = cv2.inRange(captured_frame_lab, np.array([105, 31, 137]), np.array([185, 111, 217]))
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 150, 150]), np.array([190, 255, 255]))
    # Второй blur 
    captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
    captured_frame_lab_green = cv2.GaussianBlur(captured_frame_lab_green, (5, 5), 2, 2)
    # Использование функции для нахождения круга
    circlesGreen = cv2.HoughCircles(captured_frame_lab_green, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_green.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=100)
    circlesRed = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=100)

	# Поиск и отрисовка объекта
    if circlesRed is not None:
        circlesRed = np.round(circlesRed[0, :]).astype("int")
        print("red")
        cv2.circle(output_frame, center=(circlesRed[0, 0], circlesRed[0, 1]), radius=circlesRed[0, 2], color=(0, 255, 0), thickness=2)
    if circlesGreen is not None :
        circlesGreen = np.round(circlesGreen[0, :]).astype("int")
        print("green")
        cv2.circle(output_frame, center=(circlesGreen[0, 0], circlesGreen[0, 1]), radius=circlesGreen[0, 2], color=(0, 255, 0), thickness=2)
    # Выход по нажатию 
    cv2.imshow('frame', output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
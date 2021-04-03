import pygame
# import tkinter
import time
import smbus
import Adafruit_PCA9685

import RPi.GPIO as GPIO




# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 23 # пин на передачу на датчик
GPIO_ECHO = 24 # пин на прием с датчика, на нем меряем время возврата сигнала

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) # на триггер назначаем исходящий (1 или True - назначает 3,3 В на пине)
GPIO.setup(GPIO_ECHO, GPIO.IN) # эхо делаем на прием



#i2cBus = smbus.SMBus(1)
#pca9685 = PCA9685.PCA9685(i2cBus)

pwm = Adafruit_PCA9685.PCA9685(address=0x40) # задаем переменную - обращение к контроллеру PWM -  по умолчанию, если не введен адрес устройства, используется адрес 0x40
pwm.set_pwm_freq(50) # Частота ШИМ-сигнала, равная 50Гц (20 мс) - для работы серво

servo_nul = 307 # установка серв передней оси в исходное положение
servo_set_1_left = servo_nul # установка серв передней оси в исходное положение
servo_set_1_right = servo_nul # установка серв передней оси в исходное положение
servo_set_2_left = servo_nul # установка серв задней оси в исходное положение
servo_set_2_right = servo_nul # установка серв задней оси в исходное положение


# тестирование плавного поворота серво - расчет в строках 24х...
# здесь весь коридор смещен к верхнему значению на 16 для геометрического совпадения с корпусом
# весь диапазон 180 градусов составляет 380 "шагов" - по 190 шагов на 90 градусов в каждую сторону

test_servo_min = 117 # 68 - минимальное значение сработки - превышает угол 90 / для зеленых - 68
test_servo_center = 307 # 291 - среднее (математическое) положение между крайними значениями, можно скорректировать для более точного совпадения с геометрией корпуса / для зеленых - 290 среднне математическое
test_servo_max = 497 # 514 - максимальное значение сработки для синих - превышает угол 90 / для зеленых - 511

# значения из примеров, необходимо протестировать свои  серво на фактические значения
# test_servo_min = 204  (154)
# test_servo_center = 307  (322)
# test_servo_max = 409  (491)
test_servo_pwm = 0


# переменные, которые включают/выключают импульсы на колесах (ШИМ - пары чисел из адафрут 0, 4095 и т.п.)переднее левое включение/

wheel_1_fwd_pwm = 0
wheel_1_backward_pwm = 0
wheel_2_fwd_pwm = 0
wheel_2_backward_pwm = 0
wheel_3_fwd_pwm = 0
wheel_3_backward_pwm = 0
wheel_4_fwd_pwm = 0
wheel_4_backward_pwm = 0

speedUp = 2048 # установка нижнего значения скорости двигателя, используется для плавного ускорения (при низких значениях двигатель дергается и не едет).



pygame.init() # инициализация опроса клавиатуры через Pygame
 
W = 200 # установка размера графического окна, нужно ли - удалить?
H = 200
 
sc = pygame.display.set_mode((W, H)) # переменная инициализации окна - имя переменной устанавливаем сами
 
WHITE = (255, 255, 255) # задание цветов графического окна
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
FPS = 60   # обновление окна
clock = pygame.time.Clock() # переменная цикла опроса клавиатуры
 
x = W // 2 # установка координат центра окна для установки курсора. Проверить, надо? Выкинуть
y = H // 2
speed = 1 # шаг перемещения курсора,  Проверить, надо? Выкинуть
 
flagUp = flagDown = flagLeft = flagRight = False # Установка "флагов" (из механики Pygame) по типу чекбоксов, свои переменные и присвение им значение false. Далее используются для управления стрелками с клавиатуры.
servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4 = servo_mode_5 = servo_mode_6 = servo_mode_7 = False # Тоже самое, только управление цифрами с клавиатуры.


# тестирование плавного поворота серво
test_servo_left = test_servo_right = False


while 1: # Запускаем общий цикл для всего - оптимизировать?
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Выход по какому условию? Нужен?
            exit()
        elif event.type == pygame.KEYDOWN:# Проверка нажатия кнопки
            if event.key == pygame.K_LEFT: # Обозначение клавиш из Pygame
                flagLeft = True # поворот передней оси влево
            elif event.key == pygame.K_RIGHT:
                flagRight = True # поворот передней оси вправо
            elif event.key == pygame.K_UP:
                flagUp = True # все колеса вперед
            elif event.key == pygame.K_DOWN:
                flagDown = True # все колеса назад
            elif event.key == pygame.K_1:
                servo_mode_1 = True # левый танковый разворот
            elif event.key == pygame.K_2:
                servo_mode_2 = True # правый танковый разворот
            elif event.key == pygame.K_3:
                servo_mode_3 = True # параллельная парковка, обе оси влево
            elif event.key == pygame.K_4:
                servo_mode_4 = True # параллельная парковка, обе оси вправо
            elif event.key == pygame.K_5:
                servo_mode_5 = True
            elif event.key == pygame.K_6:
                servo_mode_6 = True
            elif event.key == pygame.K_7:
                servo_mode_7 = True

            # тестирование плавного поворота серво
            elif event.key == pygame.K_8:
                test_servo_left = True

            elif event.key == pygame.K_9:
                test_servo_right = True

            if event.key in [pygame.K_SPACE]:  # общий стоп
                flagUp = flagDown = flagLeft = flagRight = False
                servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4 = servo_mode_5 = servo_mode_6 = servo_mode_7 = False
                servo_set_1_left = servo_nul  # установка серв в исходное положение
                servo_set_1_right = servo_nul  # установка серв в исходное положение
                servo_set_2_left = servo_nul  # установка серв в исходное положение
                servo_set_2_right = servo_nul  # установка серв в исходное положение

                # тестирование плавного поворота серво
                test_servo_left = test_servo_right = False
                test_servo_pwm = test_servo_center


                x = W // 2 # сброс координат курсора
                y = H // 2 # сброс координат курсора

        elif event.type == pygame.KEYUP: # проверка отжатия кнопки
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                flagUp = flagDown = flagLeft = flagRight = False
                servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4  = servo_mode_5 = servo_mode_6 = servo_mode_7 = False
                wheel_1_fwd_pwm = 0
                wheel_1_backward_pwm = 0
                wheel_2_fwd_pwm = 0
                wheel_2_backward_pwm = 0
                wheel_3_fwd_pwm = 0
                wheel_3_backward_pwm = 0
                wheel_4_fwd_pwm = 0
                wheel_4_backward_pwm = 0
                speedUp = 2048

                # тестирование плавного поворота серво
                test_servo_left = test_servo_right = False


    # Если была нажата кнопка "влево" (ПРОВЕРКА сосстояния - если flagLeft = true), то присваиваем значения переменным, отвечающим за положение серво.

    # поворот серв передней оси налево
    if flagLeft:
        servo_set_1_left = 409
        servo_set_1_right = 409


    # поворот серв передней оси направо
    elif flagRight:
        servo_set_1_left = 204
        servo_set_1_right = 204


    # все вперед
    elif flagUp:
        # y -= speed # перемещение курсора в графическом окне
        # фиксированная скорость 4095 - максимум
        # wheel_1_fwd_pwm = 4095
        # wheel_2_fwd_pwm = 4095 # переднее правое колесо вперед - значение ШИМ
        # wheel_3_fwd_pwm = 4095
        # wheel_4_fwd_pwm = 4095

        # плавное ускорение вперед
        speedUp = speedUp + 20
        if speedUp > 4095:
            speedUp = 4095
        wheel_1_fwd_pwm = wheel_2_fwd_pwm = wheel_3_fwd_pwm = wheel_4_fwd_pwm = speedUp


    # все назад
    elif flagDown:
        # y += speed
        # фиксированная скорость 4095 - максимум
        # wheel_1_backward_pwm = 4095
        # wheel_2_backward_pwm = 4095 # переднее правое колесо назад - значение ШИМ - нужное значение (в данном случае 3072 = 75%), определяет скорость вращения двигателя, в нужном месте "отпускает уровень", максимальное значение 4095 - значит, что уровень поднят постоянно, фактически не ШИМ, а прямая
        # wheel_3_backward_pwm = 4095
        # wheel_4_backward_pwm = 4095

        # плавное ускорение назад
        speedUp = speedUp + 20
        if speedUp > 4095:
            speedUp = 4095
        wheel_1_backward_pwm = wheel_2_backward_pwm = wheel_3_backward_pwm = wheel_4_backward_pwm = speedUp


    # при развороте устанавливаем скорость поменьше (через ШИМ) (максимально - 4095 - постоянная прямая сигнала)

    elif servo_mode_1: # левый танковый разворот
        # x -= speed # изменение координаты курора в окне - "-1" - на шаг speed - задан выше (=1). То есть х = х-1 (х уменьшить на один). Х - это половина размера окна - оптимизировать или удалить всю графику? Может быть оставить для отображения положения, передвижения, состояния платформы.
        wheel_1_backward_pwm = 3072  # переднее левое крутим назад
        wheel_2_fwd_pwm = 3072  # переднее правое крутим вперед
        wheel_3_backward_pwm = 3072  # заднее левое крутим назад
        wheel_4_fwd_pwm = 3072  # заднее правое крутим вперед


    elif servo_mode_2: # правый танковый разворот
        # x += speed
        wheel_1_fwd_pwm = 3072  # переднее левое крутим вперед
        wheel_2_backward_pwm = 3072  # переднее правое крутим назад
        wheel_3_fwd_pwm = 3072  # заднее правое крутим вперед
        wheel_4_backward_pwm = 3072  # заднее правое крутим назад


    elif servo_mode_3: # параллельная парковка, обе оси влево
        servo_set_1_left = 409
        servo_set_1_right = 409
        servo_set_2_left = 409
        servo_set_2_right = 409

    elif servo_mode_4: # параллельная парковка, обе оси вправо
        servo_set_1_left = 204
        servo_set_1_right = 204
        servo_set_2_left = 204
        servo_set_2_right = 204

    elif servo_mode_5: # движение по окружности вокруг центра против часовой стрелки
        servo_set_1_left = 409
        servo_set_1_right = 409
        servo_set_2_left = 204
        servo_set_2_right = 204

    elif servo_mode_6: # # движение по окружности вокруг центра по часовой стрелке
        servo_set_1_left = 204
        servo_set_1_right = 204
        servo_set_2_left = 409
        servo_set_2_right = 409

    elif servo_mode_7: # # движение на месте вокруг своего центра, после поворота серв управляем танковым разворотом
        servo_set_1_left = 204
        servo_set_1_right = 409
        servo_set_2_left = 409
        servo_set_2_right = 204

    # тестирование значений ШИМ серво
    elif test_servo_left:
        # test_servo_min = test_servo_min - 1
        test_servo_pwm = test_servo_min
        # time.sleep(0.2)
        print ("servo left")

    elif test_servo_right:
        # test_servo_max = test_servo_max + 1
        test_servo_pwm = test_servo_max
        # time.sleep(0.2)
        print ("servo right")

        # test_servo_min = 154
        # test_servo_center = 322
        # test_servo_max = 491 фактически максимальное значение 514



    # --------- проверка плавного хода
    # for i in range(test_servo_pwm, test_servo_max, 5):
    #     print (i)
    #     test_servo_pwm = i
    #     time.sleep(0.1)
    # ---------

    sc.fill(WHITE) # окошко - нужно?
    pygame.draw.rect(sc, BLUE, (x, y, 10, 10)) # размер курсора - нужно?
    pygame.display.update() # обновление окошка - нужно?

    # обращение к двигателю через номер порта и параметры ШИМ (в переменных указываются значения ШИМ) (№ pin,pwm on, pwm off)
    pwm.set_pwm(7, 0, wheel_1_fwd_pwm) # Передний левый вперёд
    pwm.set_pwm(6, 0, wheel_1_backward_pwm) # Передний левый назад
    pwm.set_pwm(5, 0, wheel_2_fwd_pwm) # Передний правый вперед
    pwm.set_pwm(4, 0, wheel_2_backward_pwm) # Передний правый назад

    pwm.set_pwm(11, 0, wheel_3_fwd_pwm) # Задний левый вперед
    pwm.set_pwm(10, 0, wheel_3_backward_pwm) # Задний левый назад
    pwm.set_pwm(9, 0, wheel_4_fwd_pwm)# Задний правый вперед
    pwm.set_pwm(8, 0, wheel_4_backward_pwm)# Задний правый назад

    # обращение к серво через номер порта и параметры ШИМ (в переменных указываются значения ШИМ)
    pwm.set_pwm(12, 0, servo_set_1_left) # Серво 1 (передний левый, на передней оси)
    pwm.set_pwm(13, 0, servo_set_1_right) # Серво 2 (передний правый, на передней оси)
    pwm.set_pwm(14, 0, servo_set_2_left) # Серво 3 (задний левый, на задней оси)
    pwm.set_pwm(15, 0, servo_set_2_right) # Серво 4 (задний правый, на задней оси)



    # тестирование плавного поворота серво
    pwm.set_pwm(0, 0, test_servo_pwm)
    print (test_servo_pwm)



    # print ("wheel_2_backward_pwm=", wheel_2_backward_pwm)

    clock.tick(FPS)


    def distance():
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)

        # устанавливаем триггер через 0.01ms в состояние LOW (False или 0)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()  # время при отправке пакета
        StopTime = time.time()  # время при приеме пакета

        # сохраняем время старта
        while GPIO.input(GPIO_ECHO) == 0:  # пока на эхо значение 0 записываем значение времени
            StartTime = time.time()

        # сохраняем время возвращения
        while GPIO.input(GPIO_ECHO) == 1:  # пока на эхо значение 1 (возврат сигнала) записываем значение времени
            StopTime = time.time()

        # определяем разницу времени между стартом и возвращением
        TimeElapsed = StopTime - StartTime  # определяем время прохождения сегнала от отправки до приема (проходит 2 расстояния - до объекта и обратно)
        # время умножаем на скорость звука (34300 cm/s)
        # и делим на 2, т.к. сигнал идет до препятствия, а затем возвращается
        distance = (TimeElapsed * 34300) / 2

        return distance


    # if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
                # в print применен шаблон вывода данных, (метод format - сокращенно %)
                # .1 - количество знаков после запятой, f - Float - дробные значения
                # (могут быть d - числовое, s - строковое, i - целое числовое)

            time.sleep(0.1)

            # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


import pygame
import tkinter
import time
import smbus
import Adafruit_PCA9685

#i2cBus = smbus.SMBus(1)
#pca9685 = PCA9685.PCA9685(i2cBus)

pwm = Adafruit_PCA9685.PCA9685(address=0x40) # задаем переменную - обращение к контроллеру PWM -  по умолчанию, если не введен адрес устройства, используется адрес 0x40
pwm.set_pwm_freq(50) # Частота ШИМ-сигнала, равная 50Гц (20 мс) - для работы серво

servo_min=204
servo_max=409
servo_set_1=307
servo_set_2=307

# переменные, которые включают/выключают импульсы на колесах (ШИМ - пары чисел из адафрут 0, 4095 и т.п.)переднее левое включение/

wheel_1_fwd_pwm = 0
wheel_1_backward_pwm = 0
wheel_2_fwd_pwm = 0
wheel_2_backward_pwm = 0
wheel_3_fwd_pwm = 0
wheel_3_backward_pwm = 0
wheel_4_fwd_pwm = 0
wheel_4_backward_pwm = 0


speedUp = 2048



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
 
flUp = flDown = flLeft = flRight = False # Установка "флагов" (из механики Pygame) по типу чекбоксов, свои переменные и присвение им значение false, =0? проверить. Далее используются для управления стрелками с клавиатуры.
servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4 = servo_mode_5 = False # Тоже самое, только управление цифрами с клавиатуры.

while 1: # Запускаем общий цикл для всего - оптимизировать?
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Выход по какому условию? Нужен?
            exit()
        elif event.type == pygame.KEYDOWN:# Проверка нажатия кнопки
            if event.key == pygame.K_LEFT: # Обозначение клавиш из Pygame
                flLeft = True
            elif event.key == pygame.K_RIGHT:
                flRight = True
            elif event.key == pygame.K_UP:
                flUp = True
            elif event.key == pygame.K_DOWN:
                flDown = True
            elif event.key == pygame.K_1:
                servo_mode_1 = True # параллельная парковка вправо
            elif event.key == pygame.K_2:
                servo_mode_2 = True
            elif event.key == pygame.K_3:
                servo_mode_3 = True # параллельная парковка влево
            elif event.key == pygame.K_4:
                servo_mode_4 = True
            elif event.key == pygame.K_5:
                servo_mode_5 = True

            if event.key in [pygame.K_SPACE]:  # общий стоп
                flUp = flDown = flLeft = flRight = False
                servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4 = servo_mode_5 = False
                servo_set_1 = 307  # установка серв в исходное положение
                servo_set_2 = 307  # установка серв в исходное положение
                x = W // 2
                y = H // 2

        elif event.type == pygame.KEYUP: # проверка отжатия кнопки
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                flUp = flDown = flLeft = flRight = False
                servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4 = False
                wheel_1_fwd_pwm = 0
                wheel_1_backward_pwm = 0
                wheel_2_fwd_pwm = 0
                wheel_2_backward_pwm = 0
                wheel_3_fwd_pwm = 0
                wheel_3_backward_pwm = 0
                wheel_4_fwd_pwm = 0
                wheel_4_backward_pwm = 0
                speedUp = 2048

    # Левый танковый разворот.
    # Если была нажата кнопка "влево" (ПРОВЕРКА сосстояния - если flLeft = true), то присваиваем значения переменным, отвечающим за направление вращения двигателем, значение скорости через параметры ШИМ.
    # при развороте устанавливаем скорость поменьше (через ШИМ) (максимально - 4095 - постоянная прямая сигнала)

    # поворот серв передней оси налево
    if flLeft:
        servo_set_1 = 409


    # поворот серв передней оси направо
    elif flRight:
        servo_set_1 = 204


    # все вперед
    elif flUp:
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
    elif flDown:
        # y += speed
        # фиксированная скорость 4095 - максимум
        # wheel_1_backward_pwm = 3072
        # wheel_2_backward_pwm = 3072 # переднее правое колесо назад - значение ШИМ - нужное значение (в данном случае 3072 = 75%), определяет скорость вращения двигателя, в нужном месте "отпускает уровень", максимальное значение 4095 - значит, что уровень поднят постоянно, фактически не ШИМ, а прямая
        # wheel_3_backward_pwm = 3072
        # wheel_4_backward_pwm = 3072

        # плавное ускорение назад
        speedUp = speedUp + 20
        if speedUp > 4095:
            speedUp = 4095
        wheel_1_backward_pwm = wheel_2_backward_pwm = wheel_3_backward_pwm = wheel_4_backward_pwm = speedUp





        
    elif servo_mode_1: # правый танковый разворот
        # x -= speed # изменение координаты курора в окне - "-1" - на шаг speed - задан выше (=1). То есть х = х-1 (х уменьшить на один). Х - это половина размера окна - оптимизировать или удалить всю графику? Может быть оставить для отображения положения, передвижения, состояния платформы.
        wheel_1_backward_pwm = 3072  # переднее левое крутим назад
        wheel_2_fwd_pwm = 3072  # переднее правое крутим вперед
        wheel_3_backward_pwm = 3072  # заднее левое крутим назад
        wheel_4_fwd_pwm = 3072  # заднее правое крутим вперед


    elif servo_mode_2: # левый танковый разворот
        # x += speed
        wheel_1_fwd_pwm = 3072  # переднее левое крутим вперед
        wheel_2_backward_pwm = 3072  # переднее правое крутим назад
        wheel_3_fwd_pwm = 3072  # заднее правое крутим вперед
        wheel_4_backward_pwm = 3072  # заднее правое крутим назад


    elif servo_mode_3: # параллельная парковка, обе оси влево
        servo_set_1 = 409
        servo_set_2 = 409

    elif servo_mode_4: # параллельная парковка, обе оси вправо
        servo_set_1 = 204
        servo_set_2 = 204

    elif servo_mode_5: # пустой
        servo_set_1 = 307
        servo_set_2 = 307


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
    pwm.set_pwm(12, 0, servo_set_1) # Серво 1 (передний левый, на передней оси)
    pwm.set_pwm(13, 0, servo_set_1) # Серво 2 (передний правый, на передней оси)
    pwm.set_pwm(14, 0, servo_set_2) # Серво 3 (задний левый, на задней оси)
    pwm.set_pwm(15, 0, servo_set_2) # Серво 4 (задний правый, на задней оси)

    print ("wheel_2_backward_pwm=", wheel_2_backward_pwm)

    clock.tick(FPS)



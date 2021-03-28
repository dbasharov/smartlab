import pygame
import tkinter
import time
import smbus
import Adafruit_PCA9685
#import PCA9685
#import ServoPCA9685

#i2cBus = smbus.SMBus(1)
#pca9685 = PCA9685.PCA9685(i2cBus)
#servo00 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL12)

pwm = Adafruit_PCA9685.PCA9685(address=0x40) # (задаем переменную - обращение к контроллеру PWM -  по умолчанию, если не введен адрес устройства, используется адрес 0x40
pwm.set_pwm_freq(50) # частота ШИМ-сигнала, равная 50Гц (20 мс)

servo_min=204
servo_max=409
servo_set_1=307
servo_set_2=307


spd_on = 4096 #проверить, удалить
spd_off = 0 #проврить, удалить

# переменные, которые включают/выключают импульсы на колесах (ШИМ? - пары чисел из адафрут 0, 4096 и т.п.)переднее левое включение/

FL_on_F = FL_off_F = 0
FL_on_B = FL_off_B = 0
FR_on_F = FR_off_F = 0
FR_on_B = FR_off_B = 0
BL_on_F = BL_off_F = 0
BL_on_B = BL_off_B = 0
BR_on_F = BR_off_F = 0
BR_on_B = BR_off_B = 0

pygame.init() #инициализация опроса клавиатуры через Pygame
 
W = 200 # установка размера графического окна, нужно ли - удалить?
H = 200
 
sc = pygame.display.set_mode((W, H)) #переменная инициализации окна - имя переменной устанавливаем сами
 
WHITE = (255, 255, 255) # задание цветов графического окна
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
FPS = 60   # обновление окна
clock = pygame.time.Clock() # переменная цикла опроса клавиатуры
 
x = W // 2 #установка координат центра окна для установки курсора. Проверить, надо? Выкинуть
y = H // 2
speed = 1 # шаг перемещения курсора,  Проверить, надо? Выкинуть
 
flUp = flDown = flLeft = flRight = False # установка флагов (из механики Pygame) по типу чекбоксов, свои переменные и присвение им значение false, =0? проверить. Далее используются для управления стрелками с клавиатуры.
R1 = R2 = R3 = R4 = R5 = False # тоже самое, только управление цифрами с клавиатуры.

while 1: #запускаем общий цикл для всего - оптимизировать?
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # выход по какому условию? Нужен?
            exit()
        elif event.type == pygame.KEYDOWN:#проверка нажатия кнопки
            if event.key == pygame.K_LEFT: #обозначение клавиш из Pygame
                flLeft = True
            elif event.key == pygame.K_RIGHT:
                flRight = True
            elif event.key == pygame.K_UP:
                flUp = True
            elif event.key == pygame.K_DOWN:
                flDown = True
            elif event.key == pygame.K_1:
                R1 = True
            elif event.key == pygame.K_2:
                R2 = True
            elif event.key == pygame.K_3:
                R3 = True
            elif event.key == pygame.K_4:
                R4 = True
            elif event.key == pygame.K_5:
                R5 = True

            if event.key in [pygame.K_SPACE]:  # общий стоп
                flUp = flDown = flLeft = flRight = False
                R1 = R2 = R3 = R4 = R5 = False
                servo_set_1 = 307  # сброс серв в исходное положение
                servo_set_2 = 307  # сброс серв в исходное положение
                x = W // 2
                y = H // 2

        elif event.type == pygame.KEYUP: #проверка отжатия кнопки
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                flUp = flDown = flLeft = flRight = False
                FL_on_F = FL_off_F = 0
                FL_on_B = FL_off_B = 0
                FR_on_F = FR_off_F = 0
                FR_on_B = FR_off_B = 0
                BL_on_F = BL_off_F = 0
                BL_on_B = BL_off_B = 0
                BR_on_F = BR_off_F = 0
                BR_on_B = BR_off_B = 0

    # Левый танковый разворот. Если была нажата кнопка "влево"  (ПРОВЕРКА сосстояния - если flLeft = true), то присваиваем значения переменным, отвечающим за направление вращения двигателем, значение скорости через параметры ШИМ.
    # при развороте устанавливаем скорость поменьше 1500 (через ШИМ) (максимально - 4096 - постоянная прямая сигнала)
    if flLeft:
        x -= speed # изменение координаты курора в окне - "-1" - на шаг speed - задан выше (=1). То есть х = х-1 (х уменьшить на один). Х - это половина размера окна - оптимизировать или удалить всю графику? Может быть оставить для отображения положения, передвижения, состояния платформы.
        FL_on_B = 1500 # переднее левое крутим назад
        FR_on_F = 1500 # переднее правое крутим вперед
        BL_on_B = 1500 # заднее левое крутим назад
        BR_on_F = 1500 # заднее правое крутим вперед
      
        #
        #
        #

    # elif flRight: # правый танковый разворот
    #     x += speed
    #     if FL_on_F < 4046: #плавный старт передний правый двигатель
    #         FL_on_F += 50
    #     else:
    #         FL_on_F = 4096
    #     FR_on_B = 4096
    #     BL_on_F = 4096
    #     BR_on_B = 4096
#
#
#
    # правый танковый разворот
    elif flRight:
        x += speed
        FL_on_F = 1500 # переднее левое крутим вперед
        FR_on_B = 1500 # переднее правое крутим назад
        BL_on_F = 1500 # заднее правое крутим вперед
        BR_on_B = 1500 # заднее правое крутим назад


    # все вперед
    elif flUp:
        y -= speed
        FL_on_F = 4096
        FR_on_F = 4096
        BL_on_F = 4096
        BR_on_F = 4096

    # все назад
    elif flDown:
        y += speed
        FL_on_B = 4096 
        FR_on_B = 4096 
        BL_on_B = 4096
        BR_on_B = 4096
        
    elif R1:#если была нажата кнопка "1" - управление сервами через цыфры, переменные осей 1 и 2
        servo_set_1 = 204
        servo_set_2 = 204

    elif R2:
        servo_set_1 = 307
        servo_set_2 = 307

    elif R3:
        servo_set_1 = 409
        servo_set_2 = 409

    elif R4:
        servo_set_1 = 409

    elif R5:
        servo_set_1 = 204

    sc.fill(WHITE) # окошко - нужно?
    pygame.draw.rect(sc, BLUE, (x, y, 10, 10)) # размер курсора - нужно?
    pygame.display.update() # обновление окошка - нужно?

    # обращение к двигателю через номер порта и параметры ШИМ (в переменных указываются значения ШИМ)
    pwm.set_pwm(7, FL_on_F, FL_off_F) # Передний левый вперёд
    pwm.set_pwm(6, FL_on_B, FL_off_B) # Передний левый назад
    pwm.set_pwm(5, FR_on_F, FR_off_F) # Передний правый вперед
    pwm.set_pwm(4, FR_on_B, FR_off_B) # Передний правый назад

    pwm.set_pwm(11, BL_on_F, BL_off_F) # Задний левый вперед
    pwm.set_pwm(10, BL_on_B, BL_off_B) # Задний левый назад
    pwm.set_pwm(9, BR_on_F, BR_off_F)# Задний правый вперед
    pwm.set_pwm(8, BR_on_B, BR_off_B)# Задний правый назад

    # обращение к серво через номер порта и параметры ШИМ (в переменных указываются значения ШИМ)
    pwm.set_pwm(12, 0, servo_set_1) # Серво 1 (передний левый, на передней оси)
    pwm.set_pwm(13, 0, servo_set_1) # Серво 2 (передний правый, на передней оси)
    pwm.set_pwm(14, 0, servo_set_2) # Серво 3 (задний левый, на задней оси)
    pwm.set_pwm(15, 0, servo_set_2) # Серво 4 (задний правый, на задней оси)

    
    clock.tick(FPS)



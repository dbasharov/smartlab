
import time                                 # Импортируем класс для работы со временем
import sys, traceback                       # Импортируем библиотеки для обработки исключений
import Adafruit_PCA9685                     # для работы с PCA9685 - ШИМ-контроллер
import RPi.GPIO as GPIO                     # Импортируем библиотеку по работе с GPIO


from Sensors import distance, init_sensors  # должно быть в старте, когда старт будет доделан
from Input import get_keyboard_values, init_input

# import tkinter
# import smbus
#i2cBus = smbus.SMBus(1)
#pca9685 = PCA9685.PCA9685(i2cBus)


init_sensors()
init_input()

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
test_servo_center = 350 # 291 - среднее (математическое) положение между крайними значениями, можно скорректировать для более точного совпадения с геометрией корпуса / для зеленых - 290 среднне математическое
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
speedUp_null = 2048



 

# servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4 = servo_mode_5 = servo_mode_6 = servo_mode_7 = False # Тоже самое, только управление цифрами с клавиатуры.


# тестирование плавного поворота серво
# test_servo_left = test_servo_right = False

try:

    while 1: # Запускаем общий цикл для всего - оптимизировать?

        # flagLeft, flagRight, flagUp, flagDown, servo_mode_1, servo_mode_2, servo_mode_3, servo_mode_4, servo_mode_5, servo_mode_6, servo_mode_7, test_servo_left, test_servo_right, reset_position, stop_position = get_keyboard_values()
        keys = get_keyboard_values()

        # Если нажат пробел, то устанавливаем все серво в исходное положение
        if keys['reset_position']:
            flagUp = flagDown = flagLeft = flagRight = False # проверить flagUp и flagDown, м.б. убрать в другое место или совсем, т.к. они определяют состояние двигателей, а не серво, а двигатели останавливаются по отжатию клавиш управления
            servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4 = servo_mode_5 = servo_mode_6 = servo_mode_7 = False
            servo_set_1_left = servo_nul  # установка серв в исходное положение
            servo_set_1_right = servo_nul  # установка серв в исходное положение
            servo_set_2_left = servo_nul  # установка серв в исходное положение
            servo_set_2_right = servo_nul  # установка серв в исходное положение

            # тестирование поворота серво - для определения крайних значений конкретных серво
            test_servo_left = test_servo_right = False
            test_servo_pwm = test_servo_center

            # x = W // 2  # сброс координат курсора
            # y = H // 2  # сброс координат курсора

        # по отжатию клавиш управления останавливаем двигатели, приводим значение PWM к исходному
        # для обеспечения плавного ускорения при следующем нажатии клавиш управления и обнуляем состояние серв
        # для недопущения "наслоения" их состояний при выборе других режимов,
        if keys['stop_position']:
            flagUp = flagDown = flagLeft = flagRight = False
            servo_mode_1 = servo_mode_2 = servo_mode_3 = servo_mode_4 = servo_mode_5 = servo_mode_6 = servo_mode_7 = False
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
            # test_servo_pwm = test_servo_center

        # Если была нажата кнопка "влево" (ПРОВЕРКА сосстояния - если flagLeft = true), то присваиваем значения переменным, отвечающим за положение серво.

        # поворот серв передней оси налево
        if keys['flagLeft']:
            servo_set_1_left = 409
            servo_set_1_right = 409


        # поворот серв передней оси направо
        elif keys['flagRight']:
            servo_set_1_left = 204
            servo_set_1_right = 204


        # все вперед
        elif keys['flagUp']:
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
        elif keys['flagDown']:
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

        elif keys['servo_mode_1']: # левый танковый разворот
            # x -= speed # изменение координаты курора в окне - "-1" - на шаг speed - задан выше (=1). То есть х = х-1 (х уменьшить на один). Х - это половина размера окна - оптимизировать или удалить всю графику? Может быть оставить для отображения положения, передвижения, состояния платформы.
            wheel_1_backward_pwm = 3072  # переднее левое крутим назад
            wheel_2_fwd_pwm = 3072  # переднее правое крутим вперед
            wheel_3_backward_pwm = 3072  # заднее левое крутим назад
            wheel_4_fwd_pwm = 3072  # заднее правое крутим вперед


        elif keys['servo_mode_2']: # правый танковый разворот
            # x += speed
            wheel_1_fwd_pwm = 3072  # переднее левое крутим вперед
            wheel_2_backward_pwm = 3072  # переднее правое крутим назад
            wheel_3_fwd_pwm = 3072  # заднее правое крутим вперед
            wheel_4_backward_pwm = 3072  # заднее правое крутим назад


        elif keys['servo_mode_3']: # параллельная парковка, обе оси влево
            servo_set_1_left = 409
            servo_set_1_right = 409
            servo_set_2_left = 409
            servo_set_2_right = 409

        elif keys['servo_mode_4']: # параллельная парковка, обе оси вправо
            servo_set_1_left = 204
            servo_set_1_right = 204
            servo_set_2_left = 204
            servo_set_2_right = 204

        elif keys['servo_mode_5']: # движение по окружности вокруг центра против часовой стрелки
            servo_set_1_left = 409
            servo_set_1_right = 409
            servo_set_2_left = 204
            servo_set_2_right = 204

        elif keys['servo_mode_6']: # # движение по окружности вокруг центра по часовой стрелке
            servo_set_1_left = 204
            servo_set_1_right = 204
            servo_set_2_left = 409
            servo_set_2_right = 409

        elif keys['servo_mode_7']: # # движение на месте вокруг своего центра, после поворота серв управляем танковым разворотом
            servo_set_1_left = 204
            servo_set_1_right = 409
            servo_set_2_left = 409
            servo_set_2_right = 204

        # тестирование значений ШИМ серво
        elif keys['test_servo_left']:
            test_servo_min = test_servo_min - 1
            # test_servo_pwm = test_servo_min
            # time.sleep(0.2)
            print ("servo left")

        elif keys['test_servo_right']:
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


        # тестирование диапазона работы серво
        pwm.set_pwm(0, 0, test_servo_pwm)
        print (test_servo_pwm)


    # ----------------------- автоматический режим

        # Датчик расстояния УЗ №1
        # Значения уже присвоены в Sensors.py в функции init_ultrasonic_sensors - проверить откуда убрать

        trigg_1 = 23
        echo_1 = 24

        # Датчик расстояния УЗ №2
        # trigg_2 = 23
        # echo_2 = 24


        dist_1 = distance(trigg_1, echo_1) #GPIO_TRIGGER, GPIO_ECHO - присвоение значений GPIO

        # dist_2 = distance(trigg_2, echo_2) #GPIO_TRIGGER, GPIO_ECHO - присвоение значений GPIO

        # print ("Расстояние с центрального УЗ датчика = %d cm" % dist_1)

        # if dist_1 > 30:
        #     # trig_dist_1 = True
        #     # flagUp = trig_dist_1
        #     print ("Расстояние с центрального УЗ датчика больше 30 см = %d cm" % dist_1)
        #     # print ("Measured Distance = %.1f cm" % dist_1)
        #
        #     speedUp = speedUp + 20
        #     if speedUp > 4095:
        #         speedUp = 4095
        #     wheel_1_fwd_pwm = wheel_2_fwd_pwm = wheel_3_fwd_pwm = wheel_4_fwd_pwm = speedUp
        #     print (wheel_1_fwd_pwm)
        #
        # if  dist_1 <= 30:
        #     print ("Расстояние с центрального УЗ датчика меньше 30 см = %d cm" % dist_1)
        #     wheel_1_fwd_pwm = wheel_2_fwd_pwm = wheel_3_fwd_pwm = wheel_4_fwd_pwm = 0
        #     # time.sleep(1)
        #
        #     # в print применен шаблон вывода данных, (метод format - сокращенно %)
        #     # .1 - количество знаков после запятой, f - Float - дробные значения
        #     # (могут быть d - числовое, s - строковое, i - целое числовое)
        #
        #
        #     # range (200)
        #     # print ("Measured Distance = %d cm" % dist_1)
        #     # speedUp = speedUp_null
        #     # speedUp = speedUp + 20
        #     # if speedUp > 4095:
        #     #     speedUp = 4095
        #     # wheel_1_backward_pwm = wheel_2_backward_pwm = wheel_3_backward_pwm = wheel_4_backward_pwm = speedUp
        #     # print (wheel_1_backward_pwm)


        # if dist_1 >= 50:
        #
        #     wheel_1_backward_pwm = wheel_2_backward_pwm = wheel_3_backward_pwm = wheel_4_backward_pwm = 0
        #     print (wheel_1_backward_pwm)




    # ----------------------- автоматический режим





        # clock.tick(FPS)


except KeyboardInterrupt:
    # ...
    print("Exit pressed Ctrl+C")  # Выход из программы по нажатию Ctrl+C
except:
    # ...
    print("Other Exception")  # Прочие исключения
    print("--- Start Exception Data:")
    traceback.print_exc(limit=2, file=sys.stdout)  # Подробности исключения через traceback
    print("--- End Exception Data:")
finally:
    print("CleanUp")  # Информируем о сбросе пинов
    GPIO.cleanup()  # Возвращаем пины в исходное состояние
    print("End of program")  # Информируем о завершении работы программы


import time
import RPi.GPIO as GPIO # для работы с GPIO


GPIO.setwarnings(False)     # Отключить предупреждения - не рекомендуется

def distance(GPIO_TRIGGER, GPIO_ECHO):

    # Устанавливаем пин на "Trigger" датчика в состояние HIGH (True или 1)
    GPIO.output(GPIO_TRIGGER, True)

    # Устанавливаем пин на триггер датчика через 0.01ms в состояние LOW (False или 0)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time() # время при отправке пакета
    StopTime = time.time() # время при приеме пакета

    # сохраняем время старта
    while GPIO.input(GPIO_ECHO) == 0: # пока на эхо значение 0 записываем значение времени
        StartTime = time.time()

    # сохраняем время возвращения
    while GPIO.input(GPIO_ECHO) == 1: # пока на эхо значение 1 (возврат сигнала) записываем значение времени
        StopTime = time.time()

    # определяем разницу времени между стартом и возвращением
    TimeElapsed = StopTime - StartTime # определяем время прохождения сегнала от отправки до приема (проходит 2 расстояния - до объекта и обратно)
    # время умножаем на скорость звука (34300 cm/s)
    # и делим на 2, т.к. сигнал идет до препятствия, а затем возвращается
    dist = (TimeElapsed * 34300) / 2

    return dist

# 1 End --------------- Работа с ультразвуковым датчиком

def init_sensors():
    """
    Инициализирует все сенсоры
    """

    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)

    print ("Инициализируем все сенсоры")
    init_ultrasonic_sensors()


def init_ultrasonic_sensors():
    """
    Инициализируем ультразвуковые сенсоры

    """
    print ("Инициализируем ультразвуковой сенсор")

    init_ultrasonic_sensor(23, 24) # GPIO_TRIGGER = 23  # пин на передачу на датчик, GPIO_ECHO = 24 пин на прием с датчика, на нем меряем время возврата сигнала

    # init_ultrasonic_sensor(17, 18)


def init_ultrasonic_sensor(GPIO_TRIGGER, GPIO_ECHO): # GPIO_TRIGGER - пин на передачу на датчик, GPIO_ECHO - пин на прием с датчика, на нем меряем время возврата сигнала
    """
    ораполрплорп
    :param GPIO_TRIGGER:
    :param GPIO_ECHO:
    """
    print ("Инициализируем ультразвуковой датчик")






    # set GPIO Pins

    # set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # на триггер назначаем исходящий (1 или True - назначает 3,3 В на пине)
    GPIO.setup(GPIO_ECHO, GPIO.IN)  # эхо делаем на прием



# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 23 # пин на передачу на датчик
GPIO_ECHO = 24 # пин на прием с датчика, на нем меряем время возврата сигнала

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) # на триггер назначаем исходящий (1 или True - назначает 3,3 В на пине)
GPIO.setup(GPIO_ECHO, GPIO.IN) # эхо делаем на прием


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # устанавливаем триггер через 0.01ms в состояние LOW (False или 0)
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
    distance = (TimeElapsed * 34300) / 2

    return distance



if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %f cm" % dist)

            time.sleep(0.1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

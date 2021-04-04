import RPi.GPIO as GPIO  # Импортируем библиотеку по работе с GPIO
import time  # Импортируем класс для работы со временем
import sys, traceback  # Импортируем библиотеки для обработки исключений

try:
    # === Инициализация пинов ===
    GPIO.setmode(GPIO.BCM)

    pinsLED = [14, 15, 18]  # Три светодиода
    pinsBtnsPullUp = [25, 8]  # Две кнопки замыкаются на ноль и подтянуты к лог. единице
    pinsBtnsPullDown = [7]  # Одна кнопка замыкается на единицу и стягивается к нулю
    GPIO.setup(pinsLED, GPIO.OUT, initial=0)  # Все пины со светодиодами в режим OUTPUT

    GPIO.setup(pinsBtnsPullUp, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Кнопки в режим INPUT, к нулю с подтяжкой к единице
    GPIO.setup(pinsBtnsPullDown, GPIO.IN,
               pull_up_down=GPIO.PUD_DOWN)  # Кнопка в режим INPUT, к единице со стяжкой к нулю

    dictLED = {14: 25,
               15: 8,
               18: 7}  # Создаем словарь для установки соответствия кнопок светодиодам
    while 1:
        for i in pinsLED:  # Перебираем светодиоды
            # Далее находим в словаре dictLED кнопку соответствующую светодиоду
            # и проверяем её состояние - если кнопки, подтянутые к земле не нажаты, то светодиоды горят, иначе - гаснут
            # если кнопка, подтянутая к единице, не нажата, то светодиод не горит, иначе - загоряется
            if GPIO.input(i) != GPIO.input(dictLED[i]):
                GPIO.output(i, GPIO.input(dictLED[i]))

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
    print("CleanUp")  # Информируем сбросе пинов
    GPIO.cleanup()  # Возвращаем пины в исходное состояние
    print("End of program")  # Информируем о завершении работы программы
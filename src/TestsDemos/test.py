import RPi.GPIO as GPIO  # Импортируем библиотеку по работе с GPIO

import time  # Импортируем класс для работы со временем
import sys, traceback  # Импортируем библиотеки для обработки исключений

try:
    # === Инициализация пинов ===
    # GPIO.setmode(GPIO.BCM)
    # ...
    # Здесь размещаем основной рабочий код
    # ...
    while 1:
        # Этот цикл нужен, чтобы программа не завершилась сразу после запуска
        i = 0  # Бессмысленная переменная, чтобы у цикла while было тело.
        # Если есть код для цикла while, предыдущую строку можно удалить


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


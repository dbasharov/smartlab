import pygame  # для работы с клавиатурой


def init_input():
    print ("Инициализируем Pygame (для работы с клавиатурой)")

    pygame.init()  # инициализация опроса клавиатуры через Pygame



    W = 200  # установка размера графического окна, нужно ли - удалить?
    H = 200

    sc = pygame.display.set_mode((W, H))  # переменная инициализации окна - имя переменной устанавливаем сами

    WHITE = (255, 255, 255)  # задание цветов графического окна
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    FPS = 60  # обновление окна
    clock = pygame.time.Clock()  # переменная цикла опроса клавиатуры

    x = W // 2  # установка координат центра окна для установки курсора. Проверить, надо? Выкинуть
    y = H // 2
    speed = 1  # шаг перемещения курсора,  Проверить, надо? Выкинуть

    sc.fill(WHITE)  # окошко - нужно?
    pygame.draw.rect(sc, BLUE, (x, y, 10, 10))  # размер курсора - нужно?
    pygame.display.update()  # обновление окошка - нужно?


def get_keyboard_values():
    keys = dict()
    keys['flagLeft'] = False
    keys['flagRight'] = False
    keys['flagUp'] = False
    keys['flagDown'] = False
    keys['servo_mode_1'] = False
    keys['servo_mode_2'] = False
    keys['servo_mode_3'] = False
    keys['servo_mode_4'] = False
    keys['servo_mode_5'] = False
    keys['servo_mode_6'] = False
    keys['servo_mode_7'] = False
    keys['test_servo_left'] = False
    keys['test_servo_right'] = False
    keys['reset_position'] = False
    keys['stop_position'] = False

    # Установка "флагов" (из механики Pygame) по типу чекбоксов = свои переменные и присвение им значение false. Далее используются для управления стрелками с клавиатуры.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Выход по какому условию? Нужен?
            exit()
        elif event.type == pygame.KEYDOWN:  # Проверка нажатия кнопки
            if event.key == pygame.K_LEFT:  # Обозначение клавиш из Pygame
                keys['flagLeft'] = True  # поворот передней оси влево
            elif event.key == pygame.K_RIGHT:
                keys['flagRight'] = True  # поворот передней оси вправо
            elif event.key == pygame.K_UP:
                keys['flagUp'] = True  # все колеса вперед
            elif event.key == pygame.K_DOWN:
                keys['flagDown'] = True  # все колеса назад
            elif event.key == pygame.K_1:
                keys['servo_mode_1'] = True  # левый танковый разворот
            elif event.key == pygame.K_2:
                keys['servo_mode_2'] = True  # правый танковый разворот
            elif event.key == pygame.K_3:
                keys['servo_mode_3'] = True  # параллельная парковка, обе оси влево
            elif event.key == pygame.K_4:
                keys['servo_mode_4'] = True  # параллельная парковка, обе оси вправо
            elif event.key == pygame.K_5:
                keys['servo_mode_5'] = True
            elif event.key == pygame.K_6:
                keys['servo_mode_6'] = True
            elif event.key == pygame.K_7:
                keys['servo_mode_7'] = True

            # тестирование плавного поворота серво
            elif event.key == pygame.K_8:
                keys['test_servo_left'] = True

            elif event.key == pygame.K_9:
                keys['test_servo_right'] = True

            if event.key in [pygame.K_SPACE]:  # общий стоп
                keys['reset_position'] = True

        elif event.type == pygame.KEYUP:  # проверка отжатия кнопки
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_1, pygame.K_2,
                             pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                keys['stop_position'] = True

    # return flagLeft, flagRight, flagUp, flagDown, servo_mode_1, servo_mode_2, servo_mode_3, servo_mode_4, servo_mode_5, servo_mode_6, servo_mode_7, test_servo_left, test_servo_right, reset_position, stop_position
    return keys

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

pwm = Adafruit_PCA9685.PCA9685(address=0x40) # (задаем переменну - обращение к контроллеру PWM -  по умолчанию, если не введен адрес устройства, используется адрес 0x40
pwm.set_pwm_freq(50) # частота ШИМ-сигнала, равная 50Гц (20 мс)

servo_min=204
servo_max=409
servo_set=307

#

spd_on = 4096
spd_off = 0

FL_on_F = FL_off_F = 0 # переднее левое включение/
FL_on_B = FL_off_B = 0
FR_on_F = FR_off_F = 0
FR_on_B = FR_off_B = 0
BL_on_F = BL_off_F = 0
BL_on_B = BL_off_B = 0
BR_on_F = BR_off_F = 0
BR_on_B = BR_off_B = 0

pygame.init()
 
W = 200
H = 200
 
sc = pygame.display.set_mode((W, H))
 
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
FPS = 60   
clock = pygame.time.Clock()
 
x = W // 2
y = H // 2
speed = 1
 
flUp = flDown = flLeft = flRight = False
R1 = R2 = R3 = R4 = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:#проверка нажатия кнопки
            if event.key == pygame.K_LEFT:
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

            if event.key in [pygame.K_SPACE]:  # общий стоп
                flUp = flDown = flLeft = flRight = False
                R1 = R2 = R3 = R4 = False
                servo_set = 307  # сброс серв
                x = W // 2
                y = H // 2

        elif event.type == pygame.KEYUP:#проверка отжатия кнопки
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

 
    if flLeft:#если была нажата кнопка "влево"
        x -= speed
        FL_on_B = 4096
        FR_on_F = 4096
        BL_on_B = 4096
        BR_on_F = 4096
      
        
    elif flRight:
        x += speed
        FL_on_F = 4096
        FR_on_B = 4096
        BL_on_F = 4096
        BR_on_B = 4096
        
    elif flUp:
        y -= speed
        FL_on_F = 4096
        FR_on_F = 4096
        BL_on_F = 4096
        BR_on_F = 4096
                
    elif flDown:
        y += speed
        FL_on_B = 4096 
        FR_on_B = 4096 
        BL_on_B = 4096
        BR_on_B = 4096
        
    elif R1:#если была нажата кнопка "1"
        servo_set=204
    
    elif R2:
        servo_set=307
        
    elif R3:
        servo_set =409

     #elif R4:
    # событие по клавише "4"

    sc.fill(WHITE)
    pygame.draw.rect(sc, BLUE, (x, y, 10, 10))
    pygame.display.update()
    pwm.set_pwm(4, FL_on_F, FL_off_F) #ПЛ_вперёд
    pwm.set_pwm(5, FL_on_B, FL_off_B) #ПЛ_назад
    pwm.set_pwm(6, FR_on_F, FR_off_F) #ПП_вперёд
    pwm.set_pwm(7, FR_on_B, FR_off_B) #ПП_назад
    pwm.set_pwm(8, BL_on_F, BL_off_F) #ЗЛ_вперёд
    pwm.set_pwm(9, BL_on_B, BL_off_B) #ЗЛ_назад
    pwm.set_pwm(10, BR_on_F, BR_off_F)#ЗП_вперёд
    pwm.set_pwm(11, BR_on_B, BR_off_B)#ЗП_назад
    
    pwm.set_pwm(12, 0, servo_set)#серв 1
    pwm.set_pwm(13, 0, servo_set)#серв 2
    pwm.set_pwm(14, 0, servo_set)#серв 3        
    pwm.set_pwm(15, 0, servo_set)#серв 4
    
    
    clock.tick(FPS)

 

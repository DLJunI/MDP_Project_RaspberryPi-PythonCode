import gpiozero
from time import sleep
# degree 0 : OPEN
# degree 90 : CLOSE
SERVOMOTOR_PIN_1 = 2


servo1 = gpiozero.Servo(SERVOMOTOR_PIN_1, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)

def setServoAngle(servo, angle) :
    servo.value = (angle/90) - 1

try :
    while True :
        setServoAngle(servo1, 90)
        sleep(2)

        # setServoAngle(servo1, 90)
        # sleep(2)
except KeyboardInterrupt :
    print("Program Close")
finally :
    print("GPIO PIN CLEANING")
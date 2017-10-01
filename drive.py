import RPi.GPIO as GPIO

LEFT_POWER = 11
RIGHT_POWER = 3

LEFT_DIR_1 = 13
LEFT_DIR_2 = 15

RIGHT_DIR_1 = 5
RIGHT_DIR_2 = 7

MAX_SPEED_LEFT = 0.1142 * 2
MAX_SPEED_RIGHT = 0.1142 * 2
WHEELBASE = 0.2

POWER_THRESHOLD = 0.1


class Driver(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LEFT_POWER, GPIO.OUT)
        GPIO.setup(RIGHT_POWER, GPIO.OUT)
        GPIO.setup(LEFT_DIR_1, GPIO.OUT)
        GPIO.setup(LEFT_DIR_2, GPIO.OUT)
        GPIO.setup(RIGHT_DIR_1, GPIO.OUT)
        GPIO.setup(RIGHT_DIR_2, GPIO.OUT)

        GPIO.output(LEFT_POWER, GPIO.LOW)
        GPIO.output(RIGHT_POWER, GPIO.LOW)
        
    def set_speed(self, v_left, v_right):
        # Cap the max speed, so that you do not set values larger than allowed
        v_left = max(min(v_left, MAX_SPEED_LEFT), -MAX_SPEED_LEFT)
        v_right = max(min(v_right, MAX_SPEED_RIGHT), -MAX_SPEED_RIGHT)

        # Transform speed to PWM
        v_left /= MAX_SPEED_LEFT
        v_right /= MAX_SPEED_RIGHT

        # Controll the motor direction correctly
        if v_left >= 0:
            GPIO.output(LEFT_DIR_1, GPIO.HIGH)
            GPIO.output(LEFT_DIR_2, GPIO.LOW)
        else:
            GPIO.output(LEFT_DIR_1, GPIO.LOW)
            GPIO.output(LEFT_DIR_2, GPIO.HIGH)
            v_left = -v_left

        if v_right >= 0:
            GPIO.output(RIGHT_DIR_1, GPIO.HIGH)
            GPIO.output(RIGHT_DIR_2, GPIO.LOW)
        else:
            GPIO.output(RIGHT_DIR_1, GPIO.LOW)
            GPIO.output(RIGHT_DIR_2, GPIO.HIGH)
            v_right = -v_right

        # Actually set the duty for the motor
        if v_left > POWER_THRESHOLD:
            GPIO.output(LEFT_POWER, GPIO.HIGH)
        else:
            GPIO.output(LEFT_POWER, GPIO.LOW)

        if v_right > POWER_THRESHOLD:
            GPIO.output(RIGHT_POWER, GPIO.HIGH)
        else:
            GPIO.output(RIGHT_POWER, GPIO.LOW)

    def kill(self):
        # When killing reseting the pwm so the motors deinitialize
        GPIO.output(LEFT_POWER, GPIO.LOW)
        GPIO.output(RIGHT_POWER, GPIO.LOW)
        GPIO.cleanup()

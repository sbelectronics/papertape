import RPi.GPIO as GPIO
import time

PIN_D0 = 4
PIN_D1 = 5
PIN_D2 = 6
PIN_D3 = 7
PIN_D4 = 8
PIN_D5 = 9
PIN_D6 = 10
PIN_D7 = 11
PIN_EXECUTE = 17
PIN_TAKEOVER = 27

PIN_DATA = [PIN_D0, PIN_D1, PIN_D2, PIN_D3, PIN_D4, PIN_D5, PIN_D6, PIN_D7]

YES_EXECUTE = 0
NO_EXECUTE = 1
YES_TAKEOVER = 1
NO_TAKEOVER = 0

class Punch:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_TAKEOVER, GPIO.OUT)
        GPIO.setup(PIN_EXECUTE, GPIO.OUT)
        GPIO.output(PIN_TAKEOVER, 0)
        GPIO.output(PIN_EXECUTE, 1)

        for pin in PIN_DATA:
            GPIO.setup(pin, GPIO.OUT)

    def execute(self):
        GPIO.output(PIN_EXECUTE, YES_EXECUTE)
        time.sleep(0.2)
        GPIO.output(PIN_EXECUTE, NO_EXECUTE)

    def write(self, v):
        GPIO.output(PIN_TAKEOVER, YES_TAKEOVER)
        for pin in PIN_DATA:
            GPIO.output(pin, v&1)
            v = v >> 1
        time.sleep(0.01)
        self.execute()
        time.sleep(0.3)  # 3 character per second limit for now
        GPIO.output(PIN_TAKEOVER, NO_TAKEOVER)

    def testbits(self):
        self.write(0)
        self.write(1)
        self.write(2)
        self.write(4)
        self.write(8)
        self.write(16)
        self.write(32)
        self.write(64)
        self.write(128)

    def release(self):
        GPIO.output(PIN_EXECUTE, NO_EXECUTE)
        GPIO.output(PIN_TAKEOVER, NO_TAKEOVER)

def main():
    punch = Punch()
    try:
        while True:
            #punch.write(0x01)
            punch.testbits()
            time.sleep(5)
    finally:
        punch.release()

if __name__ == '__main__':
    main()

import RPi.GPIO as GPIO
import sys
import time
from optparse import OptionParser

QUIET=0
NORMAL=1
VERBOSE=2

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

YES_EXECUTE = 1
NO_EXECUTE = 0
YES_TAKEOVER = 1
NO_TAKEOVER = 0

class Punch:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_TAKEOVER, GPIO.OUT)
        GPIO.setup(PIN_EXECUTE, GPIO.OUT)
        GPIO.output(PIN_TAKEOVER, NO_TAKEOVER)
        GPIO.output(PIN_EXECUTE, NO_EXECUTE)

        for pin in PIN_DATA:
            GPIO.setup(pin, GPIO.OUT)

    def execute(self):
        GPIO.output(PIN_EXECUTE, YES_EXECUTE)
        time.sleep(0.005)   # less than 0.005 will not sleep
        GPIO.output(PIN_EXECUTE, NO_EXECUTE)

    def write(self, v):
        GPIO.output(PIN_TAKEOVER, YES_TAKEOVER)
        for pin in PIN_DATA:
            GPIO.output(pin, v&1)
            v = v >> 1
        time.sleep(0.01)
        self.execute()
        time.sleep(0.1)  # 10 character per second limit for now
        GPIO.output(PIN_TAKEOVER, NO_TAKEOVER)

    def exercise(self):
        self.write(0)
        self.write(1)
        self.write(2)
        self.write(4)
        self.write(8)
        self.write(16)
        self.write(32)
        self.write(64)
        self.write(128)
        self.write(64)
        self.write(32)
        self.write(16)
        self.write(8)
        self.write(4)
        self.write(2)
        self.write(1)

    def release(self):
        GPIO.output(PIN_EXECUTE, NO_EXECUTE)
        GPIO.output(PIN_TAKEOVER, NO_TAKEOVER)
        GPIO.output(PIN_D6, 0)
        GPIO.output(PIN_D7, 0)

def stoi(s):
    if s.startswith("0x") or s.startswith("0X"):
        value = int(s[2:], 16)
    elif s.startswith("$"):
        value = int(s[1:], 16)
    elif s.lower().endswith("q"):
        value = int(s[:-1], 8)
    else:
        value = int(s)
    return value

def main():
    parser = OptionParser(usage="supervisor [options] command",
            description="Commands: ...")

    parser.add_option("-v", "--verbose", dest="verbose",
         help="verbose", action="store_true", default=False)
    parser.add_option("-q", "--quiet", dest="quiet",
         help="quiet", action="store_true", default=False)
    parser.add_option("-C", "--count", dest="count",
         help="repeat the specified number of times", metavar="amount", type="int", default=1)
    parser.add_option("-D", "--delay", dest="delay",
         help="delay between passes", metavar="milliseconds", type="int", default=0)

    (options, args) = parser.parse_args(sys.argv[1:])

    if len(args)==0:
        print("missing command")
        sys.exit(-1)

    cmd = args[0]
    args=args[1:]

    verbosity = NORMAL
    if options.quiet:
        verbosity = QUIET
    elif options.verbose:
        verbosity = VERBOSE

    punch = Punch()
    try:
        count = options.count
        while (count > 0):
            if (cmd=="exercise"):
                punch.exercise()
            elif (cmd=="number"):
                if len(args)<1:
                    raise Exception("number command requires an argument")
                for arg in args:
                    punch.write(stoi(arg))
            elif (cmd=="string"):
                s = " ".join(cmd)
                for c in s:
                    punch.write(ord(c))
            count -= 1

            if options.delay>0:
                time.sleep(options.delay/1000.0)

    finally:
        punch.release()

if __name__ == '__main__':
    main()

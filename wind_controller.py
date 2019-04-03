import Adafruit_PCA9685
import time
from motor import Motor


class WindController:

    # Min @ 60
    # us: 1060 / (1000000.0 / 4096 / 60) = 260
    # start @ 60
    # us: ......                         = 288
    # Max @ 60
    # Hz: 1860 / (1000000.0 / 4096 / 60) = 457
    #
    # Min @ 100
    # us: 1060 / (1000000.0 / 4096 / 100) = 434
    # start @ 100
    # us: ......                          = 481
    # Max @ 100
    # us: 1860 / (1000000.0 / 4096 / 100) = 761
    #
    # Min @ 400
    # Hz: 1400 / (1000000.0 / 4096 / 400) = 1736
    # start @ 400
    # us: ......                          = 1954
    # Max @ 400
    # Hz: 2000 / (1000000.0 / 4096 / 400) = 3047

    def __init__(self, n_motors=1):

        self.pwmDict = {60: [260, 276, 457],
                        100: [434, 481, 761],
                        400: [1736, 1954, 3047]
                        }

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwmFreq = int(100)
        self.pwm.set_pwm_freq(self.pwmFreq)
        self.motor_channels = []
        available_channels = [0, 1, 14, 15]
        for i in range(n_motors):
            self.motor_channels.append(available_channels[i])
        self.no_motors = n_motors
        self.motors = []
        for m in self.motor_channels:
            self.motors.append(Motor(m, self.pwm, self.pwmDict[self.pwmFreq][0],
                                     self.pwmDict[self.pwmFreq][1], self.pwmDict[self.pwmFreq][2]))

    def getPWMValueFromMicroseconds(self, microseconds):
        """ used in the calculation of pwm: stop is 1060 us, full is 1860 us """
        print(microseconds)
        pwmValue = microseconds / (1000000.0/4096.0/float(self.pwmFreq))
        return int(round(pwmValue))

    def armMotors(self):
        print('Arming motors')
        for m in self.motors:
            m.arm()

    def stopMotors(self):
        print("Stopping")
        for m in self.motors:
            m.stop()

    def calibrateThrottles(self):
        for m in self.motors:
            m.calibrateThrottle()

    def setPwmForAllMotors(self, pwmValue):
        for m in self.motors:
            m.setPwmValue(pwmValue)

    def setPwm (self, pwmValue, n_motor=0):
        self.motors[n_motor].setPwmValue(pwmValue)

    def getPWM(self, n_motor=0):
        return self.motors[n_motor].getPwmValue()

    def simpleExample(self):
        print('Starting motors at 300')
        self.setPwmForAllMotors(300)
        time.sleep(3)
        print('increasing to 360')
        self.setPwmForAllMotors(360)
        time.sleep(3)
        print('increasing to 400')
        self.setPwmForAllMotors(400)
        time.sleep(3)
        print('decreasing to 300')
        self.setPwmForAllMotors(450)
        time.sleep(3)
        print('stopping')
        self.stopMotors()

    def manualControl(self):
        exit = False
        pwmValue = self.pwmDict[self.pwmFreq]
        print("Press i to increase speed, d to decrease, q to quit")
        while not(exit):
            action = input()

            if action == "i":
                pwmValue+=1
            elif action == "d":
                pwmValue-=1
            elif action == "q":
                exit = True

            print(pwmValue)

            if not(exit):
                self.setPwmForAllMotors(pwmValue)

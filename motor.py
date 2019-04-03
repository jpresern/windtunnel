import time

""" 
engine instance. Adafruit controller is passed with the "pwm" argument.
 
"""


class Motor:
    def __init__(self, channel, pwm, pwmStop, minPwm, maxPwm):
        self.channel = channel
        self.pwm = pwm
        self.pwmValue = 0
        self.pwmStop = pwmStop
        self.minPwm = minPwm
        self.maxPwm = maxPwm

    def arm(self):
        print('Arming motor on channel: '+str(self.channel))
        self.pwmValue = self.pwmStop
        self.pwm.set_pwm(self.channel, 0, self.pwmValue)

    def setPwmValue(self, pwmValue):

        if pwmValue > self.maxPwm:
            pwmValue = self.maxPwm
        elif pwmValue < self.minPwm:
            pwmValue = self.minPwm

        self.pwmValue = pwmValue
        self.pwm.set_pwm(self.channel, 0, self.pwmValue)

    def getPwmValue(self):
        return self.pwmValue

    def stop(self):
        print('Stopping motor on channel: '+str(self.channel))
        self.pwmValue = self.pwmStop
        self.pwm.set_pwm(self.channel, 0, self.pwmStop)

    def calibrateThrottle(self):
        print("Disconnect power from ESC, leave connected to PWM hat")
        time.sleep(5)
        print("Setting throttle to highest position, please connect power to ESC")
        self.pwm.set_pwm(self.channel, 0, self.maxPwm)
        time.sleep(15)
        print("The motor should produce a series of initialization beeps increasing in pitch, followed by another beep matching the pitch of the last initialization beep.")
        input("Press enter once initialization beeps finish")
        print("Moving throttle to lowest position, two beeps of the same pitch should be emitted, followed by higher pitched long beep")
        self.pwm.set_pwm(self.channel, 0, self.minPwm)
        input("Press enter after the beeps")
        print("ESC exiting calibration mode")
        print("ESC should arm and produce a higher pitched long beep")

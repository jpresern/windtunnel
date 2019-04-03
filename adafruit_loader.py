class AdafruitLoader:

    def __init__(self):
        self.mode = 'wind'

    def getPwmModule(self):
        import Adafruit_PCA9685
        pwm = Adafruit_PCA9685.PCA9685()
        return pwm

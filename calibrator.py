import pandas as pd
import numpy as np
from scipy.interpolate import UnivariateSpline as us
from IPython import embed
import matplotlib.pyplot as plt

__author__ = 'Janez Presern'


class FitSpeed:

    def __init__(self, table_fn):

        self.calib_data = pd.read_csv(table_fn)
        self.spl = us(self.calib_data.pwm, self.calib_data.speed)#, s=s, k=k)
        self.pwm_range = np.arange(min(self.calib_data.pwm), max(self.calib_data.pwm) + 1, 1)
        self.y = self.spl(self.pwm_range)

    def look_up(self, pwm):

        return self.y[self.pwm_range == pwm]


if __name__ == "__main__":

    fs = FitSpeed("./kalibracije/kalibracija.csv")
    fs.look_up(500)

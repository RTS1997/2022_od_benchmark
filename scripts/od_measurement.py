
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from re import X

from ADCPi import ADCPi


# General settings
# adc0 sets channel where the raspberry pi and the adc board can communicate.
adc0 = ADCPi(0x68, 0x69, 12)

# Set ADC board channel
chan = 8

# Set experiment length in seconds (86400s = 24h)
duration = 86400

def write_results(timeor, voltage_value, bit_value, od_value=0):
        """Writes results to a csv file.
        Args:
            timeor: time of recording as int.
            voltage_value: raw voltage value as int.
            bit_value: raw bit value as int.
        Returns:
            csv file in the dist directory in the form of a pandas data frame.
        """

        # The ** unpacks the dictionaries and this makes it possible to combine them into one.
        pd.DataFrame({**timeor, **voltage_value, **bit_value, **od_value}).to_csv("test_od_script.csv")

current_time = time.perf_counter()
voltage_value = 0
bit_value = 0

while current_time < duration:
    voltage_value = adc0.read_voltage(chan)
    bit_value = adc0.read_raw(chan)
    write_results(current_time, voltage_value, bit_value)
    time.sleep(30)
    current_time = time.perf_counter()






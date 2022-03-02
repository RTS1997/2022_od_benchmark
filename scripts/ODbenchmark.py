from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
from ast import arg, parse
from email import parser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse
import pathlib
import time
import os

from ADCPi import ADCPi

# import the ADCPi module
# try:
#     from ADCPi import ADCPi
# except ImportError:
#     print("Failed to import ADCPi from python system path")
#     print("Importing from parent folder instead")
#     try:
#         import sys
#         sys.path.append('..')
#         from ADCPi import ADCPi
#     except ImportError:
#         raise ImportError(
#             "Failed to import library from parent folder")


# Create function that either shows plots or not

def plot_show(show_plot):
    if show_plot:
        plt.show()
    else:
        plt.close()

# Protects user from jubling up anything during imports
if __name__ == "__main__":
    print("yap")

    # Create all parameters that can be parsed by the command line.

    parser = argparse.ArgumentParser(
        description="OD measurement analysis"
    )
    parser.add_argument(
        "phototransistor",
        type=str,
        help="name of the phototransistor"
    )
    parser.add_argument(
        "diode",
        type=str,
        help="name of the light diode"
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="shows graphs"
    )
    parser.add_argument(
        "--dest",
        type=str,
        help="destination of graphs"
    )
    parser.add_argument(
        "--od_measurements",
        type=int,
        required=True,
        help="Number of od measurements"
    )
    parser.add_argument(
        "--ADCchannel",
        type=int,
        required=True,
        help="ADC channel used"
    )

    args = parser.parse_args()

    # Set ADC i2c addresses
    adc0 = ADCPi(0x68, 0x69, 12)
    # adc1 = ADCPi(0x6A, 0x6B, 12)
    # adc2 = ADCPi(0x6C, 0x6D, 12)
    # adc3 = ADCPi(0x6E, 0x6F, 12)

    # Create an array for each OD measurement
    voltage_array = np.zeros(args.od_measurements, dtype=float)
    bit_array = np.zeros(args.od_measurements, dtype=float)

    phototransistor = input("Enter phototransistor name or id (If you want to abort type: n):")

    if phototransistor != "n" and isinstance(phototransistor, str) == True:
        print("Well done")
        diode = input("Enter diode name or id (If you want to abort type: n):")
        if diode != "n" and isinstance(diode, str) == True:
            print("Well done 2")
            for number in range(0, args.od_measurements):
                solution_od = input("Add solution to reaction vessle and enter OD here(If you want to abort type: n):")
                if solution_od != "n" and isinstance(solution_od, str) ==True:
                    print("Solution is measured now!")
                    # voltage_array[number] = adc0.read_voltage(1)
                    # bit_array[number] = adc0.read_raw(1)
                    voltage_array[number] = 3
                    bit_array[number] = 4
                    time.sleep(0.2)
                    print(voltage_array, bit_array)
                else:
                    print("Experiment done or aborted, files are stored in 3")
            print("Experiment done!")
        else:
            print("Experiment done or aborted, files are stored in 2")
    else:
        print("Experiment done or aborted, files are stored in ")






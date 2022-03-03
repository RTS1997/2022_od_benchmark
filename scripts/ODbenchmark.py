from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
from ast import arg, parse
from email import parser
from heapq import merge
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse
import pathlib
import time
import os
import csv

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
        required=True,
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

    # Function that writes a file from a list and string name
    def write_results(bit_array, od_array, voltage_array):
        """Writes results to a csv file.

        Args:
            result_list: list of all results.
            header: string name as header for the list.

        Returns:
            list of all results to the --dest folder.

        """
        pd.DataFrame({**od_array, **bit_array, **voltage_array}).to_csv(args.dest+"/od_benchmark.csv")


    # Function that plots data from results
    def plot_results(od_label, dictkey):
        """Plots all results as a line plot for voltage and bit values.

            Plots are saved in the --dest folder.

            Args:
                result_list: list of all results.
                header: string name as header for the list.

            Returns:
                plot1: lineplot for all voltage results
                plot2: lineplot for all bit value results

        """
        # Voltage plot

        data_csv = pd.read_csv(args.dest+"/od_benchmark.csv")

        sns.set_theme()


        #print("od", od_array.keys(), "dc", dictkey.keys(), len(dictkey.keys()))
        # First plot
        for index in range(0, len(od_label.keys())):
            sns.lineplot(data = data_csv, x = list(od_label.keys())[index], y = list(dictkey.keys())[index])

        # data_formatter_dict = merge(results_list , {"od_values":od_values})
        # print("df",data_formatter_dict)

        # final_data_frame = pd.DataFrame.from_dict(data_formatter_dict)
        # print("final",final_data_frame)

        # for entry in

        # sns.set_theme()
        # sns.lineplot(data = final_data_frame, x = 'od_values', y = od_values.ke)


    phototransistor = input("Enter phototransistor name or id (If you want to abort type: n):")


    if phototransistor != "n" and isinstance(phototransistor, str) == True:
        print("Well done")
        diode = input("Enter diode name or id (If you want to abort type: n):")
        if diode != "n" and isinstance(diode, str) == True:

            # Create an array for each OD measurement
            voltage_array = {phototransistor+diode+"_voltage_array":np.zeros(args.od_measurements, dtype=float)}
            bit_array = {phototransistor+diode+"_bit_array":np.zeros(args.od_measurements, dtype=float)}
            od_array = {"OD"+str(phototransistor)+str(diode): np.zeros(args.od_measurements, dtype=float)}

            print("Well done 2")
            for number in range(0, args.od_measurements):
                solution_od = input("Add solution to reaction vessle and enter OD here(If you want to abort type: n):")
                if solution_od != "n" and isinstance(solution_od, str) == True:
                    print("Solution is measured now!")
                    voltage_array[phototransistor+diode+"_voltage_array"][number] = adc0.read_voltage(args.ADCchannel)
                    bit_array[phototransistor+diode+"_bit_array"][number] += adc0.read_raw(args.ADCchannel)
                    od_array["OD"+str(phototransistor)+str(diode)][number] = float(solution_od)
                    time.sleep(0.2)
                    print(voltage_array, bit_array, od_array)
                else:
                    print("Experiment done or aborted, files are stored in 3")
            print("Experiment done!")
        else:
            print("Experiment done or aborted, files are stored in 2")
    else:
        print("Experiment done or aborted, files are stored in ")


    # Write the results to a file in the destination folder
    write_results(bit_array, od_array, voltage_array)


    # Load and show plots
    if args.display == True:
        plot_results(od_array,voltage_array)
        plot_show('show_plot')
        plot_results(od_array,bit_array)
        plot_show('show_plot')
        # plot_results(bit_array, od_array)
        # plot_show('show_plot')
        # plot_results(voltage_array, od_array)
        # plot_show('show_plot')
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import argparse
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from email import parser

from re import X

from ADCPi import ADCPi

def plot_show(show_plot):
    """Function shows or closes plots

        Args:
            String 'show_plot'.
    """
    if show_plot:
        plt.show()
    else:
        plt.close()

# Protects user from jubling up anything during imports
if __name__ == "__main__":

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
            bit_array: directory of all bit value results.
            od_array: directory of OD values.
            voltage_array: directory of all recorded voltages.

        Returns:
            csv file in the dist directory in the form of a pandas data frame.

        """

        # The ** unpacks the dictionaries and this makes it possible to combine them into one.
        pd.DataFrame({**od_array, **bit_array, **voltage_array}).to_csv(args.dest+"/od_benchmark.csv")


    # Function that plots data from results
    def plot_results(od_label, dictkey, y_lab, x_lab="OD600"):
        """Plots all results as a line plot for voltage and bit values.

            Plots are saved in the --dest folder csv after the measurements are done.
            The od label and dictkey are used to find the correct columns within the csv file.

            Args:
                od_label: dictionary of all od values used during the run.
                dictkey: dictionary of all used values either bit or voltage.

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
            sns.lineplot(data = data_csv, x = list(od_label.keys())[index], y = list(dictkey.keys())[index], label = list(dictkey.keys())[index])

        plt.xlabel(x_lab)
        plt.ylabel(y_lab)
        plt.title("Calibration plot")
        plt.legend()
        plt.savefig(args.dest+"/"+y_lab+".svg")

    ### Experiment program

    experiment_switch = "YES"

    # set arrays

    voltage_array = {}
    bit_array = {}
    od_array = {}

    while experiment_switch.upper() == "YES":

        phototransistor = input("Enter phototransistor name or id (If you want to abort type: n):")

        if phototransistor != "n" and isinstance(phototransistor, str) == True:
            print("PHOTOTRANSISTOR ENTERED.")
            diode = input("Enter diode name or id (If you want to abort type: n):")
            if diode != "n" and isinstance(diode, str) == True:

                # Create an array for each OD measurement
                voltage_array[phototransistor+diode+"_voltage_array"] = np.zeros(args.od_measurements, dtype=float)
                bit_array[phototransistor+diode+"_bit_array"] = np.zeros(args.od_measurements, dtype=float)
                od_array["OD"+str(phototransistor)+str(diode)] = np.zeros(args.od_measurements, dtype=float)

                print("DIODE ENTERED.")
                for number in range(0, args.od_measurements):
                    solution_od = input("Add solution to reaction vessle and enter OD here(If you want to abort type: n):")
                    if solution_od != "n" and isinstance(solution_od, str) == True:
                        print("SOLUTION IS BEING MEASURED NOW!")
                        voltage_array[phototransistor+diode+"_voltage_array"][number] = adc0.read_voltage(args.ADCchannel)
                        bit_array[phototransistor+diode+"_bit_array"][number] += adc0.read_raw(args.ADCchannel)
                        od_array["OD"+str(phototransistor)+str(diode)][number] = float(solution_od)
                        time.sleep(0.2)
                        print(voltage_array, bit_array, od_array)
                    else:
                        print(f"Experiment done or aborted, files are stored in {args.dest}")

                experiment_switch = input("Do you want to continue the experiment? (Yes/No):")

                if experiment_switch.upper() != "NO" and experiment_switch.upper() != "YES":
                    print("Invalid answer was given!")
                    experiment_switch = input("Do you still want to continue the experiment? If answer is not Yes, experiment will abort! (Yes/No):")
                else:
                    continue
            else:
                print(f"Experiment done or aborted, files are stored in {args.dest}")
        else:
            print(f"Experiment done or aborted, files are stored in {args.dest}")


    # Write the results to a file in the destination folder
    if experiment_switch.upper() == "NO":
        write_results(bit_array, od_array, voltage_array)


    # Load and show plots
    if args.display == True and experiment_switch.upper() == "NO":
        plot_results(od_array,voltage_array, "Voltage in [mV]")
        plot_show('show_plot')
        plot_results(od_array,bit_array, "bits measured")
        plot_show('show_plot')

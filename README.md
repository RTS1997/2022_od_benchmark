# 2022_od_benchmark

To improve our morbidostat design, we try to find more sensitive OD measurement componenets. As a main hub, we are using a raspberry pi connected to an ADC (analog-to-digital converter board), which in turn is connected to the OD measuring components (IR diode and phototransistor). 

The script is automating the OD data acquisition and ploting the results for easy analysis.

This script uses the functionality of code provided by the ADP board manufacturer: https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/tree/master/ADCPi

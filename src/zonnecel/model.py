from zonnecel.arduino_device import list_devices, ArduinoVISADevice
import numpy as np

def show_devices():
    return list_devices()

class ZonnecelExperiment:
# Creating lists
    def __init__(self, port):
        self.device = ArduinoVISADevice(port)

    def scan(self, start, stop):
        """Run experiment with ADC inputs in range(start, stop)

        Args:
            start (int): ADC value where the experiment starts (0 - 1023)
            stop (int): ADC value where the experiment stops (0 - 1023)

        Return:
            lists of voltages and currents
        """        
        R2 = 4.7

        voltages = []
        currents = []
                
        for U0 in range (start,stop):
            self.device.set_output_value(U0)
            U1 = self.device.get_input_voltage(channel = 1) # spanningsmeter
            U2 = self.device.get_input_voltage(channel = 2) # stroommeter
            # U_zonnecel = 3 x U1
            voltages.append(3*U1)
            # I2 = U2 / R2
            currents.append(float(U2)/R2)

        # print(self.measurements.currents)
        return voltages, currents

    def repeat_scan(self, start, stop, n):
        U_n = []
        I_n = []

        """Repeat the experiment n times with ADC inputs in the range(start, stop) to calculate the currents mean and std

        Args:
            start (int): ADC value where the experiment starts (0 - 1023)
            stop (int): ADC value where the experiment stops (0 - 1023)
            n (int): number of times the experiment runs

        Returns:
            float: lists of floats, corresponding with the average voltage, average current and their standard deviation
        """        

        for i in range (n):
            U, I = self.scan(start, stop)
            U_n.append(U)
            I_n.append(I)

        return (np.mean(U_n,axis=0),np.mean(I_n,axis=0),
        np.std(U_n,axis=0)/np.sqrt(n),np.std(I_n,axis=0)/np.sqrt(n))
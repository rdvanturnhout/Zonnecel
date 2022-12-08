from controllers.arduino_device import list_devices, ArduinoVISADevice
import numpy as np

print(list_devices())


class ZonnecelExperiment:
# Creating lists
    def __init__(self, port):
        self.device = ArduinoVISADevice(port)
        self.voltages = []
        self.currents = []
        self.avg_voltages = []
        self.avg_currents = []
        self.std_voltages = []
        self.std_currents = []

    def scan(self, start, stop):
        """Run experiment with ADC inputs in range(start, stop)

        Args:
            start (int): ADC value where the experiment starts (0 - 1023)
            stop (int): ADC value where the experiment stops (0 - 1023)

        Return:
            lists of voltages and currents
        """        
        R2 = 4.7
                
        for U0 in range (start,stop):
            self.device.set_output_value(U0)
            U1 = self.device.get_input_value(channel = 1) # spanningsmeter
            U2 = self.device.get_input_value(channel = 2) # stroommeter
            # U_zonnecel = 3 x U1
            self.voltages.append(3*U1)
            # I2 = U2 / R2
            self.currents.append(float(U2)/R2)

        # print(self.measurements.currents)
        return self.voltages, self.currents

    def repeat_scan(self, start, stop, n):
        """Repeat the experiment n times with ADC inputsin the range(start, stop) to calculate the currents mean and std

        Args:
            start (int): ADC value where the experiment starts (0 - 1023)
            stop (int): ADC value where the experiment stops (0 - 1023)
            n (int): number of times the experiment runs

        Returns:
            float: lists of floats, corresponding with the average voltage, average current and their standard deviation
        """        

        for i in range (n):
            U, I = self.scan(start, stop)
            U_avg = np.mean(U)
            I_avg = np.mean(I)
            U_std = np.std(U)
            I_std = np.std(I)
            self.avg_voltages.append(U_avg)
            self.avg_currents.append(I_avg)
            self.std_voltages.append(U_std)
            self.std_currents.append(I_std)

        return (self.avg_voltages.append(U_avg), self.avg_currents.append(I_avg), 
                self.std_voltages.append(U_std), self.std_currents.append(I_std))
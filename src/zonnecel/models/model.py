from controllers.arduino_device import list_devices, ArduinoVISADevice

print(list_devices())


class ZonnecelExperiment:
# Creating lists
    def __init__(self, port):
        self.device = ArduinoVISADevice(port)
        self.voltages = []
        self.currents = []

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
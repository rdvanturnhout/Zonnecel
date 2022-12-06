from controllers.arduino_device import list_devices, ArduinoVISADevice

print(list_devices())

class DiodeExperiment:
# Creating lists
    def __init__(self, port):
        self.device = ArduinoVISADevice(port)

    def scan(self, start, stop):
        """Run experiment with ADC inputs in range(start, stop)

        Args:
            start (int): ADC value where the experiment starts (0 - 1023)
            stop (int): ADC value where the experiment stops (0 - 1023)


        """        
        R = 220
                
        for i in range (start,stop):
            self.device.set_output_value(i)
            U1 = 
            U2 = 
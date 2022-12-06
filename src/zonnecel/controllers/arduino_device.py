# Rick van Turnhout
# 10 - 11 - 2022

# Arduino Device

import pyvisa

def list_devices():
    # Resource Manager, Requesting a list of all available ports
    rm = pyvisa.ResourceManager("@py")
    return rm.list_resources()

def ADC_to_Voltage(ADC):
    """Get a voltage out of a ADC value
    Args:
        ADC (int): value between 0 - 1024
    Returns:
        float: Voltage
    """    # from bits to voltage
    ###Voltage = 3.3*device.query("OUT:CH0 1023")/1024
    Voltage = 3.3*int(ADC)/1024
    # print(Voltage)

    return float(Voltage)

class ArduinoVISADevice:
    """Controlling and measuring the device: give inputs en request output

    Args:
        value (int): ADS value between 0 - 1024 to input into device
        channel (int): number of channel to get ouput/input ADS from
    """
    def __init__(self, port):
        # Resourcemanager, accessing device
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(f"{port}", read_termination="\r\n", write_termination="\n")
        
        self.port = port

# Return connected port
    def get_identification(self):
        return self.port

    def set_output_value(self, value):
        """Set ouput value in ADC

        Args:
            value (int): ADC value (0 - 1023)
        """        
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        """Get ouput value in ADC

        Returns:
            int: ADC value (0 - 1023) 
        """        
        return self.device.query("MEAS:CH0?")
     
    def get_input_value(self, channel):
        """Get input value in ADC

        Args:
            channel (int): number of channel. We use 1 and 2

        Returns:
            int: ADC value (0 - 1023) in requested channel
        """        
        return self.device.query(f"MEAS:CH{channel}?")

    def get_input_voltage(self, channel):
        """Get input value in Voltage using the function ADC_to_Voltage

        Args:
            channel (int): number of channel. We use 1 and 2

        Returns:
            float: Voltage in requesting channel
        """        
        return ADC_to_Voltage(self.device.query(f"MEAS:CH{channel}?"))
from zonnecel.arduino_device import list_devices, ArduinoVISADevice
import numpy as np

def show_devices():
    return list_devices()

class ZonnecelExperiment:
# Creating lists
    def __init__(self, port):
        self.device = ArduinoVISADevice(port)

    def scan(self, start, stop):
        """Run experiment with ADC inputs in range(start, stop):
           Measure the voltage on the cel;
           the current on the circuit;
           the resistance on the variable resistor;
           and the power on the cel.

        Args:
            start (int): ADC value where the experiment starts (0 - 1023)
            stop (int): ADC value where the experiment stops (0 - 1023)

        Return:
            lists of voltages, currents, resistance and power
        """        
        R2 = 4.7

        voltages = []
        currents = []
        resistances = []
        powers = []
                
        for U0 in range (start,stop):
            self.device.set_output_value(U0)
            U1 = self.device.get_input_voltage(channel = 1) # spanningsmeter
            U2 = self.device.get_input_voltage(channel = 2) # stroommeter
            U_zonnecel = 3 * U1
            voltages.append(U_zonnecel)
            I = float(U2) / R2
            currents.append(I)

            U_var = 3*U1 - U2
            if I:
                R_var = U_var/I
            else:
                R_var = 10**7
            resistances.append(R_var)
            P_zonnecel = U_zonnecel * I
            powers.append(P_zonnecel)

        # print(self.measurements.currents)
        return voltages, currents, resistances, powers

    def repeat_scan(self, start, stop, n):
        U_n = []
        I_n = []
        R_n = []
        P_n = []

        """Repeat the experiment n times with ADC inputs in the range(start, stop) to calculate mean and std of:
                * Voltage on cel;
                * Current;
                * Resistance on variable resistor;
                * Power on cel.

        Args:
            start (int): ADC value where the experiment starts (0 - 1023)
            stop (int): ADC value where the experiment stops (0 - 1023)
            n (int): number of times the experiment runs

        Returns:
            float: lists of floats, corresponding with the average voltage, current, resistance, power and their standard deviation
        """        

        for i in range (n):
            U, I, R, P = self.scan(start, stop)
            U_n.append(U)
            I_n.append(I)
            R_n.append(R)
            P_n.append(P)

        return (np.mean(U_n,axis=0),np.mean(I_n,axis=0), np.mean(R_n,axis=0),np.mean(P_n,axis=0), 
        np.std(U_n,axis=0)/np.sqrt(n),np.std(I_n,axis=0)/np.sqrt(n), np.std(R_n,axis=0)/np.sqrt(n),np.std(P_n,axis=0)/np.sqrt(n))

    def max_power(self, R_list, P_list):
        """Get the maximum value out of the power list and its resistance

        Args:
            R_list (floats): list of resistances
            P_list (floats): list of powers

        Returns:
            float: maximum power and its resistance
        """         
        P_max = np.amax(P_list)
        return R_list[np.argmax(P_list)], P_max

from models.model import ZonnecelExperiment
import matplotlib.pyplot as plt

port = 'ASRL5::INSTR'
experiment = ZonnecelExperiment(port)

def run_experiment():
    U, I = experiment.scan(0, 1023)

    # plotting measurements 
    plt.fig_d1 = plt.figure('Plot Voltage and Current')
    # plt.plot(experiment.self.voltages , experiment.self.currents, '.')
    plt.plot(U , I, '.')
    # plt.errorbar( U, I, yerr = I_std, fmt = 'o', label = "LED with error")
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.legend(loc='upper right', shadow=True, ncol=1)

    plt.show()
             
run_experiment()
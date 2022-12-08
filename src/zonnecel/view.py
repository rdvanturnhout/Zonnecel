from zonnecel.model import ZonnecelExperiment
import matplotlib.pyplot as plt

port = 'ASRL5::INSTR'
experiment = ZonnecelExperiment(port)

def run_experiment():
    U, I, U_err, I_err = experiment.repeat_scan(0, 1023, 20)

    # plotting measurements 
    plt.fig_d1 = plt.figure('Plot Voltage and Current')
    # plt.plot(experiment.self.voltages , experiment.self.currents, '.')
    plt.plot(U , I, '.')
    plt.errorbar( U, I, xerr = U_err , yerr = I_err, fmt = 'o', label = "Cel with error")
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.legend(loc='upper right', shadow=True, ncol=1)

    plt.show()
             
run_experiment()
#grafical user interface application

import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from zonnecel.model import ZonnecelExperiment, show_devices
import pyqtgraph as pg
import pandas as pd
import numpy as np

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        """ Init function that builds the format of the graphical user interface and indicates what happens when buttons are clicked
        """        
        # roep de __init__() aan van de parent class
        super().__init__()

        # every QMainWindow needs a central widget
        # inside this widget you can add a layout and other widgets
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # add plot widget
        self.plot_widget = pg.PlotWidget()
        

        # add layouts and widgets
        vbox = QtWidgets.QVBoxLayout(central_widget)
        vbox.addWidget(self.plot_widget)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox2 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox2)
        hbox3 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox3)

        # buttons and text
        # first hbox and add min and max values
        self.startwlabel = QtWidgets.QLabel("Start:")
        hbox.addWidget(self.startwlabel) 
        self.startwaarde = QtWidgets.QDoubleSpinBox()
        hbox.addWidget(self.startwaarde)
        self.startwaarde.setMinimum(0)
        self.startwaarde.setMaximum(3.3)
        self.stopwlabel = QtWidgets.QLabel("Stop:")
        hbox.addWidget(self.stopwlabel)
        self.stopwaarde = QtWidgets.QDoubleSpinBox()
        hbox.addWidget(self.stopwaarde)
        self.stopwaarde.setMaximum(3.3)
        self.measurementslabel = QtWidgets.QLabel("Amount of measurements:")
        hbox.addWidget(self.measurementslabel) 
        self.measurements = QtWidgets.QSpinBox()
        hbox.addWidget(self.measurements)
        self.measurements.setMinimum(1)

        #second hbox
        add_start_button = QtWidgets.QPushButton("Do a measurement")
        hbox2.addWidget(add_start_button)
        add_save_button = QtWidgets.QPushButton("Save Data")
        hbox2.addWidget(add_save_button)
        
        # third hbox (ports)
        self.portlabel = QtWidgets.QLabel("Add port you want to use:")
        hbox3.addWidget(self.portlabel)
        self.add_port_choise = QtWidgets.QComboBox()
        self.add_port_choise.addItems(show_devices())
        hbox3.addWidget(self.add_port_choise)
        
        # set initial values
        self.startwaarde.setValue(0)
        self.stopwaarde.setValue(3.3)
        self.measurements.setValue(1)

        #signals
        add_start_button.clicked.connect(self.plot)
        add_save_button.clicked.connect(self.save_data)

        # intitial lists
        self.I = []
        self.U = []
        self.U_err = []
        self.I_err = []



    @Slot()
    def plot(self):
        """Plots data with the variables that are currently in the boxes/buttons
        """        
        self.plot_widget.clear()
        experiment = ZonnecelExperiment(port = self.add_port_choise.currentText())
        self.U, self.I, self.U_err, self.I_err = experiment.repeat_scan(int(self.startwaarde.value()/3.3*1024), int(self.stopwaarde.value()/3.3*1024), self.measurements.value())
        
        
        #plotting
        error = pg.ErrorBarItem()
        error.setData(x = np.array(self.U), y = np.array(self.I), top = np.array(self.I_err), bottom = np.array(self.I_err), left = np.array(self.U_err), right = np.array(self.U_err))
        self.plot_widget.addItem(error)
        self.plot_widget.plot(self.U, self.I, symbol = "o", pen = None, symbolSize = 5, SymbolBrush = "b", symbolPen = "k")
        self.plot_widget.setLabel("left", "current (A)")
        self.plot_widget.setLabel("bottom", "voltage (V)")
        self.plot_widget.setTitle("Current against voltage graph")
    
    def save_data(self):
        """Saves data as a csv file that the user can name themselves
        """        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        pd.DataFrame(np.array(self.IU_list)).to_csv(filename) # hiermee verder


def main():
    """ Making instance of the QtWidgets.QApplication and our own class, call method show and making sure error is shown when something goes wrong
    """    
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
             
 
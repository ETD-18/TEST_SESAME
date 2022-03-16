import time
import pyvisa

class DMM34401A:
    def __init__(self, ress):
        self.ress = ress
        ress.write("SYSTEM:REMOTE")
        ress.write("*CLS")
 
    def check(self, role, name, port):
        rep = self.ress.query("*IDN?")
        rep = rep.strip()
        if (rep == name):
            print("The " + role + " is connected on the port " + port)
        else:
            print("The " + role + " is not connected on the port " + port)
            exit() #abortProcedure()

    def measureVoltage(self):
        """Measuring the voltage on the DMM"""
        self.ress.write("MEAS:VOLT:DC?")
        voltage = self.ress.read()
        voltage = voltage.strip()
        return float(voltage)

    def measureCurrent(self):
        """Measuring the current on the DMM"""
        self.ress.write("MEAS:CURR:DC?")
        current = self.ress.read()
        current = current.strip()
        return float(current)



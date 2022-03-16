import time
import pyvisa

class PSUHMP4030:
    def __init__(self, ress):
        self.ress = ress
        #ress.write("*IDN?")
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
    
    def disableOut(self):
        self.ress.write("OUTP:GEN OFF")

    def enableOut(self):
        self.ress.write("OUTP:GEN ON")

    def enableChannel(self, channel):
        c = self.genDriverChannel(channel)
        self.ress.write(c)
        self.ress.write("OUTP:SEL 1")

    def disableChannel(self, channel):
        c = self.genDriverChannel(channel)
        self.ress.write(c)
        self.ress.write("OUTP:SEL 0")

    def alertBeep(self):
        """Nice tree beeps to alert my human"""
        self.ress.write("SYST:BEEP")
        time.sleep(0.7)
        self.ress.write("SYST:BEEP")
        time.sleep(0.7)
        self.ress.write("SYST:BEEP")
        time.sleep(0.7)

    def genDriverChannel(self, channel):
        if (channel >= 1 and channel <= 3):
            return "INST OUT" + str(channel)
        else:
            print("Channel " + str(channel) + " is invalid")
            self.disableOut()
            exit() #abortProcedure()

    def measureVoltage(self, channel):
        """Here we measure the voltage of the power supply for a given channel"""
        c = self.genDriverChannel(channel)
        self.ress.write(c)
        self.ress.write("MEAS:VOLT?")
        voltage = self.ress.read()
        voltage = voltage.strip()
        return (float(voltage))

    def measureCurrent(self, channel):
        """Here we measure the current of the power supply for a given channel"""
        c = self.genDriverChannel(channel)
        self.ress.write(c)
        self.ress.write("MEAS:CURR?")
        current = self.ress.read()
        current = current.strip()
        return (float(current))

    def setVoltage(self, channel, voltage):
        c = self.genDriverChannel(channel)
        self.ress.write(c)
        self.ress.write("VOLT " + str(voltage))

    def setCurrent(self, channel, voltage):
        c = self.genDriverChannel(channel)
        self.ress.write(c)
        self.ress.write("CURR " + str(voltage))

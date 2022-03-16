import pyvisa
import signal
import time
import json

import PSUHMP4030, DMM34401A, DMM3146A
import genGraph

def quitHandler(signum, frame): #done
    print("Quitting...")
    abortProcedure()

def abortProcedure(): #done
    """Something went wrong abort and power off the power supply"""
    PSUHMP4030.disableOut(alim)
    exit()

def checkSystems():  #done
    """Is everything connected ??"""
    print("Checking for equipment")
    repA = alim.query("*IDN?")
    repA = repA.strip()
    print("Alim : \"" + repA + "\"")
    if (repA == "HAMEG,HMP4030,019480198,HW50020001/SW2.30"):
        print("The power supply is connected")
    else:
        print("The power supply is not on the port USB0")
        abortProcedure()
    time.sleep(0.5)
    
    repMV = multVoltageIn.query("*IDN?")
    repMV = repMV.strip()
    print("Voltage multimeter : \"" + repMV + "\"")
    if (repMV == "HEWLETT-PACKARD,34401A,0,11-5-3"):
        print("The voltage multimeter is connected")
    else:
        print("The voltage multimeter is not on the port USB1")
        abortProcedure()
    time.sleep(0.5)

    repMC = multCurrentOut.query("*IDN?")
    repMC = repMC.strip()
    print("Current multimeter : \"" + repMC + "\"")
    if (repMC == "HEWLETT-PACKARD,34401A,0,10-5-2"):
        print("The current multimeter is connected")
    else:
        print("The current multimeter is not on the port USB2")
        abortProcedure()
    time.sleep(0.5)

    ###TODO: check for the escort crappy DMM, maybe with the RV command ??


signal.signal(signal.SIGINT, quitHandler)
rm = pyvisa.ResourceManager()
rm.list_resources()

alim = rm.open_resource('ASRL/dev/ttyUSB0::INSTR')
multVoltageIn = rm.open_resource('ASRL/dev/ttyUSB1::INSTR')
multVoltageOut = rm.open_resource('ASRL/dev/ttyUSB2::INSTR')
multCurrentOut = rm.open_resource('ASRL/dev/ttyUSB3::INSTR')

rm = pyvisa.ResourceManager()
rm.list_resources()

alim = PSUHMP4030.PSUHMP4030(rm.open_resource('ASRL/dev/ttyUSB0::INSTR'))
vinDMM = DMM34401A.DMM34401A(rm.open_resource('ASRL/dev/ttyUSB1::INSTR'))
voutDMM = DMM34401A.DMM34401A(rm.open_resource('ASRL/dev/ttyUSB2::INSTR'))
IoutDMM = DMM3146A.DMM3146A(rm.open_resource('ASRL/dev/ttyUSB3::INSTR'))

alim.write("SYSTEM:REMOTE")
time.sleep(0.5)
multVoltageOut.write("SYSTEM:REMOTE")
time.sleep(0.5)
multVoltageOut.write("SYSTEM:REMOTE")
time.sleep(0.5)
#cant do system remote for the multCurrentOut bc its a crappy dmm

checkSystems()

#ch1 = electronic load
alim.write("OUTP:GEN OFF")
alim.write("INST OUT1")
alim.write("VOLT 1")
alim.write("CURR 0.250")

#ch2 = Vin
alim.write("INST OUT2")
alim.write("VOLT 5")
alim.write("CURR 10")

#ch3 = PID setpoint
alim.write("INST OUT3")
alim.write("VOLT 0.1")
alim.write("CURR 0.1")

PSUHMP4030.alertBeep(alim)

alim.write("OUTP:GEN ON")

setPointStep = 10 #in mV
baseSetPoint = 1000 #in mV
finalSetPoint = 1500 #in mV
currentSetPoint = baseSetPoint

setPointSteps = []
currentInSteps = []
currentOutSteps = []
voltageInSteps = []
voltageOutSteps = []
powerInSteps = []
powerOutSteps = []
efficiencySteps = []


setPointIStep = 10 #in mV
baseSetPointI = 1000 #in mV
finalSetPointI = 1500 #in mV
currentSetPointI = baseSetPointI

while currentSetPointI < finalSetPointI:
    alim.write("INST OUT3")
    alim.write("VOLT %f" % (currentSetPoint/1000))
    setPointSteps.append(currentSetPoint/1000)

    voltageIn = DMM34401A.measureVoltage(multVoltageIn)
    currentIn = PSUHMP4030.measureCurrentAlim(alim, 2)

    voltageOut = DMM34401A.measureVoltage(multVoltageOut)
    currentOut = DMM3146A.measureCurrent(multCurrentOut)
    
    powerIn = voltageIn * currentIn
    powerOut = voltageOut * currentOut
    efficiency = powerOut / powerIn

    print("=====================================")
    print("SetPoint = " + str(currentSetPoint) + "mV")
    print("Voltage IN  " + str(voltageIn) + " V | Current IN  " + str(currentIn) + " A | Power IN  " + str(powerIn) + " W")
    print("Voltage OUT " + str(voltageOut) + " V | Current OUT " + str(currentOut) + " A | Power OUT " + str(powerOut) + " W")
    print("Efficiency " + str(efficiency) + " %")

    currentInSteps.append(currentIn)
    currentOutSteps.append(currentOut)
    voltageInSteps.append(voltageIn)
    voltageOutSteps.append(voltageOut)
    powerInSteps.append(powerIn)
    powerOutSteps.append(powerOut)
    efficiencySteps.append(efficiency)
    
    currentSetPointI += setPointIStep
    time.sleep(1.0)

PSUHMP4030.disableOut(alim)
genGraph.effIout(currentOutSteps, efficiencySteps)
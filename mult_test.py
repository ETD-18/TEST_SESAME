# - *- coding: utf- 8 - *-
import pyvisa
import time
import git
import signal
import DMM34401A, DMM3146A, PSUHMP4030
import genGraph
import csv

setPointISteps = []
setPointSteps = []
currentInSteps = []
currentOutSteps = []
voltageInSteps = []
voltageOutSteps = []
powerInSteps = []
powerOutSteps = []
efficiencySteps = []

dataSetsTotal = []
testContinue = True

def quitHandler(signum, frame):
    print("Quitting...")
    global testContinue
    testContinue = False

def abortProcedure():
    """Something went wrong abort and power off the power supply"""
    alim.disableOut()
    time.sleep(2.0)
    exit()

def header():
    print("  █████████   █████                ██████     ██████     █████     ████████")
    print(" ███░░░░░███ ░░███                ███░░███   ███░░███  ███░░░███  ███░░░░███")
    print("░███    ░░░  ███████    ██████   ░███ ░░░   ░███ ░░░  ███   ░░███░░░    ░███")
    print("░░█████████ ░░░███░    ███░░███ ███████    ███████   ░███    ░███   ███████ ")
    print(" ░░░░░░░░███  ░███    ░███████ ░░░███░    ░░░███░    ░███    ░███  ███░░░░  ")
    print(" ███    ░███  ░███ ███░███░░░    ░███       ░███     ░░███   ███  ███      █")
    print("░░█████████   ░░█████ ░░██████   █████      █████     ░░░█████░  ░██████████")
    print(" ░░░░░░░░░     ░░░░░   ░░░░░░   ░░░░░      ░░░░░        ░░░░░░   ░░░░░░░░░░ ")
    print("Sesame Tester Efficient Figure Fabricator (ver.) 02")
    repo = git.Repo(search_parent_directories=True)
    print("Commit " + str(repo.git.rev_parse(repo.head.object.hexsha, short=6)) + "\n")

def checkSystems(): 
    """Is everything connected ??"""
    print("Checking for equipment")

    alim.check("power supply", "HAMEG,HMP4030,019480198,HW50020001/SW2.30", "USB0")
    time.sleep(0.5)
    VinDMM.check("voltage IN DMM", "HEWLETT-PACKARD,34401A,0,11-5-3", "USB1")
    time.sleep(0.5)
    VoutDMM.check("voltage OUT DMM", "HEWLETT-PACKARD,34401A,0,10-5-2", "USB2")
    time.sleep(0.5)
    IoutDMM.check("current OUT DMM", "TODO", "USB3")
    time.sleep(0.5)
    print()

def currentSetpointIncrease(dataset, baseSetPointI, finalSetPointI, setPointIStep):
    runContinue = True
    currentSetPointI = baseSetPointI
    alim.enableOut()
    while (currentSetPointI <= finalSetPointI and testContinue == True and runContinue == True):
        alim.setVoltage(1, float(currentSetPointI/1000))
        setPointISteps.append(currentSetPointI/1000)

        voltageIn = VinDMM.measureVoltage()
        currentIn = alim.measureCurrent(2)

        voltageOut = VoutDMM.measureVoltage()
        currentOut = IoutDMM.measureCurrent()
        #currentOut = IoutDMM.measureCurrentAvrg(3) worse
        
        if (currentIn > 9.9):
            runContinue = False
            print("Power supply cant keep up")
        else:
            powerIn = voltageIn * currentIn
            powerOut = voltageOut * currentOut
            efficiency = round(powerOut / (powerIn + 0.000000001), 3)

            print("=====================================")
            print("SetPoint electronic load = " + str(currentSetPointI) + "mV")
            print("Voltage IN  " + str(voltageIn) + " V  | Current IN  " + str(currentIn) + " A  | Power IN  " + str(powerIn) + " W")
            print("Voltage OUT " + str(voltageOut) + " V | Current OUT " + str(currentOut) + " A | Power OUT " + str(powerOut) + " W")
            print("Efficiency " + str(efficiency) + " %")

            if (efficiency < 1 and efficiency > 0):
                dataset["currentInSteps"].append(currentIn)
                dataset["currentOutSteps"].append(currentOut)
                dataset["voltageInSteps"].append(voltageIn)
                dataset["voltageOutSteps"].append(voltageOut)
                dataset["powerInSteps"].append(powerIn)
                dataset["powerOutSteps"].append(powerOut)
                dataset["efficiencySteps"].append(efficiency)
            else:
                print("The data is wrong, abort")
                runContinue = False
            currentSetPointI += setPointIStep
            #time.sleep(1.0)    
    alim.disableOut()
    #return dataset

def measureVout(setPointI):
    alim.setVoltage(1, float(setPointI/1000))
    alim.enableOut()
    time.sleep(2.0)
    voltageOut = VoutDMM.measureVoltage()
    alim.disableOut()
    return voltageOut


def senario():
    setPointStep = 250 #in mV
    baseSetPoint = 1000 #in mV
    finalSetPoint = 2000 #1500 #in mV
    currentSetPoint = baseSetPoint

    setPointIStep = 25#25 #in mV
    baseSetPointI = 200 #in mV
    finalSetPointI = 10000 #10000 #in mV
    currentSetPointI = baseSetPointI
    
    Vin = 5.0
    alim.disableOut()

    #Electronic load
    alim.enableChannel(1)
    alim.setVoltage(1, 1.0)
    alim.setCurrent(1, 0.250)

    #IN
    alim.enableChannel(2)
    alim.setVoltage(2, Vin)
    alim.setCurrent(2, 10.0)

    #PID setpoint
    alim.enableChannel(3)
    alim.setVoltage(3, (baseSetPoint/1000))
    alim.setCurrent(3, 0.1)

    alim.alertBeep()
    runNbr = 1
    while (currentSetPoint <= finalSetPoint and testContinue == True):
        alim.setVoltage(3, float(currentSetPoint/1000))
        runDataSet = {"runName" : "default name", "mode" : "Boost D->G", "VIN" : Vin, "VOUT" : round(measureVout(baseSetPointI), 1), "setPointISteps" : [], "setPointSteps" : [], "currentInSteps" : [], "currentOutSteps" : [], 
    "voltageInSteps" : [], "voltageOutSteps" : [], "powerInSteps" : [], "powerOutSteps": [], "efficiencySteps" : []}
        print("#####################################################################")
        runName = "RUN #" + str(runNbr) + " PID SetPoint : " + str(currentSetPoint/1000) + " : Vin " + str(Vin) + " Vout : " + str(runDataSet["VOUT"])
        print(runName)
        runDataSet["runName"] = runName

        currentSetpointIncrease(runDataSet, baseSetPointI, finalSetPointI, setPointIStep)
        dataSetsTotal.append(runDataSet)

        currentSetPoint += setPointStep
        runNbr = runNbr + 1
        time.sleep(3.0)
    print(dataSetsTotal)
    genGraph.effIout(dataSetsTotal, False)
    time.sleep(3.0)
    print(dataSetsTotal)
    genGraph.effIout(dataSetsTotal, True)


#voltageIn = DMM34401A.measureVoltage(my_instrument)
#print(str(voltageIn))

signal.signal(signal.SIGINT, quitHandler)
header()
rm = pyvisa.ResourceManager()
alim = PSUHMP4030.PSUHMP4030(rm.open_resource('ASRL/dev/ttyUSB0::INSTR'))
VinDMM = DMM34401A.DMM34401A(rm.open_resource('ASRL/dev/ttyUSB1::INSTR'))
VoutDMM = DMM34401A.DMM34401A(rm.open_resource('ASRL/dev/ttyUSB2::INSTR'))
IoutDMM = DMM3146A.DMM3146A(rm.open_resource('ASRL/dev/ttyUSB3::INSTR'))

checkSystems()
senario()

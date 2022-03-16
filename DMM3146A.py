import time
import pyvisa

class DMM3146A:
    def __init__(self, ress):
        self.ress = ress

    def check(self, role, name, port):
        #rep = self.ress.query("RV?")
        #rep = rep.strip()
        #TODO: finish this
        if ("TODO" == name):
            print("The " + role + " is connected on the port " + port)
        else:
            print("The " + role + " is not connected on the port " + port)
            exit() #abortProcedure()
    
    def readScreen(self, screen = 1):
        if (screen == 1 or screen == 2):
            self.ress.query("R" + str(screen))
            val = self.ress.read()
            self.ress.read() #empty the return of the command
            val = val.strip()
            return val
        else:
            print("Invalid screen choosen in for the 3146A DMM")
            exit()
            #abortProcedure()

    def measureVoltage(self):
        """Special function for the 3146A"""
        self.ress.query("S100") #DCV auto range
        self.ress.read()
        time.sleep(2)
        return float(self.readScreen(1))

    def measureCurrent(self):
        """Special function for the 3146A"""
        self.mode = 1
        self.ress.query("S147") #DCA max range
        val = self.ress.read()
        time.sleep(2.0)
        return float(self.readScreen(1))
    
    def removeHighestLowest(self, list):
        list.remove(max(list))
        list.remove(min(list))
        return list
    
    def measureCurrentAvrg(self, nbrReadings):
        samples = []
        for x in range(nbrReadings):
            print("aq " + str(x))
            samples.append(self.measureCurrent())

        print(*samples)

        if (nbrReadings > 3):
            samples = self.removeHighestLowest()
        
        avg = sum(samples)/len(samples)
        print("Average " + str(avg))
        return avg
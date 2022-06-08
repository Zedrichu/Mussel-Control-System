#PID controller

# r is the desired temperature
# v output system temp
# e array of tracking errors
class PIDControl:
    def __init__(self, rtemp, vtemp):
        self.r = rtemp
        self.v = vtemp
        self.e = [rtemp-vtemp] 

    def setProportional(self, value):
        self.P = value
        
    def setIntegral(self, value):
        self.I = value

    def setDerivative(self, value):
        self.D = value
    
    #Influcenced by slides of PID update
    def update(self, newTemp):
        self.e.append(self.r - newTemp)
        self.v = newTemp
        Pterm = self.P * self.e[-1] # Et
        Iterm = self.I * sum(self.e)
        Dterm = self.D * (self.e[-1] - self.e[-2])
        u = Pterm + Iterm + Dterm
        return u
    
    
    
            

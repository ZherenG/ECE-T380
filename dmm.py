class dmm:
    # Constructor
    def __init__(self, Resource_Manager, DMM_VISA_ADDRESS):
        self.rm = Resource_Manager
        self.dmm_handle = None
        self.connectstatus = False
        self.visa_address = DMM_VISA_ADDRESS
    
    # Function to connect computer to power supply    
    def connect(self):
        if self.connectstatus == False:
            try:
                self.dmm_handle = self.rm.open_resource(self.visa_address)
                self.dmm_handle.read_termination = '\n'
                self.dmm_handle.write_termination = '\n'
            except Exception:
                print("Unable to Connect to DMM at " + 
                      str(self.visa_address))
                #sys.exit()
                return False
            print("Successfully Connected to DMM")
            self.dmm_handle.timeout = 10000
            self.dmm_handle.clear()
            self.connectstatus = True
        else:
            print("Device already connected")
        return self.dmm_handle
    
    # Function to disconnect computer from power supply
    def disconnect(self):
        if self.connectstatus == True:
            self.dmm_handle.clear()
            self.dmm_handle.close()
            self.dmm_handle = None
            self.connectstatus = False
            print("Device Successfully Disconnected")
            return True
        else:
            print("Device not Connected")
            return False
    
    # Function to reset power supply    
    def reset(self):
        self.dmm_handle.write("*RST")
        return
    
    # Function to wait until all commands are caught up
    def wait(self):
        self.dmm_handle.write("*WAI")
        return
    def identity(self):
        # *OPC?
        name = (self.dmm_handle.query("*IDN?"))
        print(name)
        return
    def single_or_dual(self, mode, meas1, meas2):
        if mode == 0:
            self.dmm_handle.write("CONF:PRIM:" + meas1)
            self.dmm_handle.write("INIT")
            self.dmm_handle.write("FETC?") # Works
            
        if mode == 1:
            self.dmm_handle.write("CONF:PRIM:" + meas1)
            self.dmm_handle.write("CONF:SEC:" + meas2)
            self.dmm_handle.write("INIT") #try colon in front of init
            self.dmm_handle.write("FETC?")
            self.dmm_handle.query("*OPC?")
            
    def voltage_reading(self, channel):
        if channel == 0:
            voltage = (self.dmm_handle.query("MEAS:PRIM:VOLT:DC?"))
            print(voltage)
        if channel == 1:
            voltage = (self.dmm_handle.query("MEAS:SEC:VOLT:DC?")) 
            print(voltage)      
        return voltage
    def current_reading(self, channel):
        if channel == 0:
            current = (self.dmm_handle.query("MEAS:PRIM:CURR:DC?"))
            print(current)
        if channel == 1:
            current = (self.dmm_handle.query("MEAS:SEC:CURR:DC?"))
            print(current)
        return current
    def Diode_cont(self):
        # TODO: Finish
        return
    def resistance(self, channel):
        resistance = (self.dmm_handle.query("MEAS:RES?"))
        print(resistance)
        return resistance
    def capacitance(self):
        capacitance = (self.dmm_handle.query("MEAS:CAP?"))
        print(capacitance)
        return capacitance

        

    
    
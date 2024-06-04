class wave:
    # Constructor
    def __init__(self, Resource_Manager, wave_VISA_ADDRESS):
        self.rm = Resource_Manager
        self.wave_handle = None
        self.connectstatus = False
        self.visa_address = wave_VISA_ADDRESS
    
    def connect(self):
        if self.connectstatus == False:
            try:
                self.wave_handle = self.rm.open_resource(self.visa_address)
                self.wave_handle.read_termination = '\n'
                self.wave_handle.write_termination = '\n'
            except Exception:
                print("Unable to Connect to wave at " + 
                      str(self.visa_address))
                #sys.exit()
                return False
            print("Successfully Connected to wave")
            self.wave_handle.timeout = 10000
            self.wave_handle.clear()
            self.connectstatus = True
        else:
            print("Device already connected")
        return self.wave_handle
    
    def disconnect(self):
        if self.connectstatus == True:
            self.wave_handle.clear()
            self.wave_handle.close()
            self.wave_handle = None
            self.connectstatus = False
            print("Device Successfully Disconnected")
            return True
        else:
            print("Device not Connected")
            return False
    
    def reset(self):
        self.wave_handle.write("*RST")
        return
    
    # Function to wait until all commands are caught up
    def wait(self):
        self.wave_handle.write("*WAI")
        return
    def identity(self):
        # *OPC?
        name = (self.wave_handle.query("*IDN?"))
        print(name)
        return
            
    def high_z(self):
        self.wave_handle.write("OUTPUT:LOAD INF")
    def square_wave(self):
        self.wave_handle.write("APPL:SQU")
        self.wave_handle.write("VOLT:UNIT VPP")
        self.wave_handle.write("VOLT 5")
        self.wave_handle.write("FREQ 5000")
        self.wave_handle.write("FUNC:SQU:DCYCL 40")
        self.wave_handle.write("VOLT:OFFS 2.5")
        
    def output(self, val):
        if val == 1:
            self.wave_handle.write("OUTP ON")
        if val == 0:
            self.wave_handle.write("OUTP OFF")
    
    def clear(self):
        self.wave_handle.write("DISPLAY:CLE")
    # def burst_config(self):
    #     self.wave_handle.write("BURS:MODE TRIG") # triggerd Burst Mode
    #     self.wave_handle.write("BURS:NCYC 1") #count of 1
    #     self.wave_handle.write("BURS:INT:PER 0.02") # 20 ms
    #     self.wave_handle.write("TRIG:SOUR IMM") # trigger source 1
    #     self.wave_handle.write("OUTP:TRIG ON")

    # def gen_burst(self):
    #     self.wave_handle.write("*TRG")

    #set up burst characteristics
    def burst_characteristics(self):
       # Set the burst count to 1 cycle
        self.wave_handle.write('BURS:NCYC 1')
        # Set the burst period to 20 ms
        self.wave_handle.write('BURS:INT:PER 20e-3')
        
        return

    #Triggers WFG 
    def trigger(self):
        self.wave_handle.write("BURS:MODE TRIG")
        self.wave_handle.write("TRIG:SOUR:IMM")  #Maybe, This might be TRIG:SOUR:IMM
        self.wave_handle.write("*TRG")
        #self.wave_handle.write(":RUN") 
        self.wave_handle.write("OUTP:TRIG ON")

        self.wave_handle.write('BURS:STATe ON')  # Turn on output
        return

  
        
        

    
    
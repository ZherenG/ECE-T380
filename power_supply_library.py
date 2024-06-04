class power_supply:
    # Constructor
    def __init__(self, Resource_Manager, PS_VISA_ADDRESS):
        self.rm = Resource_Manager
        self.ps_handle = None
        self.connectstatus = False
        self.visa_address = PS_VISA_ADDRESS
    
    # Function to connect computer to power supply    
    def connect(self):
        if self.connectstatus == False:
            try:
                self.ps_handle = self.rm.open_resource(self.visa_address)
                self.ps_handle.read_termination = '\n'
                self.ps_handle.write_termination = '\n'
            except Exception:
                print("Unable to Connect to Power Supply at " + 
                      str(self.visa_address))
                #sys.exit()
                return False
            print("Successfully Connected to Power Supply")
            self.ps_handle.timeout = 10000
            self.ps_handle.clear()
            self.connectstatus = True
        else:
            print("Device already connected")
        return self.ps_handle
    
    # Function to disconnect computer from power supply
    def disconnect(self):
        if self.connectstatus == True:
            self.ps_handle.clear()
            self.ps_handle.close()
            self.ps_handle = None
            self.connectstatus = False
            print("Device Successfully Disconnected")
            return True
        else:
            print("Device not Connected")
            return False
    
    # Function to reset power supply    
    def reset(self):
        self.ps_handle.write("*RST")
        return
    
    # Function to wait until all commands are caught up
    def wait(self):
        self.ps_handle.write("*WAI")
        return
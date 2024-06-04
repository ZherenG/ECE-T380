class scope:
    # Constructor
    def __init__(self, Resource_Manager, SCOPE_VISA_ADDRESS):
        self.rm = Resource_Manager
        self.scope_handle = None
        self.connectstatus = False
        self.visa_address = SCOPE_VISA_ADDRESS
    
    # Function to connect computer to power supply    
    def connect(self):
        if self.connectstatus == False:
            try:
                self.scope_handle = self.rm.open_resource(self.visa_address)
                self.scope_handle.read_termination = '\n'
                self.scope_handle.write_termination = '\n'
            except Exception:
                print("Unable to Connect to scope at " + 
                      str(self.visa_address))
                #sys.exit()
                return False
            print("Successfully Connected to scope")
            self.scope_handle.timeout = 10000
            self.scope_handle.clear()
            self.connectstatus = True
        else:
            print("Device already connected")
        return self.scope_handle
    
    # Function to disconnect computer from power supply
    def disconnect(self):
        if self.connectstatus == True:
            self.scope_handle.clear()
            self.scope_handle.close()
            self.scope_handle = None
            self.connectstatus = False
            print("Device Successfully Disconnected")
            return True
        else:
            print("Device not Connected")
            return False
    
    # Function to reset power supply    
    def reset(self):
        self.scope_handle.write("*RST")
        return
    
    # Function to wait until all commands are caught up
    def wait(self):
        self.scope_handle.write("*WAI")
        return
    def identity(self):
        # *OPC?
        name = (self.scope_handle.query("*IDN?"))
        print(name)
        return
    def autoscale(self):
        self.scope_handle.write(":AUToscale")
        return
    def clear(self):
        self.scope_handle.write(":MEASure:CLEar")
    def channel(self, status, display):
        if(status == "on"):
            if(display == 1):
                self.scope_handle.write(":VIEW CHANnel1")
            elif(display == 2):
                self.scope_handle.write(":VIEW CHANnel2")
        elif(status == "off"):
            if(display == 1):
                self.scope_handle.write(":BLANk CHANnel1")
            elif(display == 2):
                self.scope_handle.write(":BLANk CHANnel1")

       
    def run(self):
        self.scope_handle.write(":RUN")
    def stop(self):
        self.scope_handle.write(":STOP")
    def single(self):
        self.scope_handle.write(":SINGLE")
# Performs data transfer of channel(s) via binary transfer
    def get_waveform_binary(self,channel=1):
        self.scope_handle.write(f':WAV:SOUR CHAN{channel}')
        self.scope_handle.write(f':WAV:FORM BYTE')
        self.scope_handle.write(f':WAV:BYT LSBF')
        self.scope_handle.query('*OPC?')
        values = self.scope_handle.query_binary_values(':WAV:DATA?', 
                                                     datatype='B',
                                                     header_fmt='ieee',
                                                     expect_termination = True,
                                                     is_big_endian=False)
        xinc = float(self.scope_handle.query(':WAV:XINC?'))
        xor = float(self.scope_handle.query(':WAV:XOR?'))
        xref = float(self.scope_handle.query(':WAV:XREF?'))
        yinc = float(self.scope_handle.query(':WAV:YINC?'))
        yor = float(self.scope_handle.query(':WAV:YOR?'))
        yref = float(self.scope_handle.query(':WAV:YREF?'))
        self.scope_handle.query('*OPC?')
        times = [xor + i*xinc for i in range(len(values))]
        volts = [(values[i]-yref)*yinc+yor for i in range(len(values))]
        return times,volts
    
    #Performs data transfer of channel(s) via ASCII transfer
    def get_waveform_ascii(self,channel=1):
        self.scope_handle.write(f':WAV:SOUR CHAN{channel}')
        self.scope_handle.write(f':WAV:FORM ASC')
        self.scope_handle.query('*OPC?')
        values = self.scope_handle.query(':WAV:DATA?')
        values = values[10:]
        values = values.split(',')
        xinc = float(self.scope_handle.query(':WAV:XINC?'))
        xor = float(self.scope_handle.query(':WAV:XOR?'))
        xref = float(self.scope_handle.query(':WAV:XREF?'))
        yinc = float(self.scope_handle.query(':WAV:YINC?'))
        yor = float(self.scope_handle.query(':WAV:YOR?'))
        yref = float(self.scope_handle.query(':WAV:YREF?'))
        self.scope_handle.query('*OPC?')
        times = [xor + i*xinc for i in range(len(values))]
        volts = [float(x) for x in values]
        return times,volts

    #Perform screen capture of display in BMP format
    def screen_capture(self,filename='test', format='BMP', palette = 'COL',
                       inksaver = 'OFF'):
        self.scope_handle.write(f':HARD:INKS {inksaver}')
        self.scope_handle.query("*OPC?")
        confstr = f':DISP:DATA? {format},{palette}'
        data = self.scope_handle.query_binary_values(confstr, 
                                                    datatype='B',
                                                    header_fmt='ieee',
                                                    expect_termination = True,
                                                    is_big_endian=False)
        if "PNG" in format:
            f = open(f'{filename}.png',"wb")
        else:
            f = open(f'{filename}.bmp',"wb")
        f.write(bytes(data))
        f.close()
        return       



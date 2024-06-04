class device_addresses:
    def __init__(self):
        import pyvisa as visa
        
        # Define class variables
        self.scope_address = []
        self.scope_id = []
        self.dmm_address = []
        self.dmm_id = []
        self.ps_address = []
        self.ps_id = []
        self.wfg_address = []
        self.wfg_id = []
        
        # Turn on all test equipment and get the base list
        print("Turn ON all necessary test equipment") 
        temp = input("before pressing ENTER")
        print("")
        rm = visa.ResourceManager('')
        addresses = list(rm.list_resources())
        res = [i for i in addresses if "USB" in i]
        
        # Assign addresses and IDs to respective equipment
        for i in res:
            try:
                temp=rm.open_resource(i)
                id=temp.query("*IDN?")
                if id.find("34450A") !=-1:
                    self.dmm_address = i
                    self.dmm_id = id
                if id.find("33220A") !=-1:
                    self.wfg_address = i
                    self.wfg_id = id
                if id.find("E36313A") !=-1:
                    self.ps_address = i
                    self.ps_id = id
                if id.find("MSO-X 2012A") !=-1:
                    self.scope_address = i
                    self.scope_id = id
            except:
                pass
        
        
    def __repr__(self):
        return "Scope Address: %s, \nDMM Address: %s,"\
            "\nPower supply Address: %s, \nWFG Address: %s" \
            % (self.scope_address, self.dmm_address, \
               self.ps_address, self.wfg_address)
                
    def __str__(self):
        return "Scope Address: %s, \nDMM Address: %s,"\
            "\nPower supply Address: %s, \nWFG Address: %s" \
            % (self.scope_address, self.dmm_address, \
               self.ps_address, self.wfg_address)
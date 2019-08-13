import enum

# SMBusDummy Class
# Device addresses 0x20, 0x21, 0x22, 0x23, 0x24 = DEVICE. up to 8 allowed
# IODIRA: Pin direction register for bank A = 0x00
# IODIRB: Pin direction register for bank B = 0x01
# GPIOA:  Inputs register for bank A = 0x12
# GPIOB:  Inputs register for bank B = 0x13


class SMBusDummy:
    def __init__(self, piSeries):
        self.piSeries = int(piSeries)

    def bus_rev(self):
        if self.piSeries == 0:
            print("pi Revision 1")
        else:
            print("pi Revision 2 or later")

    def write_byte_data(self, device, reg, value):
        if reg==0x00:
            print("{0:08b} written to bank A of device {1:4x}".format(value, device))
        elif reg==0x01:
            print("{0:08b} written to bank B of device {1:4x}".format(value, device))
        elif reg==0x14:
            print("{0:08b} written to bank A of device {1:4x}".format(value, device))
        elif reg==0x15:
            print("{0:08b} written to bank B of device {1:4x}".format(value, device))
        else:
            print("Unknown command")

    def read_byte_data(self, device, gpio_addr):
        if gpio_addr==0x12:
            val = 0b00010001
            print ("{0:08b} read from bank A of device {1:4x}".format(val, device))
            return val  # bank A
        elif gpio_addr==0x13:
            val = 0b00100010
            print("{0:08b} read from bank B of device {1:4x}".format(val, device))
            return val  # bank B

class McpFunc(enum.Enum):
    control = 1
    sensor = 2

def ByteToBits(mcp_byte):
    outList = []
    for offset in range(7, -1, -1):
        mask = 1 << offset
        bit = (mcp_byte & mask) >> offset
        outList.append(bit)

    return outList

def ByteToActivated(mcp_byte):
    outList = []
    for offset in range(7, -1, -1):
        mask = 1 << offset
        if ((mcp_byte & mask) >> offset):
            outList.append(offset)

    return outList

def BitsToByte(bitsList):
    if len(bitsList) != 8:
        print("error in bitsList")
        return 0x00

    byte = 0x00
    for i in range(0, 8):
        if bitsList[i]:
            mask = 1 << (7 - i)
            byte = byte | mask

    return byte


class McpChip:
    """
    McpChip objects should have a valid bus address

    Register addresses IODIRA, IODIRB, GPIOA, GPIOB, OLATA and OLATB are specified as class attributes
    The Control MCP IODIRA needs to set bank A as inputs, and IODIRB to set bank B as outputs.
    Both A & B banks in the other MCP's are all specified as inputs   """

    IODIRA = 0x00   # IO direction registers
    IODIRB = 0x01
    GPIOA = 0x12    # input registers
    GPIOB = 0x13
    OLATA = 0x14    # output latch registers
    OLATB = 0x15

    def __init__(self, bus, bus_addr, chip_func):
        self.bus_addr = bus_addr
        self.chip_func = chip_func
        if self.chip_func == McpFunc.control:
            bus.write_byte_data(bus_addr, McpChip.IODIRA, 0xff)  # specifies that bank A pins are to be inputs.
            bus.write_byte_data(bus_addr, McpChip.IODIRB, 0x00)  # specifies that bank B pins are to be outputs.
        elif self.chip_func == McpFunc.sensor:
            bus.write_byte_data(bus_addr, McpChip.IODIRA, 0xff)  # specifies that bank A pins are to be inputs.
            bus.write_byte_data(bus_addr, McpChip.IODIRB, 0xff)  # specifies that bank B pins are to be inputs.

    def read_zone_switches(self, bus):
        """
        read byte from bank A
        return byte converted to list of bits (0/1)       """

        zone_sw = bus.read_byte_data(self.bus_addr, McpChip.GPIOA) # reads bank A of 0x20. GPIOA registers are at address 0x12 (GPIOB is 0x13)
        outList = ByteToBits(zone_sw)
        return outList

    def get_zone_switches(self, bus):
        """
        gets the switch numbers that are set i.e. = 1
        returns a list of switches that are set to'ON' """

        zone_sw = bus.read_byte_data(self.bus_addr, McpChip.GPIOA) # reads bank A of 0x20. GPIOA registers are at address 0x12 (GPIOB is 0x13)
        outList = ByteToActivated(zone_sw)
        return outList

    def set_zone_LEDs(self, bus, zoneList):
        outByte = BitsToByte(zoneList)
        print("inList to LED's {}".format(zoneList))
        print("outbyte to LED's {0:08b}".format(outByte))
        bus.write_byte_data(self.bus_addr, McpChip.OLATB, outByte)

    def read_sensors(self, bus):
        """  read byte from bank A
             return byte converted to list of bits (0 or 1)       """

        sens_pins = bus.read_byte_data(self.bus_addr,
                                       McpChip.GPIOA)  # reads bank A of MCP. GPIOA registers are at address 0x12 (GPIOB is 0x13)
        sensList = ByteToBits(sens_pins)
        return sensList

    def get_triggered(self, bus):
        """  read byte from bank A
             return list of activated pins (ie pins with value 1)       """

        sens_pins = bus.read_byte_data(self.bus_addr,
                                       McpChip.GPIOA)  # reads bank A of MCP. GPIOA registers are at address 0x12 (GPIOB is 0x13)
        actList = ByteToActivated(sens_pins)
        return actList

    def read_tampers(self, bus):
        """  read byte from bank B
             return byte converted to list of bits (0 or 1)     """

        tam_pins = bus.read_byte_data(self.bus_addr,
                                      McpChip.GPIOB)  # reads bank B of MCP. GPIOA registers are at address 0x13 (GPIOA is 0x12)
        tamlist = ByteToBits(tam_pins)
        return tamlist

    def get_trig_tams(self, bus):
        """  read byte from bank B
             return list of activated pins (ie pins with value 1)     """

        tam_pins = bus.read_byte_data(self.bus_addr,
                                      McpChip.GPIOB)  # reads bank B of MCP. GPIOA registers are at address 0x13 (GPIOA is 0x12)
        actList = ByteToActivated(tam_pins)
        return actList

##
##    def set_iodira(self, iodira):
##        self.iodira = iodira
##
##    def set_iodirb(self, iodirb):
##        self.iodirb = iodirb
##
##    def set_output_reg_a(self, olata):
##        self.olata = olata
##
##    def set_output_reg_b(self, olatb):
##        self.olatb = olatb
##
##    def set_input_reg_a(self, gpioa):
##        self.gpioa = gpioa
##
##    def set_input_reg_b(self, gpiob):
##        self.gpiob = gpiob

# ************************************
# Main Start *************************
#*************************************
def main():

    bus = SMBusDummy(1)

    bus.bus_rev()

    mcp_control = McpChip(bus, 0x20, McpFunc.control)  # construct mcp_control object
    mcp_sens1 = McpChip(bus, 0x21, McpFunc.sensor)     # construct mcp_sensor objects
    mcp_sens2 = McpChip(bus, 0x22, McpFunc.sensor)
    mcp_sens3 = McpChip(bus, 0x23, McpFunc.sensor)

    LEDzoneList = [0,0,1,0,0,1,0,1]
    print("set LED's")
    mcp_control.set_zone_LEDs(bus, LEDzoneList)             # set control LEDs

    zoneSwitchList = mcp_control.read_zone_switches(bus)   # read zone switches
    print("zone switches {}".format(zoneSwitchList))

    sens1List = mcp_sens1.read_sensors(bus)
    print("sens1 pins {}".format(sens1List))

    tam2List = mcp_sens2.read_tampers(bus)
    print("tam2 pins {}".format(tam2List))


if __name__ == "__main__":
    # bus = SMBusDummy(1)

    # bus.bus_rev()

    main()

# Similarly Poll all the sensor MCPs


""" There is one bus object to communicate between the Pi and between 1 and 8 chip objects.
     Each chip object has a unique address (DEVICE or bus_addr) 0x20, 0x21, up to 0x27
     
     For each chip the IODIRA register address is 0x00 and IODIRB register is 0x01.
     And each chip's IODIRA and IODIRB registers will have its own value to specify whether the pins are to be used as 
     inputs or outputs. 0 for outputs and 1 for inputs.
     For example if all of the GPIOA pins are to be outputs then 0x00 (or 0b00000000) must be stored in IODIRA, 
     likewise if all of the GPIOB pins are to be inputs, then 0xFF (or 0b11111111) must be stored in IODIRB.
     And if the first 7 pins are to be outputs and the last one an input, then 0x80 (or 0b10000000) would be stored in 
     IODIRA (or IODIRB)
      
     Each chip has A & B registers for outputs, OLATA (=0x14) and OLATB (=0x15) and A & B registers for inputs 
     GPIOA (=0x12) and GPIOB (=0x13).
     
     To write (or output) to the pins one uses write_byte_data(DEVICE, OLATA, value), where value = 0x00000000 if all 
     pins are to be off and 0x11111111 if all pins are to be on, and any value in between for a combination of on's 
     and off's.
     
     To read (or input) the values on the pins one uses value = read_byte_data(DEVICE, GPIOA), which returns an 8 bit 
     value, which can then be decoded to get the individual pin values.
     
     So  lets assume that mcp_0 is the 'control mcp' with bank A asigned to the zone switches, and bank B assigned to 
     the zone LED's. If a particular zone switch (say zone 3) is up, then that zone is 'OFF' or deactivated. If zone 3 
     LED is on then a sensor within zone 3 has been activated. (If alarm is armed syren/buzzer will activate, etc. If 
     alarm is not armed then LED merely shows which zone has been activated.) So bank A is connected to the zone 
     switches and therefore is an input to the system.  Bank B is connected to the LED's so that is an output.
     So the IODIRA (0x00) registers must be se as inputs, while the IODIRB (0x01) registers must be set as outputs.
     Also assume that mcp_0 address is set at 0x20.
      """

# bus.write_byte_data(0x20, 0x00, 0xff) # specifies that bank A pins are to be inputs.
# bus.write_byte_data(0x20, 0x01, 0x00) # specifies that bank B pins are to be outputs.

"""
     Now lets assume that mcp_1 (with bus address 0x21) is the first of the mcp chips connected to sensors. Bank A pins 
     are connected to the sensor contacts, while bank B pins are connected to the corresponding tamper contacts 
     (if available.) This will be repeated for mcp_2 (0x22), mcp_3 (0x23), etc.  All have inputs only.
     
"""

# bus.write_byte_data(0x21, 0x00, 0xff) # specifies that bank A pins (sensors) are to be inputs.
# bus.write_byte_data(0x21, 0x01, 0xff) # specifies that bank B pins (sensor tamper contacts) are also inputs.

"""
     The above pin direction writes are only done once - ie could be done when mcp objects are instantiated.
     
     However, sensor polling takes place on a regular basis. Control mcp must be polled to see if zone switches have 
     been changed, and LED's switched on or off to indicate system status. Likewise, Sensor mcps must be polled to see 
     if sensors or tampers have been triggered.

"""

# zone_sw = bus.read_byte_data(0x20, 0x12) #reads bank A of 0x20. GPIOA registers are at address 0x12 (GPIOB is 0x13)
# bus.write_byte_data(0x20, 0x15, 0x00)    # would switch all zone LED's off for bank B,. (OLATB = 0x15)
#
# sensor_sw = bus.read_byte_data(0x21, 0x12) # reads bank A of 0x21, sensor values
# tamper_sw = bus.read_byte_data(0x21, 0x13) # reads bank B of 0x21, tamper values

"""
     One does need to generate the 8 bit value to drive the latches OLATB from a list of values (true/false or 1/0).
     Likewise, the zone_sw value is also an 8 bit number which needs to be converted into a list of sensor outputs.
     See junk04.py in ThonnyProjects
"""


     



    
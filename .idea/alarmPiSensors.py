# sensor blueprint or class
# zones are groups of protected areas in house, outbuildings or on property
# sens_mod or sensor module is a class of object that has the functionality of a sensor with its settings. A sens_mod
# may be a reed switch on a door, a pir, a breaking glass sensor, a panic button, a fire or heat sensor, etc.
# but I would like the sens_mod to include several attributes: eg, type, isArmed, isTriggered, isTampered, overRide, etc
class sens_mod:
    """__init__() functions as the class constructor"""
    def __init__(self, name=None, desc=None, typeof='0', n_closed='0', overrideoff='0', istriggered='0', isarmed='0',
                 hastamper='0', tampertriggered='0'):
        self.name = name
        self.desc = desc
        self.typeOf = int(typeof)
        self.n_closed = int(n_closed)
        self.overRideOff = int(overrideoff)
        self.isTriggered = int(istriggered)
        self.isArmed = int(isarmed)
        self.hasTamper = int(hastamper)
        self.tamperTriggered = int(tampertriggered)


sensors = []
file = open('AlarmPiSensors.txt', 'r')
for line in file:
    lst = line.split(',')
    sensor = sens_mod()
    sensor.name = lst[0]
    sensor.desc = lst[1]
    sensor.typeOf = int(lst[2])
    sensor.n_closed = bool(lst[3])
    sensor.overRideOff = bool(lst[4])
    sensor.isTriggered = bool(lst[5])
    sensor.isArmed = bool(lst[6])
    sensor.hasTamper = bool(lst[7])
    sensor.tamperTriggered = bool(lst[8])
    sensors.append(sensor)

for x in sensors:
    print("{0:<8s}  {1:<25s}   {2:2d}   {3:2d}".format(x.name, x.desc, x.typeOf, int(x.n_closed)))#, ' ', x.overRideOff, x.isTriggered, x.isArmed, x.hasTamper, x.tamperTriggered)
    #print(x.name)



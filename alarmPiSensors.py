"""
sens-mod is the blueprint or class that defines the attributes of each sensor
Definitions:
    zones are groups of protected areas in house, outbuildings or on property
    sens_mod or sensor module is a class of object that has the functionality of a sensor with its settings. A sens_mod
      may be a reed switch on a door, a pir, a breaking glass sensor, a panic button, a fire or heat sensor, etc.
    But I would like the sens_mod to include several attributes: eg, type, isArmed, isTriggered, isTampered, overRide, etc
"""

import csv

class sens_mod:
    """__init__() functions as the class constructor"""
    def __init__(self, id='0', name=None, desc=None, zone='0', grp=None, mcp_addr='0', bank='0', pin='0', typeof='0', dec_code='0',
                 operable='0', norm_closed='0', override_on='0', is_triggered='0', is_armed='0',
                 has_tamper='0', tamper_overr_on='0', tamper_triggered='0'):
        self.id = id
        self.name = name
        self.desc = desc
        self.zone = int(zone)
        self.grp = grp
        self.mcp_addr = int(mcp_addr)
        self.bank = int(bank)
        self.pin = int(pin)
        self.typeOf = int(typeof)
        self.dec_code = int(dec_code)
        self.operable = int(operable)
        self.norm_closed = int(norm_closed)
        self.overRide_on = int(override_on)
        self.is_Triggered = int(is_triggered)
        self.is_Armed = int(is_armed)
        self.has_Tamper = int(has_tamper)
        self.tamper_overr_on = int(tamper_overr_on)
        self.tamper_Triggered = int(tamper_triggered)


def GetDataFromHost():
    active_list = []
    field_names, sensors = getSensorList()
    for sensor in sensors:
        if sensor.operable:
            active_list.append(sensor)

    return active_list

def getSensorList():
    field_names = []
    sensors = []
    with open('AlarmPiSensors.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_counter = 0
        for row in csv_reader:
            line_counter += 1
            if line_counter == 1:
                continue
            if line_counter == 2:
                for fld in row:
                    field_names.append(fld)
            else:
                sensor = sens_mod()
                sensor.id = int(row[0])
                sensor.name = row[1]
                sensor.desc = row[2]
                sensor.zone = int(row[3])
                sensor.grp = row[4]
                sensor.mcp_addr = int(row[5])
                sensor.bank = int(row[6])
                sensor.pin = int(row[7])
                sensor.typeOf = int(row[8])
                sensor.dec_code = int(row[9])
                sensor.operable = int(row[10])
                sensor.norm_closed = bool(row[11])
                sensor.overRide_on = bool(row[12])
                sensor.is_Triggered = bool(row[13])
                sensor.is_Armed = bool(row[14])
                sensor.has_Tamper = bool(row[15])
                sensor.tamper_overr_on = bool(row[16])
                sensor.tamperTriggered = bool(row[17])

                sensors.append(sensor)
     # 'with' automatically closes file

    return field_names, sensors

def main():
    field_names, sensors = getSensorList()

    print(f'{" ".join(field_names)}')
    for x in sensors:
            print("{0:3d} {1:<10s} {2:<28s} {3:3d} {4:<5s} {5:3d} {6:4d} {7:3d} {8:4d} {9:4d} {10:2d} {11:2d} {12:2d} "
                  "{13:2d} {14:2d} {15:2d} {16:2d} {17:2d}"
                    .format(x.id, x.name, x.desc, x.zone, x.grp, x.mcp_addr, x.bank, x.pin, x.typeOf, x.dec_code,
                            x.operable, x.norm_closed,
                            x.overRide_on, x.is_Triggered, x.is_Armed, x.has_Tamper, x.tamper_overr_on,
                            x.tamper_Triggered, x.id))
    # for sensor in sensors:
    #     for item in sensor:
    #         print(f" {item}")


if __name__ == "__main__":
    main()


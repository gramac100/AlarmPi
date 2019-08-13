#!/usr/bin/env python
"""
alarm.py 0.00 Home Alarm System
---------------------------------------------------------------------------------

 ----------------------------------------------------------------------------------
"""

import time
import config
import io_extender
import alarmPiSensors

def build_io_lists():
    RecordSet = alarmPiSensors.GetDataFromHost()
    if RecordSet == False:
        return
    n_records = len(RecordSet)
    print(f"n records {n_records}")

    for i in range(0, n_records):
        print(f"{RecordSet[i].id}  {RecordSet[i].name} {RecordSet[i].grp}")

    zoneSw = []
    zoneLed = []
    global act_sens, act_panic, act_tamper
    act_sens = []
    act_panic = []
    act_tamper = []
    for i in range (0, n_records):
        if RecordSet[i].grp == 'ctl':
            zoneSw.append(RecordSet[i])
        elif RecordSet[i].grp == 'led':
            zoneLed.append(RecordSet[i])
        elif RecordSet[i].grp == 'alm':
            act_sens.append(RecordSet[i])
        elif RecordSet[i].grp == 'pan':
            act_panic.append(RecordSet[i])
        elif RecordSet[i].grp == 'tam':
            act_tamper.append(RecordSet[i])

    n_zoneSw = len(zoneSw)
    n_zoneLed = len(zoneLed)
    n_sensor = len(act_sens)
    n_panic = len(act_panic)
    n_tamper = len(act_tamper)

    print(f"zone sw {n_zoneSw}, zone led {n_zoneLed}, sensor {n_sensor}, panic {n_panic}, tamper {n_tamper}")

# TODO: runs to "panic pan01 id 56 then stops with exit code 1 - Fixed must be pan.pin in line 108 or address wrong

def poll_mcp_a():
    # TODO: as code stands: in normal use one sends an empty list, [], and the sensor mcps get read and
    #  a list of sensor values returned. Optionally one can send the list of sensor values that one wants
    #  returned, for testing purposes. This would be a list of 24 0's and 1's. Better to send a list of 3 bytes,
    #  which can then be converted, or handled appropriately.
    mcp_a_list = pi_X.read_mcp_a([])
    # print(f" sensors {sens_list} len {len(sens_list)}")
    return mcp_a_list

def poll_mcp_b():
    # TODO: see above
    mcp_b_list = pi_X.read_mcp_b([])
    #print(f" sensors {sens_list} len {len(sens_list)}")
    return mcp_b_list

def poll_zone_sw():
    # TODO: see above
    zone_list = pi_X.read_zone_switches([])#[1, 1, 1, 1, 1, 1, 1, 1])

    #print(f" zones {zone_list} len {len(zone_list)}")

    return zone_list

def poll_settings(time):
    pass

def main():
    config.init()
    # Start Main Program Loop

    build_io_lists()
    # create IoXtender objects for each mcp. ie configure i2c bus & mcp io ports
    global pi_X
    pi_X = io_extender.IoX()

    #  poll_zone_sw()
    # zone_list = pi_X.read_zone_switches()
    # print(f" zones {zone_list} len {len(zone_list)}")


    config.start_time = time.time()

    while True:
        mcp_a_list = poll_mcp_a()
        print(f'sens list (in loop) {mcp_a_list}')

        mcp_b_list = poll_mcp_b()
        print(f'tamper + panic list (in loop) {mcp_b_list}')

        config.elapsed_time = time.time() - config.start_time
        zone_list = poll_zone_sw()
        print(f'zone_list (in loop) {zone_list}')

        for pan in act_panic:
            print(f'panic {pan.name} id {pan.id}')
            if mcp_a_list[pan.mcp_addr-1 + pan.pin]:   # note pan.pin NOT pan.id
                print(f'panic {pan.id} is triggered')

        for sens in act_sens:
            print(f'sensor {sens.name} id {sens.id}')
            if zone_list[sens.zone]: #  == 1:
                print('is in active zone')
                if mcp_a_list[sens.mcp_addr-1 + sens.pin]: # == 1:
                    print(f'sensor {sens.id} is triggered')
                    print(f'zone led {sens.zone} must be  on')

        poll_settings(config.elapsed_time)

        print(config.elapsed_time)

        time.sleep(2)  # 0.2


if __name__ == "__main__":
    main()

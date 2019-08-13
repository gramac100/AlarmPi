import smbusDummy


class IoX:
    def __init__(self):
        self.bus = smbusDummy.SMBusDummy(1)

        self.mcp_ctrl = smbusDummy.McpChip(self.bus, 0x20, smbusDummy.McpFunc.control)  # construct mcp_control object
        self.mcp_sens1 = smbusDummy.McpChip(self.bus, 0x21, smbusDummy.McpFunc.sensor)  # construct mcp_sensor objects
        self.mcp_sens2 = smbusDummy.McpChip(self.bus, 0x22, smbusDummy.McpFunc.sensor)
        self.mcp_sens3 = smbusDummy.McpChip(self.bus, 0x23, smbusDummy.McpFunc.sensor)

    def bus_version(self):
        self.bus.bus_rev()

    def read_mcp_a(self, set_vals):
        if len(set_vals) == 24:
            return set_vals
        else:
            sens_list = self.mcp_sens1.read_sensors(self.bus)
            sens_list.extend(self.mcp_sens2.read_sensors(self.bus))
            sens_list.extend(self.mcp_sens3.read_sensors(self.bus))
            return sens_list

    def get_activated_sensors(self):
        sens_list = self.mcp_sens1.get_triggered(self.bus)
        sens_list.extend(self.mcp_sens2.get_triggered(self.bus))
        sens_list.extend(self.mcp_sens3.get_triggered(self.bus))
        return sens_list


    def read_mcp_b(self, set_vals):
        if len(set_vals) == 8:
            return set_vals
        else:
            tam_list = self.mcp_sens1.read_tampers(self.bus)
            tam_list.extend(self.mcp_sens2.read_tampers(self.bus))
            tam_list.extend(self.mcp_sens3.read_tampers(self.bus))
            return tam_list

    def get_activated_tams(self):
        tam_list = self.mcp_sens1.get_trig_tams(self.bus)
        tam_list.extend(self.mcp_sens2.get_trig_tams(self.bus))
        tam_list.extend(self.mcp_sens3.get_trig_tams(self.bus))
        return tam_list

    def read_zone_switches(self, set_vals):
        if len(set_vals) == 8:
            return set_vals
        else:
            zone_list = self.mcp_ctrl.read_zone_switches(self.bus)
            return zone_list

    def get_ctrl_switches(self):
        ctrl_list = self.mcp_ctrl.get_zone_switches(self.bus)
        return ctrl_list

    def set_ctrl_leds(self, led_list):
        self.mcp_ctrl.set_zone_LEDs(self.bus, led_list)


def main():
    pi_x = IoX()
    pi_x.bus_version()

    outlist = pi_x.read_mcp_a()
    print("sensor pins {}".format(outlist))

    actlist = pi_x.get_activated_sensors()
    print(f"activated sensor pins {actlist}")

    outlist = pi_x.read_mcp_b()
    print("tamper pins {}".format(outlist))

    actlist = pi_x.get_activated_tams()
    print(f"activated tamper pins {actlist}")

    LEDzoneList = [0, 0, 1, 0, 0, 1, 0, 1]
    print(f"set LED's to : {LEDzoneList}")
    pi_x.set_ctrl_leds(LEDzoneList)            # set control LEDs

    outlist = pi_x.read_zone_switches()
    print(f"control switches {outlist}")

    outlist = pi_x.get_ctrl_switches()
    print(f"list of ctrls set to 'ON' {outlist}")


if __name__ == "__main__":

    main()

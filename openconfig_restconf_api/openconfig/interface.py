#!/usr/bin/env python3


class OpenConfigInterface:
    """This class is not used in the code now,
    but it is a good example of how"""

    def __init__(self, json_data):
        self.json_data = json_data

    def to_dict(self):
        return self.json_data

    def get_description(self):
        return self.json_data['openconfig-interfaces:description']

    def get_mtu(self):
        return self.json_data['openconfig-interfaces:mtu']

    def get_name(self):
        return self.json_data['openconfig-interfaces:name']

    def get_enabled(self):
        return self.json_data['openconfig-interfaces:enabled']

    def get_type(self):
        return self.json_data['openconfig-interfaces:type']

    def get_counters(self):
        return self.json_data['openconfig-interfaces:counters']

    def get_state(self):
        return self.json_data['openconfig-interfaces:state']

    def get_config(self):
        return self.json_data['openconfig-interfaces:config']

    def get_subinterfaces(self):
        return self.json_data['openconfig-interfaces:subinterfaces']

    def get_subinterface(self, index):
        return self.json_data['openconfig-interfaces:subinterfaces']['subinterface'][
            index
        ]

    def get_subinterface_index(self, index):
        return self.json_data['openconfig-interfaces:subinterfaces']['subinterface'][
            index
        ]

    def get_subinterface_config(self, index):
        return self.json_data['openconfig-interfaces:subinterfaces']['subinterface'][
            index
        ]['config']

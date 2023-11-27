#!/usr/bin/env python3

import json
import pyangbind.lib.pybindJSON as pybindJSON
from flask import Flask, jsonify, Response

from openconfig.oc_interfaces import openconfig_interfaces
from base.utils import rc_cmd
import pyangbind.lib.xpathhelper as xpathhelper

app = Flask(__name__)

ph = xpathhelper.YANGPathHelper()

oc_interface = openconfig_interfaces()
oc_interface.interfaces.interface.add("eth0")
oc_interface.interfaces.interface['eth0'].config.name = 'eth0'
oc_interface.interfaces.interface['eth0'].config.description = 'WAN interface'
oc_interface.interfaces.interface['eth0'].config.enabled = True
oc_interface.interfaces.interface['eth0'].config.mtu = 1504
from pprint import pprint
#pprint(dir(oc_interface.interfaces.interface['eth0'].config))

# Serialise the oc_interface object to JSON
# print(pybindJSON.dumps(oc_interface, mode="ietf"))


def get_ip_link_data(ifname=""):
    if ifname:
        _cmd = f"ip --json --stats link show dev {ifname}"
    else:
        _cmd = f"ip --json --stats link show"
    rc, out = rc_cmd(_cmd)
    return json.loads(out) if rc == 0 else []


def populate_interfaces(oc_iface, ip_link_data):
    """Populate the OpenConfig interfaces model with data from the ip link command"""
    for interface_data in ip_link_data:
        oc_interface_path = oc_iface.interfaces.interface
        ifname = interface_data.get("ifname", "")
        if ifname == "lo":
            continue
        # Only add the interface if it doesn't already exist
        if ifname:
            if ifname and ifname not in oc_interface_path:
                oc_interface_path.add(ifname)

            oc_interface_path[ifname].config.name = ifname
            oc_interface_path[ifname].config.description = str(
                interface_data.get("ifalias", "")
            )
            oc_interface_path[ifname].config.mtu = int(interface_data.get("mtu", 1500))


@app.get("/restconf/data/openconfig-interfaces:interfaces")
# http://localhost:5000/restconf/data/openconfig-interfaces:interfaces
def get_interfaces():
    ip_link_data = get_ip_link_data()
    populate_interfaces(oc_interface, ip_link_data)

    result = oc_interface.interfaces.get(filter=False)
    return jsonify(result)


@app.get("/restconf/data/openconfig-interfaces:interfaces/interface=<name>")
# http://localhost:5000/restconf/data/openconfig-interfaces:interfaces/interface=eth0
def get_interface(name):
    ip_link_data = get_ip_link_data(name)
    populate_interfaces(oc_interface, ip_link_data)

    result = oc_interface.interfaces.get(filter=False)
    return jsonify(result)


@app.get("/restconf/data/openconfig-interfaces:interfaces/interface=<name>/state")
# http://localhost:5000/restconf/data/openconfig-interfaces:interfaces/interface=eth0/state
def get_interface_state(name):
    pass


@app.get(
    "/restconf/data/openconfig-interfaces:interfaces/interface=<name>/config/description"
)
# http://localhost:5000/restconf/data/openconfig-interfaces:interfaces/interface=eth0/config/description
def get_interface_description(name):
    pass


@app.get("/restconf/data/openconfig-interfaces:tmp")
def tmp_get_interfaces():
    ip_link_data = get_ip_link_data()
    populate_interfaces(oc_interface, ip_link_data)

    # result = oc_interface.interfaces.get(filter=False)
    # json_data = pybindJSON.dumps(result, mode="ietf")
    # response = Response(response=json_data, status=200, mimetype="application/json")
    # return response
    tmp = pybindJSON.dumps(oc_interface, mode="ietf")
    return tmp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

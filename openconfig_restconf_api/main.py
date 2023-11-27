#!/usr/bin/env python3

import json

import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
from pyangbind.lib.serialise import pybindIETFXMLEncoder
import pyangbind.lib.xpathhelper as xpathhelper
from flask import Flask, jsonify, request, Response

from base.utils import rc_cmd
from openconfig.oc_interfaces import openconfig_interfaces

from pyangbind.lib.pybindJSON import dumps as pybind_dumps


app = Flask(__name__)

ph = xpathhelper.YANGPathHelper()

oc_interface = openconfig_interfaces()
oc_interface.interfaces.interface.add("eth0")
oc_interface.interfaces.interface['eth0'].config.name = 'eth0'
oc_interface.interfaces.interface['eth0'].config.description = 'WAN interface'
oc_interface.interfaces.interface['eth0'].config.enabled = True
oc_interface.interfaces.interface['eth0'].config.mtu = 1504


# pprint(dir(oc_interface.interfaces.interface['eth0'].config))

# Serialise the oc_interface object to JSON
tmp = pybindJSON.dumps(oc_interface, mode="ietf")
print(tmp)
tmp = pybindIETFXMLEncoder.serialise(oc_interface)
print(tmp)
# print(pybindIETFXMLEncoder.serialise(oc_interface))
# print(pybindJSONDecoder.load_json(tmp, None, None, "openconfig_interfaces", ph))


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


# http://localhost:5000/restconf/data/openconfig-interfaces:interfaces
@app.get("/restconf/data/openconfig-interfaces:interfaces")
def get_interfaces():
    ip_link_data = get_ip_link_data()
    populate_interfaces(oc_interface, ip_link_data)

    result = oc_interface.interfaces.get(filter=False)
    return jsonify(result)


# http://localhost:5000/restconf/data/openconfig-interfaces:interfaces/interface=eth0
@app.route(
    "/restconf/data/openconfig-interfaces:interfaces/interface=<name>",
    methods=["GET", "POST", "PUT", "DELETE"],
)
def get_interface(name):
    if request.method == "GET":
        ip_link_data = get_ip_link_data(name)
        populate_interfaces(oc_interface, ip_link_data)

        result = oc_interface.interfaces.get(filter=False)
        return jsonify(result)
    elif request.method == "POST":
        pass
    # ip_link_data = get_ip_link_data(name)
    #  populate_interfaces(oc_interface, ip_link_data)
    #
    #  result = oc_interface.interfaces.get(filter=False)
    #  return jsonify(result)


# http://localhost:5000/restconf/data/openconfig-interfaces:interfaces/interface=eth0/state
@app.get("/restconf/data/openconfig-interfaces:interfaces/interface=<name>/state")
def get_interface_state(name):
    pass


# http://localhost:5000/restconf/data/openconfig-interfaces:interfaces/interface=eth0/config/description
@app.get(
    "/restconf/data/openconfig-interfaces:interfaces/interface=<name>/config/description"
)
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

    # tmp = pybindJSON.dumps(oc_interface, mode="ietf")
    # return tmp
    # Check the Accept header to determine the client's preference
    accept_header = request.headers.get('Accept', '')
    # print(f' DEBUG {accept_header}')
    # Respond with XML
    if 'application/yang-data+xml' in accept_header:
        tmp = pybindIETFXMLEncoder.serialise(oc_interface)
        response = Response(response=tmp, status=200, content_type="application/xml")
        return response
    # Respond with JSON
    elif 'application/yang-data+json' in accept_header:
        # Respond with JSON
        tmp = pybindJSON.dumps(oc_interface, mode="ietf")
        response = Response(
            response=tmp, status=200, content_type="application/yang-data+json"
        )
        return response
    # Default to JSON
    else:
        # Respond with JSON (default)
        tmp = pybindJSON.dumps(oc_interface, mode="ietf")
        response = Response(response=tmp, status=200, content_type="application/json")
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

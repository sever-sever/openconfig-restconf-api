# openconfig-restconf-api
Openconfig RESTCONF API

Start API server and get info
```shell
$ ./main.py
$ curl --location --globoff 'http://localhost:5000/restconf/data/openconfig-interfaces:tmp' \
  --header 'Accept: application/yang-data+json, application/yang-data.errors+json' \
  --header 'Content-Type: application/yang-data+json'

$ curl --location --globoff 'http://localhost:5000/restconf/data/openconfig-interfaces:tmp' \
  --header 'Accept: application/yang-data+xml'
```

Example:
```shell
$ curl --location --globoff 'http://localhost:5000/restconf/data/openconfig-interfaces:tmp' \
  --header 'Accept: application/yang-data+json, application/yang-data.errors+json' \
  --header 'Content-Type: application/yang-data+json'
{
    "openconfig-interfaces:interfaces": {
        "interface": [
            {
                "name": "eth0",
                "config": {
                    "name": "eth0",
                    "mtu": 1504,
                    "description": "WAN interface",
                    "enabled": true
                }
            },
        ...
        ]
    }
}

$ curl --location --globoff 'http://localhost:5000/restconf/data/openconfig-interfaces:tmp' \
  --header 'Accept: application/yang-data+xml'
<openconfig-interfaces xmlns="http://openconfig.net/yang/interfaces">
  <interfaces>
    <interface>
      <name>eth0</name>
      <config>
        <name>eth0</name>
        <mtu>1504</mtu>
        <description>WAN interface</description>
        <enabled>true</enabled>
      </config>
    </interface>
    ...
  </interfaces>
</openconfig-interfaces>

```
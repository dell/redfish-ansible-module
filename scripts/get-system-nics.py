# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import rfutils
import json
import sys
rf = rfutils.rfutils()

def get_list_of_interfaces(idrac, base_uri, rf_uri):
    count = 0
    interfaces = []
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()

    for interface in data[u'Members']:
        c = interface[u'@odata.id']
        interfaces.append(c)
    return interfaces

def get_interface_details(idrac, base_uri, interfaces):
    for i in interfaces:
        uri = base_uri + i
        response = rf.send_get_request(idrac, uri)
        if not response.status_code == 200:
            rf.print_red("Something went wrong.")
            exit(1)
        data = response.json()
        rf.print_bold("Name: %s" % data[u'Name'])
        print(" FQDN: %s" % data[u'FQDN'])
        for info in data[u'IPv4Addresses']:
            print(" IPv4: %s" % info[u'Address'])
            print(" Gateway: %s" % info[u'GateWay'])
            print(" SubnetMask: %s" % info[u'SubnetMask'])
        for info in data[u'IPv6Addresses']:
            print(" IPv6: %s" % info[u'Address'])
        for info in data[u'NameServers']:
            print(" NameServer: %s" % info)
        print(" MAC: %s" % data[u'PermanentMACAddress'])
        print(" Speed: %s Mbps" % data[u'SpeedMbps'])
        print(" MTU: %s" % data[u'MTUSize'])
        print(" Autoneg: %s" % data[u'AutoNeg'])
        print(" State: %s" % data[u'Status'][u'State'])
        print(" Health: %s\n" % data[u'Status'][u'Health'])
    return

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/"

    # Get all interfaces
    interfaces = get_list_of_interfaces(idrac, base_uri, rf_uri)

    # Go through list of devices and get detailed information for each one
    get_interface_details(idrac, base_uri, interfaces)

if __name__ == '__main__':
    main()

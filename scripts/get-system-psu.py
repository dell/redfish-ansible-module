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

def get_list_of_psus(idrac, base_uri, rf_uri):
    count = 0
    psus = []
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()

    for psu in data[u'Links'][u'PoweredBy']:
        c = psu[u'@odata.id']
        psus.append(c)
    return psus

def get_psu_details(idrac, base_uri, psus):
    for i in psus:
        uri = base_uri + i
        response = rf.send_get_request(idrac, uri)
        if not response.status_code == 200:
            rf.print_red("Something went wrong.")
            exit(1)
        data = response.json()
        rf.print_bold("Name: %s" % data[u'MemberId'])
        print(" Model: %s" % data[u'Model'])
        print(" Serial Number: %s" % data[u'SerialNumber'])
        print(" Part Number: %s" % data[u'PartNumber'])
        print(" Manufacturer: %s" % data[u'Manufacturer'])
        print(" Firmware Version: %s" % data[u'FirmwareVersion'])
        print(" Power Capacity: %s Watts" % data[u'PowerCapacityWatts'])
        print(" Power Supply Type: %s" % data[u'PowerSupplyType'])
        print(" State: %s" % data[u'Status'][u'State'])
        print(" Health: %s\n" % data[u'Status'][u'Health'])
    return

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Systems/System.Embedded.1/"

    # Get all power supplies
    psus = get_list_of_psus(idrac, base_uri, rf_uri)

    # Go through list of devices and get detailed information for each one
    get_psu_details(idrac, base_uri, psus)

if __name__ == '__main__':
    main()

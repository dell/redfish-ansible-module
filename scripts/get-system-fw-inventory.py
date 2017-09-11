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
import requests
import sys
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
rf = rfutils.rfutils()

def send_get_request(idrac, uri):
    try:
        response = requests.get(uri, verify=False, auth=(idrac['user'], idrac['pswd']))
    except: raise
    return response

def get_list_of_devices(idrac, base_uri, rf_uri):
    count = 0
    devices = []
    response = send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if response.status_code == 400:
        rf.print_red("Only supported on 14G.")
        return 1

    data = response.json()
    for device in data[u'Members']:
        d = device[u'@odata.id']
        d = d.replace(rf_uri, "")	# remove part of URL, leave device name
        if "Installed" in d: devices.append(d)
    return devices

def get_fw_version(idrac, base_uri, rf_uri, devices):
    devices_details = []
    for d in devices:
        uri = base_uri + rf_uri + d
        response = send_get_request(idrac, uri)
        data = response.json()

        devices_details.append("Name: %s" % data[u'Name'])
        devices_details.append("FW version: %s\n" % data[u'Version'])
    return devices_details

def main():
    idrac = rf.check_args(sys)

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/UpdateService/FirmwareInventory/"

    # Get all devices
    devices = get_list_of_devices(idrac, base_uri, rf_uri)
    if devices == 1: exit(1)

    # Go through list of devices and get detailed information for each one
    devices_details = get_fw_version(idrac, base_uri, rf_uri, devices)
    for d in devices_details:
        print(d)

if __name__ == '__main__':
    main()

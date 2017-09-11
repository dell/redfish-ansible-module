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

def get_inventory(idrac, base_uri, rf_uri):
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if response.status_code == 400:
        rf.print_red("Something went wrong.")
        exit(1)

    data = response.json()
    # print(json.dumps(data, separators=(',', ':')))
    print("Model:       %s" % data[u'Model'])
    print("Mfg:         %s" % data[u'Manufacturer'])
    print("Part Number: %s" % data[u'PartNumber'])
    print("System Type: %s" % data[u'SystemType'])
    print("Asset tag:   %s" % data[u'AssetTag'])
    print("Service tag: %s" % data[u'SKU'])
    print("Serial No.:  %s" % data[u'SerialNumber'])
    print("BIOS:        %s" % data[u'BiosVersion'])
    print("Hostname:    %s" % data[u'HostName'])
    print("Power state: %s" % data[u'PowerState'])
    print("Memory:      %s" % data[u'MemorySummary'][u'TotalSystemMemoryGiB'])
    print("CPU count:   %s" % data[u'ProcessorSummary'][u'Count'])
    print("CPU model:   %s" % data[u'ProcessorSummary'][u'Model'])
    print("CPU health   %s" % data[u'ProcessorSummary'][u'Status'][u'Health'])
    print("Status:      %s" % data[u'Status'][u'Health'])

    return

def main():
    idrac = rf.check_args(sys)

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Systems/System.Embedded.1"

    # Get system inventory
    get_inventory(idrac, base_uri, rf_uri)

if __name__ == '__main__':
    main()

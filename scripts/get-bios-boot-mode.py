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

# Script used to get boot mode (Legacy BIOS/UEFI) and device boot order.

import rfutils
import json
import sys
rf = rfutils.rfutils()

def get_bios_boot_mode(idrac, uri):
    response = rf.send_get_request(idrac, uri)
    if response.status_code == 400:
        rf.print_red("Only supported on 14G.")
        exit(1)
    elif not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()
    boot_mode = data[u'Attributes']["BootMode"]
    print("Boot mode: %s" % boot_mode)
    return boot_mode

def get_bios_boot_source(idrac, uri, boot_mode):
    response = rf.send_get_request(idrac, uri)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()
    if boot_mode == "Uefi": boot_seq = "UefiBootSeq"
    else: boot_seq = "BootSeq"

    boot_devices = data[u'Attributes'][boot_seq]
    for b in boot_devices:
        print("Device: [%s] %s" % (b[u'Index'], b[u'Name']))
    return

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']

    # Get BIOS boot mode
    rf_uri = "/redfish/v1/Systems/System.Embedded.1/Bios"
    boot_mode = get_bios_boot_mode(idrac, base_uri + rf_uri)

    # Get BIOS boot sources (PERC, NIC, etc.)
    rf_uri = "/redfish/v1/Systems/System.Embedded.1/BootSources"
    get_bios_boot_source(idrac, base_uri + rf_uri, boot_mode)

if __name__ == '__main__':
    main()

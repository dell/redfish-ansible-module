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

# Script used to retrieve fan information

import rfutils
import json
import sys
rf = rfutils.rfutils()

def get_list_of_fans(idrac, base_uri, rf_uri):
    fanslist = []
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if response.status_code == 400:
        rf.print_red("Only supported on 14G.")
        return 1
    elif not response.status_code == 200:
        rf.print_red("Something went wrong.")
        return 1
    data = response.json()
    for fans in data[u'Fans']:
    # There is more information avvailable but this is most important
        print("Name: %s" % fans[u'FanName'])
        print("Reading: %s RPMs" % fans[u'Reading'])
        print("State: %s" % fans[u'Status'][u'State'])
        print("Health: %s\n" % fans[u'Status'][u'Health'])
    return fanslist

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']

    # Get all fan information
    rf_uri = "/redfish/v1/Chassis/System.Embedded.1/Thermal"
    fans = get_list_of_fans(idrac, base_uri, rf_uri)

if __name__ == '__main__':
    main()

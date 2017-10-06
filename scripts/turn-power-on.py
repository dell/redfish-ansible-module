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

# Script to turn system power off

import rfutils
import json
import sys
rf = rfutils.rfutils()

def turn_power_on(idrac, base_uri, rf_uri, payload, headers):
    response = rf.send_post_request(idrac, base_uri + rf_uri, payload, headers)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 204:
        rf.print_red("Something went wrong.")
        exit(1)
    return

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri="/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"

    payload = {'ResetType' : 'On'}
    headers = {'content-type': 'application/json'}

    # Turn system power on
    turn_power_on(idrac, base_uri, rf_uri, json.dumps(payload), headers)

if __name__ == '__main__':
    main()

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

# Script to get power readings from server

import rfutils
import json
import sys
rf = rfutils.rfutils()

def get_power(idrac, base_uri, rf_uri):
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()
    # print(json.dumps(data, separators=(',', ':')))
    print("Power Monitoring - Historical Trends - Last Hour")
    print("Average Usage: %s" % data[u'PowerMetrics'][u'AverageConsumedWatts'])
    print("Max Peak:      %s" % data[u'PowerMetrics'][u'MaxConsumedWatts'])
    print("Min Peak:      %s" % data[u'PowerMetrics'][u'MinConsumedWatts'])
    return

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Chassis/System.Embedded.1/Power/PowerControl"

    # Get system inventory
    get_power(idrac, base_uri, rf_uri)

if __name__ == '__main__':
    main()

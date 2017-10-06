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

# Script to get System Event (SE) and Lifecycle Controller (LC) Logs

import rfutils
import json
import sys
rf = rfutils.rfutils()

def get_selogs(idrac, base_uri, rf_uri):
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    #rf.print_bold("status_code: %s" % response.status_code)
    rf.print_bold("uri: %s" % base_uri + rf_uri)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()

    print("---------------- SE Logs ----------------\n")
    for logEntry in data[u'Members']:
        print("%s: %s" % (logEntry[u'Name'], logEntry[u'Created']))
        print(" %s\n" % logEntry[u'Message'])
    return

def get_lclogs(idrac, base_uri, rf_uri):
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()

    print("---------------- LC Logs ----------------\n")
    for logEntry in data[u'Members']:
        print("%s: %s" % (logEntry[u'Name'], logEntry[u'Created']))
        print(" %s\n" % logEntry[u'Message'])
    return

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']

    # Get System Event Logs
    rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Sel"
    get_selogs(idrac, base_uri, rf_uri)

    # Get Lifecycle Controller Logs
#   rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Lclog"
#   get_lclogs(idrac, base_uri, rf_uri)

if __name__ == '__main__':
    main()

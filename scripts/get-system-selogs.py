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
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
rf = rfutils.rfutils()

def get_logs(idrac, base_uri, rf_uri):
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if response.status_code == 400:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()

    for logEntry in data[u'Members']:
        print("%s: %s" % (logEntry[u'Name'], logEntry[u'Created']))
        print(" %s\n" % logEntry[u'Message'])
    return

def main():
    idrac = rf.check_args(sys)

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Sel"

    get_logs(idrac, base_uri, rf_uri)

if __name__ == '__main__':
    main()

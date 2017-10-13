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

# Script to add a user to iDRAC. Very simple stuff here, should add some
# logic to get first empty user ID rather than specifying one.

import rfutils
import json
import sys
rf = rfutils.rfutils()

def delete_user(idrac, base_uri, rf_uri, payload, headers):
    response = rf.send_patch_request(idrac, base_uri + rf_uri, payload, headers)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    return

def main():
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri="/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/3"

    a = {'Enabled': False}		# make sure you disable it first
    c = {'UserName': ""}		# Same effect as deleting it (mostly)
    headers = {'content-type': 'application/json'}

    # Delete user
    for payload in a, c:
        delete_user(idrac, base_uri, rf_uri, payload, headers)

if __name__ == '__main__':
    main()

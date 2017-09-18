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

# Script used to retrieve all iDRAC users

import rfutils
import json
import sys
rf = rfutils.rfutils()

def get_list_of_users(idrac, base_uri, rf_uri):
    user_list = []
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()
    for users in data[u'Members']:
        u = users[u'@odata.id']
        u = u.replace(rf_uri, "")       # remove part of URL, leave user Id
        user_list.append(u)
    return user_list

def get_users_details(idrac, base_uri, rf_uri, user_list):
    users_details = []
    for u in user_list:
        uri = base_uri + rf_uri + u
        response = rf.send_get_request(idrac, uri)
        if not response.status_code == 200:
            rf.print_red("Something went wrong.")
            continue
        data = response.json()
        if not data[u'UserName'] == "":	# only care if name is not empty
            users_details.append("Id: %s" % data[u'Id'])
            users_details.append("Name: %s" % data[u'Name'])
            users_details.append("UserName: %s" % data[u'UserName'])
            users_details.append("RoleId: %s\n" % data[u'RoleId'])
    return users_details

def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Accounts/"

    # Get all users (ignore empty user slots)
    user_list = get_list_of_users(idrac, base_uri, rf_uri)
    if user_list == 1: exit(1)			# catch return error

    # Go through list of users and get detailed information for each one
    users_details = get_users_details(idrac, base_uri, rf_uri, user_list)
    for u in users_details:
        print(u)

if __name__ == '__main__':
    main()

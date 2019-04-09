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
rf = rfutils.rfutils()


def get_list_of_controllers(idrac, base_uri, rf_uri):
    count = 0
    controllers = []
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 200:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()

    for controller in data[u'Members']:
        c = controller[u'@odata.id']
        controllers.append(c)
    return controllers


def get_controller_details(idrac, base_uri, controllers):
    properties = ['CacheSummary', 'FirmwareVersion', 'Identifiers',
                  'Location', 'Manufacturer', 'Model', 'Name',
                  'PartNumber', 'SerialNumber', 'SpeedGbps', 'Status']

    for controller in controllers:
        uri = base_uri + controller
        response = rf.send_get_request(idrac, uri)
        if not response.status_code == 200:
            rf.print_red("Something went wrong.")
            exit(1)
        data = response.json()
        rf.print_bold("Name: %s" % data[u'Name'])
        # print(" FQDN: %s" % data[u'FQDN'])

        for property in properties:
            if property in data: 
                print("%s: %s" % (property, data[property]))
    return


def main():
    # Initialize iDRAC arguments
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Systems/System.Embedded.1/Storage/"

    # Get all controllers
    controllers = get_list_of_controllers(idrac, base_uri, rf_uri)

    # Go through list of devices and get detailed information for each one
    get_controller_details(idrac, base_uri, controllers)


if __name__ == '__main__':
    main()

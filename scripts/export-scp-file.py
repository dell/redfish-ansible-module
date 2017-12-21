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

import json
import sys
import re
import rfutils
rf = rfutils.rfutils()

def export_scp(idrac, base_uri, rf_uri, payload, headers):
    response = rf.send_post_request(idrac, base_uri + rf_uri, payload, headers)
    rf.print_bold("status_code: %s" % response.status_code)
    if not response.status_code == 202:
        rf.print_red("Something went wrong.")
        exit(1)

    response_output=response.__dict__
    job_id = response_output["headers"]["Location"]
    job_id = re.search("JID_.+", job_id).group()
    rf.print_green("Job ID: %s" % job_id)
    return

def main():
    idrac = rf.check_args(sys)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ExportSystemConfiguration"

    headers = {'content-type': 'application/json'}
    payload = {"ExportFormat": "XML",
               "ShareParameters": {
                    "Target":    "ALL",
                    "IPAddress": "192.168.1.100",
                    "ShareName": "share2",
                    "ShareType": "CIFS",
                    "UserName":  "dell",
                    "Password":  "111111",
                    "FileName":  idrac['ip'] + ".xml"
                  }
              }

    export_scp(idrac, base_uri, rf_uri, payload, headers)

if __name__ == '__main__':
    main()

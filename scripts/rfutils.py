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

import sys
import os
import requests
import json
# http://bit.ly/2iGTEGS
from requests.packages.urllib3.exceptions import InsecureRequestWarning

user_def = "root"
pswd_def = "calvin"

# As in "(r)ed(f)ish utilites". Should probably name it something better.
class rfutils:

    def __init__ (self):
        return

    def usage(self, me):
        print("Usage: %s <ip> [user] [password]" % me)
        print("  ip:       iDRAC IP address")
        print("  user:     iDRAC login      (default: %s)" % user_def)
        print("  password: iDRAC password   (default: %s)" % pswd_def)
        exit(0)

    def die(self, msg):
        print(msg)
        exit(1)

    def check_args(self, args):
        # This could use better logic, maybe use argparse. But will do for now
        # If we don't provide credentials then it will use defaults above
        idrac = {}
        if len(sys.argv) < 2:       	# must provide iDRAC IP address
            self.usage(args.argv[0])
        if len(args.argv) == 2:
            if (args.argv[1]) == "--help" or (args.argv[1]) == "-h":
                self.usage(args.argv[0])
            else: idrac["ip"] = args.argv[1]
        else: idrac["ip"] = addr_def
        if len(args.argv) == 3: idrac["user"] = args.argv[2]
        else: idrac["user"] = user_def
        if len(args.argv) == 4: idrac["pswd"] = args.argv[3]
        else: idrac["pswd"] = pswd_def
        print("-"*65)
        print("idracip=%s, user=%s, pass=%s" %
                               (idrac["ip"],idrac["user"],idrac["pswd"]))
        return idrac

    def send_get_request(self, u, p, str):
        print("uri=%s" % str)
        print("-"*65)
        try:
            # Disable insecure-certificate-warning message
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(str, verify=False, auth=(u,p))
        except:
            # self.die("Error! Verify Redfish support or credentials.")
            raise
        return response

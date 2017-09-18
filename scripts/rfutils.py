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
        # Disable insecure-certificate-warning message
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        return

    def usage(self, me):
        print("Usage: %s <ip> [user] [password]" % me)
        print("  ip:       iDRAC IP address")
        print("  user:     iDRAC login      (default: %s)" % user_def)
        print("  password: iDRAC password   (default: %s)" % pswd_def)
        exit(1)

    def print_bold(self, str):
        bold="\033[1m"
        end="\033[0m"
        print(bold + str + end)
        return

    def print_green(self, str):
        green="\033[92m"
        end="\033[0m"
        print(green + str + end) 	# adding a coma prevents a newline
        return

    def print_red(self, str):
        red="\033[91m"
        end="\033[0m"
        print(red + str + end)
        return

    def send_get_request(self, idrac, uri):
        try:
            response = requests.get(uri, verify=False, auth=(idrac['user'],
                                                       idrac['pswd']))
        except: raise
        return response

    def send_post_request(self, idrac, uri, payload, headers):
        try:
            response = requests.post(uri, payload, headers=headers,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
        except: raise
        return response

    def send_patch_request(self, idrac, uri, payload, headers):
        try:
            response = requests.patch(uri, payload, headers=headers,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
        except: raise
        return response

    def check_args(self, args):
        # This could use better logic (argparse?) but should do for now
        idrac = {}
        if len(sys.argv) < 2:       # must pass iDRAC IP
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
        self.print_bold("ip=%s, id=%s, pw=%s" %
                                (idrac["ip"], idrac["user"], idrac["pswd"]))
        return idrac

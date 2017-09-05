#!/usr/bin/env python

import sys, os
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
        sys.exit(1)

    def die(self, msg):
        print >>sys.stderr, msg
        os._exit(1)

    def check_args(self, args):
        # This could use better logic, maybe use argparse. But will do for now
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
        print("ip=%s, id=%s, pw=%s" % (idrac["ip"],idrac["user"],idrac["pswd"]))
        return idrac

    def get_info(self, u, p, str):
        print("uri=%s" % str)
        try:
            # Disable insecure-certificate-warning message
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            system = requests.get(str, verify=False, auth=(u,p))
            systemData = system.json()
        except:
            raise
            # self.die("Error! Verify Redfish support or credentials.")
        return systemData

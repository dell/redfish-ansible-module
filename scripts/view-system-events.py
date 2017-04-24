#!/usr/bin/env python

import Common
import sys
import signal

def sig_handler(signum, frame):
    # should this do something else?
    print("Received Signal:", signum)
    exit(1)

def print_results(i):
    for logEntry in i[u'Members']:
        print("{}: {}".format(logEntry[u'Name'], logEntry[u'Created']))
        print(" {}\n".format(logEntry[u'Message']))
    return

def mymain():
    idrac = {}
    global common
    common = Common.Common()
    idrac = common.check_args(sys)

    uri = ''.join(["https://%s" % idrac["ip"],
        "/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Sel"])
    print_results(common.get_info(idrac["user"], idrac["pswd"], uri))

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sig_handler)
    try:
        mymain()
    except KeyboardInterrupt:
        common.get("Interrupt detected, exiting.")

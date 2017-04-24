#!/usr/bin/env python

import Common
import sys
import signal

def sig_handler(signum, frame):
    # should this do something else?
    print("Received Signal:", signum)
    exit(1)

def print_results(i):
    print("Power Monitoring - Historical Trends - Last Hour")
    print("Average Usage:  {} W".format(i[u'PowerMetrics'][u'AverageConsumedWatts']))
    print("Max Peak:       {} W".format(i[u'PowerMetrics'][u'MaxConsumedWatts']))
    print("Min Peak:       {} W".format(i[u'PowerMetrics'][u'MinConsumedWatts']))
    return

def mymain():
    idrac = {}
    global common
    common = Common.Common()
    idrac = common.check_args(sys)

    uri = ''.join(["https://%s" % idrac["ip"],
       "/redfish/v1/Chassis/System.Embedded.1/Power/PowerControl"])
    print_results(common.get_info(idrac["user"], idrac["pswd"], uri))

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sig_handler)
    try:
        mymain()
    except KeyboardInterrupt:
        common.get("Interrupt detected, exiting.")

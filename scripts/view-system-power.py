#!/usr/bin/env python

import rfutils
import sys
import signal
rf=rfutils.rfutils()

def sig_handler(signum, frame):
    # should this do something else?
    print("Received Signal:", signum)
    exit(1)

def print_results(i):
    print("Power Monitoring - Historical Trends - Last Hour")
    print("Average Usage: {} W".format(i[u'PowerMetrics'][u'AverageConsumedWatts']))
    print("Max Peak:      {} W".format(i[u'PowerMetrics'][u'MaxConsumedWatts']))
    print("Min Peak:      {} W".format(i[u'PowerMetrics'][u'MinConsumedWatts']))
    return

def mymain():
    idrac = {}
    idrac = rf.check_args(sys)

    uri = ''.join(["https://%s" % idrac["ip"],
       "/redfish/v1/Chassis/System.Embedded.1/Power/PowerControl"])
    print_results(rf.get_info(idrac["user"], idrac["pswd"], uri))

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sig_handler)
    try:
        mymain()
    except KeyboardInterrupt:
        rf.die("Interrupt detected, exiting.")

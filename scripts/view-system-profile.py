#!/usr/bin/env python

import Common
import sys
import signal

def sig_handler(signum, frame):
    # should this do something else?
    print("Received Signal:", signum)
    exit(1)

def print_results(i):
    print("Model:       {}").format(i[u'Model'])
    print("Mfg:         {}").format(i[u'Manufacturer'])
    print("BIOS:        {}").format(i[u'BiosVersion'])
    print("Service tag: {}").format(i[u'SKU'])
    print("Serial No.:  {}").format(i[u'SerialNumber'])
    print("Hostname:    {}").format(i[u'HostName'])
    print("Power state: {}").format(i[u'PowerState'])
    print("Asset tag:   {}").format(i[u'AssetTag'])
    print("Memory:      {}").format(i[u'MemorySummary'][u'TotalSystemMemoryGiB'])
    print("CPUs:        {}").format(i[u'ProcessorSummary'][u'Count'])
    print("CPU type:    {}").format(i[u'ProcessorSummary'][u'Model'])
    print("Status:      {}").format(i[u'Status'][u'Health'])
    return

def mymain():
    idrac = {} 
    global common
    common = Common.Common()
    idrac = common.check_args(sys)

    uri = ''.join(["https://%s" % idrac["ip"],
         "/redfish/v1/Systems/System.Embedded.1"])
    print_results(common.get_info(idrac["user"], idrac["pswd"], uri))

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sig_handler)
    try:
        mymain()
    except KeyboardInterrupt:
        common.get("Interrupt detected, exiting.")

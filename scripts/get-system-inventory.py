#!/usr/bin/env python

import rfutils
import sys
import signal
rf = rfutils.rfutils()

def sig_handler(signum, frame):
    # should this do something else?
    print("Received Signal:", signum)
    exit(1)

def print_results(response):
    i = response.json() 
    print("Model:         {}").format(i[u'Model'])
    print("Mfg:           {}").format(i[u'Manufacturer'])
    print("Part Number:   {}").format(i[u'PartNumber'])
    print("System Type:   {}").format(i[u'SystemType'])
    print("Asset tag:     {}").format(i[u'AssetTag'])
    print("Service tag:   {}").format(i[u'SKU'])
    print("Serial Number: {}").format(i[u'SerialNumber'])
    print("BIOS:          {}").format(i[u'BiosVersion'])
    print("Hostname:      {}").format(i[u'HostName'])
    print("Power state:   {}").format(i[u'PowerState'])
    print("Memory:        {}").format(i[u'MemorySummary'][u'TotalSystemMemoryGiB'])
    print("Memory health: {}").format(i[u'MemorySummary'][u'Status'][u'Health'])
    print("CPU count:     {}").format(i[u'ProcessorSummary'][u'Count'])
    print("CPU model:     {}").format(i[u'ProcessorSummary'][u'Model'])
    print("CPU health:    {}").format(i[u'ProcessorSummary'][u'Status'][u'Health'])
    print("Status:        {}").format(i[u'Status'][u'Health'])
    return

def mymain():
    idrac = rf.check_args(sys)

    uri = ''.join(["https://%s" % idrac["ip"],
          "/redfish/v1/Systems/System.Embedded.1"])

    response = rf.send_get_request(idrac["user"], idrac["pswd"], uri)
    if response.status_code == 400:
        print("Error detected!")
    else:
        print_results(response)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sig_handler)
    try:
        mymain()
    except KeyboardInterrupt:
        rf.die("Interrupt detected, exiting.")

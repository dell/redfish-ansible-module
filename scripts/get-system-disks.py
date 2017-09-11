import rfutils
import json
import requests
import sys
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
rf = rfutils.rfutils()

def get_list_of_controllers(idrac, base_uri, rf_uri):
    count = 0
    controllers = []
    response = rf.send_get_request(idrac, base_uri + rf_uri)
    rf.print_bold("status_code: %s" % response.status_code)
    if response.status_code == 400:
        rf.print_red("Something went wrong.")
        exit(1)
    data = response.json()

    for controller in data[u'Members']:
        c = controller[u'@odata.id']
        # Only PERC? What about lower-end systems with SATA controllers only?
        # if "RAID" in c or "PERC" in c:
        controllers.append(c)
    return controllers

def get_controller_disks(idrac, base_uri, controllers):
    disks = []
    for c in controllers:
        uri = base_uri + c
        response = rf.send_get_request(idrac, uri)
        data = response.json()

        rf.print_bold("Controller name: %s" % data[u'Name'])
        for disk in data[u'Devices']:
            print("Disk name: %s" % disk[u'Name'])
            print("Disk mfg: %s" % disk[u'Manufacturer'])
            print("Disk model: %s" % disk[u'Model'])
            print("Disk state: %s" % disk[u'Status'][u'State'])
            print("Disk health: %s\n" % disk[u'Status'][u'Health'])
            disks.append(disk)
    return disks

def main():
    idrac = rf.check_args(sys)

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    base_uri = "https://" + idrac['ip']
    rf_uri = "/redfish/v1/Systems/System.Embedded.1/Storage/Controllers/"

    # Get all devices
    controllers = get_list_of_controllers(idrac, base_uri, rf_uri)

    # Go through list of devices and get detailed information for each one
    disks = get_controller_disks(idrac, base_uri, controllers)

    # Uncomment if you want to see all fields returned
    # for d in disks: print(d)

if __name__ == '__main__':
    main()

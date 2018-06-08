import json
import sys
from ansible.module_utils.urls import open_url
from urllib2 import URLError, HTTPError

def usage(me):
    print("Usage: %s <ip> <user> <password>" % (me))
    exit(1)

def get_inventory(argv, redfish_uri):
    uri = "https://" + argv[1] + redfish_uri
    r = None
    data = {}
    try:
        r = open_url(uri, method="GET",
            url_username=argv[2], url_password=argv[3],
            force_basic_auth=True, validate_certs=False, use_proxy=False)
        data = json.loads(r.read())
    except HTTPError as e:
        print("HTTP [%s]" % e)
        print("HTTP [%s]" % e.code)
        exit(1)
    except URLError as e:
        print("URL [%s]" % e)
        print("URL [%s]" % e.reason)
        exit(1)
    except:
        print("Other Error")
        exit(1)

    print("Hostname:    %s" % data[u'HostName'])
    print("Model:       %s" % data[u'Model'])
    print("Mfg:         %s" % data[u'Manufacturer'])
    print("Part Number: %s" % data[u'PartNumber'])
    print("System Type: %s" % data[u'SystemType'])
    print("Service tag: %s" % data[u'SKU'])
    print("Serial No.:  %s" % data[u'SerialNumber'])
    print("BIOS:        %s" % data[u'BiosVersion'])
    print("Power state: %s" % data[u'PowerState'])
    print("Memory:      %s" % data[u'MemorySummary'][u'TotalSystemMemoryGiB'])
    print("Status:      %s" % data[u'Status'][u'Health'])
    return

def main():
    if len(sys.argv) < 4:
        usage(sys.argv[0])

    rf_uri = "/redfish/v1/Systems/System.Embedded.1"
    get_inventory(sys.argv, rf_uri)

if __name__ == '__main__':
    main()

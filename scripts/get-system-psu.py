import json
import sys
from ansible.module_utils.urls import open_url
from urllib2 import URLError, HTTPError

def usage(me):
    print("Usage: %s <ip> <user> <password>" % (me))
    exit(1)

def get_list_of_psus(argv, redfish_uri):
    uri = "https://" + argv[1] + redfish_uri
    count = 0
    psus = []
    data = {}
    r = None
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

    for psu in data[u'Links'][u'PoweredBy']:
        c = psu[u'@odata.id']
        psus.append(c)
    return psus

def get_psu_details(argv, psus):
    for i in psus:
        uri = "https://" + argv[1] + i
        print(uri)
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

        print(" Name: %s" % data[u'MemberId'])
        print(" Model: %s" % data[u'Model'])
        print(" Serial Number: %s" % data[u'SerialNumber'])
        print(" Part Number: %s" % data[u'PartNumber'])
        print(" Firmware Version: %s" % data[u'FirmwareVersion'])
        print(" Power Capacity: %s Watts" % data[u'PowerCapacityWatts'])
        print(" Power Supply Type: %s" % data[u'PowerSupplyType'])
        print(" State: %s" % data[u'Status'][u'State'])
        print(" Health: %s\n" % data[u'Status'][u'Health'])
    return

def main():
    if len(sys.argv) < 4:
        usage(sys.argv[0])

    rf_uri = "/redfish/v1/Systems/System.Embedded.1"
    psus = get_list_of_psus(sys.argv, rf_uri)
    print(psus)
    get_psu_details(sys.argv, psus)

if __name__ == '__main__':
    main()

import json
import sys
from ansible.module_utils.urls import open_url
from urllib2 import URLError, HTTPError

def usage(me):
    print("Usage: %s <ip> <user> <password>" % (me))
    exit(1)

def turn_power_on(argv, redfish_uri, payload, headers):
    uri = "https://" + argv[1] + redfish_uri
    r = None
    try:
        r = open_url(uri, data=json.dumps(payload),
            headers=headers, method="POST",
            url_username=argv[2], url_password=argv[3],
            force_basic_auth=True, validate_certs=False, use_proxy=False)
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
    return

def main():
    if len(sys.argv) < 4:
        usage(sys.argv[0])

    rf_uri="/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
    payload = {'ResetType' : 'On'}
    headers = {'content-type': 'application/json'}
    turn_power_on(sys.argv, rf_uri, payload, headers)

if __name__ == '__main__':
    main()

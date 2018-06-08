import json
import sys
import re
from ansible.module_utils.urls import open_url
from urllib2 import URLError, HTTPError

def usage(me):
    print("Usage: %s <ip> <user> <password>" % (me))
    exit(1)

def export_scp(argv, redfish_uri, payload, headers):
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

    response_output = r.__dict__
    job_id = response_output["headers"]["Location"]
    job_id = re.search("JID_.+", job_id).group()
    print("Job ID: %s" % job_id)
    return

def main():
    if len(sys.argv) < 4:
        usage(sys.argv[0])

    rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ExportSystemConfiguration"
    headers = {'content-type': 'application/json'}
    payload = {"ExportFormat": "XML",
               "ShareParameters": {
                    "Target":    "ALL",
                    "IPAddress": "10.9.160.45",
                    "ShareName": "share1",
                    "ShareType": "CIFS",
                    "UserName":  "dell",
                    "Password":  "Spr1nt71",
                    "FileName":  sys.argv[1] + ".xml"
                  }
              }

    export_scp(sys.argv, rf_uri, payload, headers)

if __name__ == '__main__':
    main()

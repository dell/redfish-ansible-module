import json
import sys
from ansible.module_utils.urls import open_url
from urllib2 import URLError, HTTPError

def usage(me):
    print("Usage: %s <ip> <user> <password>" % (me))
    exit(1)

def get_list_of_users(argv, redfish_uri):
    uri = "https://" + argv[1] + redfish_uri
    r = None
    data = {}
    user_list = []
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

    for users in data[u'Members']:
        u = users[u'@odata.id']
        u = u.replace(redfish_uri, "")       # remove part of URL, leave user Id
        user_list.append(u)
    return user_list

def get_users_details(argv, redfish_uri, user_list):
    r = None
    data = {}
    users_details = []

    for u in user_list:
        uri = "https://" + argv[1] + redfish_uri + u
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

        if not data[u'UserName'] == "":	# only care if name is not empty
            users_details.append("Id: %s" % data[u'Id'])
            users_details.append("Name: %s" % data[u'Name'])
            users_details.append("UserName: %s" % data[u'UserName'])
            users_details.append("RoleId: %s" % data[u'RoleId'])
            users_details.append("Enabled: %s\n" % data[u'Enabled'])
    return users_details

def main():
    if len(sys.argv) < 4:
        usage(sys.argv[0])

    rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.2/Accounts/"
    user_list = get_list_of_users(sys.argv, rf_uri)
    if user_list == 1:
        exit(1)			# catch return error

    # Go through list of users and get detailed information for each one
    users_details = get_users_details(sys.argv, rf_uri, user_list)
    for u in users_details:
        print(u)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2017, Dell EMC Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '0.1'}

DOCUMENTATION = """
module: idrac_users
version_added: "2.3"
short_description: User iDRAC Redfish APIs to manage iDRAC users.
options:
  choice:
    required: true
    default: None
    description:
      - What type of information to get from server
  idracip:
    required: true
    default: None
    description:
      - iDRAC IP address
  idracuser:
    required: false
    default: root
    description:
      - iDRAC user name used for authentication
  idracpswd:
    required: false
    default: calvin
    description:
      - iDRAC user password used for authentication
  userid:
    required: true
    default: None
    description:
      - ID of iDRAC user to add/delete/modify
  username:
    required: true
    default: None
    description:
      - name of iDRAC user to add/delete/modify
  userpswd:
    required: true
    default: None
    description:
      - password of iDRAC user to add/delete/modify
  userrole:
    required: true
    default: None
    description:
      - role of iDRAC user to add/delete/modify
author: "jose.delarosa@dell.com"
"""

import os
import requests
import json
import re
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ansible.module_utils.basic import AnsibleModule

def send_get_request(idrac, uri):
    try:
        response = requests.get(uri, verify=False, auth=(idrac['user'], idrac['pswd']))
        systemData = response.json()
    except:
        raise
    return systemData

def send_post_request(idrac, uri, pyld, hdrs):
    try:
        response = requests.post(uri, data=json.dumps(pyld), headers=hdrs,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
    except:
        raise
    return response

def send_patch_request(idrac, uri, pyld, hdrs):
    try:
        response = requests.patch(uri, data=json.dumps(pyld), headers=hdrs,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
        statusCode = response.status_code
    except:
        raise
    return statusCode

def send_delete_request(idrac, uri, pyld, hdrs):
    try:
        response = requests.delete(uri, data=json.dumps(pyld), headers=hdrs,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
    except:
        raise
    return response

def main():
    module = AnsibleModule(
        argument_spec = dict(
            choice = dict(required=True, type='str', default=None),
            idracip = dict(required=True, type='str', default=None),
            idracuser = dict(required=False, type='str', default='root'),
            idracpswd = dict(required=False, type='str', default='calvin'),
            userid = dict(required=False, type='str', default=None),
            username = dict(required=False, type='str', default=None),
            userpswd = dict(required=False, type='str', default=None),
            userrole = dict(required=False, type='str', default=None),
        ),
        supports_check_mode=True
    )

    params = module.params
    choice   = params['choice']

    # Build initial URI
    root_uri = ''.join(["https://%s" % params['idracip'], "/redfish/v1"])
    system_uri   = root_uri + "/Systems/System.Embedded.1" 
    chassis_uri  = root_uri + "/Chassis/System.Embedded.1" 
    manager_uri  = root_uri + "/Managers/iDRAC.Embedded.1"
    eventsvc_uri = root_uri + "/EventService"
    session_uri  = root_uri + "/Sessions"
    tasksvc_uri  = root_uri + "/TaskService"

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    IDRAC_INFO = { 'ip'   : params['idracip'],
                   'user' : params['idracuser'],
                   'pswd' : params['idracpswd']
                 } 
    USER_INFO = { 'userid'   : params['userid'],
                  'username' : params['username'],
                  'userpswd' : params['userpswd'],
                  'userrole' : params['userrole']
                 } 

    # Execute based on what we want
    if choice == "Add":
        uri = manager_uri + "/Accounts/" + USER_INFO['userid']
        plUserName = {'UserName': USER_INFO['username']}
        plPass     = {'Password': USER_INFO['userpswd']}
        plRoleID   = {'RoleId': USER_INFO['userrole']}
        headers = {'content-type': 'application/json'}
        for payload in plUserName,plPass,plRoleID:
            result = send_patch_request(IDRAC_INFO, uri, payload, headers)

    elif choice == "UpdatePassword":
        uri = manager_uri + "/Accounts/" + USER_INFO['userid']
        headers = {'content-type': 'application/json'}
        payload = {'Password': USER_INFO['userpswd']}
        result = send_patch_request(IDRAC_INFO, uri, payload, headers)

    elif choice == "UpdateRole":
        uri = manager_uri + "/Accounts/" + USER_INFO['userid']
        headers = {'content-type': 'application/json'}
        payload = {'RoleId': USER_INFO['userrole']}
        result = send_patch_request(IDRAC_INFO, uri, payload, headers)

    elif choice == "Delete":
        result = "Not yet implemented."

    else:
        result = "Invalid Option."

    module.exit_json(result=result)

if __name__ == '__main__':
    main()

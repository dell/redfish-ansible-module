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
module: idrac_storage
version_added: "2.3"
short_description: Use iDRAC Redfish APIs to get system storage information.
options:
  choice:
    required: true
    default: None
    description:
      - Type of action to run on server
  idracip:
    required: true
    default: None
    description:
      - iDRAC IP address
  idracuser:
    required: false
    default: root
    description:
      - iDRAC user name
  idracpswd:
    required: false
    default: calvin
    description:
      - iDRAC user password
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

def main():
    module = AnsibleModule(
        argument_spec = dict(
            choice = dict(required=True, type='str', default=None),
            idracip = dict(required=True, type='str', default=None),
            idracuser = dict(required=False, type='str', default='root'),
            idracpswd = dict(required=False, type='str', default='calvin'),
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

    uri = system_uri + "/Storage/Controllers/"

    # Execute based on what we want
    if choice == "Status":
        controller_list={}
        list_of_uris=[]
        # get a list of all controllers available
        i = send_get_request(IDRAC_INFO, uri)

        for controller in i["Members"]:
            for controller_name in controller.items():
                list_of_uris.append(uri + controller_name[1].split("/")[-1])

        # for each controller, get name and status
        for storuri in list_of_uris:
            data = send_get_request(IDRAC_INFO, storuri)
            # Only interested in PERC and PCIe? What about SATA?
            if "PERC" in data['Name'] or "PCIe" in data['Name']:
                controller_list[data['Name']] = data['Status']['Health']

        # Returning a list of all controllers found along with status
        result = controller_list

    else:
        result = "Invalid Option."

    module.exit_json(result=result)

if __name__ == '__main__':
    main()

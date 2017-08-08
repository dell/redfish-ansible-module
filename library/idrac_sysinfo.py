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
module: idrac_sysinfo
version_added: "2.3"
short_description: Use iDRAC Redfish APIs to get system information.
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

    # Execute based on what we want
    if choice == "Health":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'Status'][u'Health']

    elif choice == "Model":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'Model']

    elif choice == "BiosVersion":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'BiosVersion']

    elif choice == "AssetTag":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'AssetTag']

    elif choice == "MemoryGiB":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'MemorySummary'][u'TotalSystemMemoryGiB']

    elif choice == "MemoryHealth":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'MemorySummary'][u'Status'][u'Health']

    elif choice == "CPU":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'ProcessorSummary'][u'Model']

    elif choice == "CPUHealth":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'ProcessorSummary'][u'Status'][u'Health']

    elif choice == "CPUCount":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'ProcessorSummary'][u'Count']

    elif choice == "ConsumedWatts":
        power = send_get_request(IDRAC_INFO, chassis_uri + "/Power/PowerControl")
        result = power[u'PowerConsumedWatts']

    elif choice == "PowerState":
        power = send_get_request(IDRAC_INFO, system_uri)
        result = power[u'PowerState']

    elif choice == "ServiceTag":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'SKU']

    elif choice == "SerialNumber":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'SerialNumber']

    elif choice == "IdracFirmwareVersion":
        system = send_get_request(IDRAC_INFO, manager_uri)
        result = system[u'FirmwareVersion']

    elif choice == "IdracHealth":
        system = send_get_request(IDRAC_INFO, manager_uri)
        result = system[u'Status'][u'Health']

    else:
        result = "Invalid Option."

    module.exit_json(result=result)

if __name__ == '__main__':
    main()

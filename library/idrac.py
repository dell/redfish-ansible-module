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
module: idrac
version_added: "2.3"
short_description: Talk to Dell EMC PowerEdge iDRAC using supported Redfish APIs
description:
  - For demonstration purposes only (more functionality coming soon)
  - TO DO: Add option to specify action: GET, POST, PATCH or DELETE
options:
  choice:
    required: true
    default: None
    description:
      - What type of information to get from server
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
  idracip:
    required: true
    default: None
    description:
      - iDRAC IP address
author: "jose.delarosa@dell.com"
"""

EXAMPLES = """
 - name: Get System Information
    local_action: >
       idrac choice=system idracuser={{ idracuser }}         
            idracpswd={{ idracpswd }} idracip={{ idracip }}
    register: result

  - name: Output inventory file in pretty json format
    local_action: copy content={{ result | to_nice_json }}
                       dest=/root/{{ host }}-sysinfo
"""

import os
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ansible.module_utils.basic import AnsibleModule

def send_get_request(str, u, p):
    try:
        system = requests.get(str, verify=False, auth=(u,p))
        systemData = system.json()
    except:
        raise
    return systemData

def send_post_request(str, u, p):
    try:
        system = requests.post(str, verify=False, auth=(u,p))
        systemData = system.json()
    except:
        raise
    return systemData

def send_patch_request(str, u, p):
    try:
        system = requests.patch(str, verify=False, auth=(u,p))
        systemData = system.json()
    except:
        raise
    return systemData

def send_delete_request(str, u, p):
    try:
        system = requests.delete(str, verify=False, auth=(u,p))
        systemData = system.json()
    except:
        raise
    return systemData

def main():
    module = AnsibleModule(
        argument_spec = dict(
            choice = dict(required=True, type='str', default=None),
            idracuser = dict(required=False, type='str', default='root'),
            idracpswd = dict(required=False, type='str', default='calvin'),
            idracip = dict(required=True, type='str', default=None),
        ),
        supports_check_mode=True
    )

    params = module.params
    choice    = params['choice']
    idracip   = params['idracip']
    idracuser = params['idracuser']
    idracpswd = params['idracpswd']

    # Build initial URI
    root_uri = ''.join(["https://%s" % idracip, "/redfish/v1"])
    system_uri   = root_uri + "/Systems/System.Embedded.1" 
    chassis_uri  = root_uri + "/Chassis/System.Embedded.1" 
    manager_uri  = root_uri + "/Managers/iDRAC.Embedded.1"
    eventsvc_uri = root_uri + "/EventService"
    session_uri  = root_uri + "/Sessions"
    tasksvc_uri  = root_uri + "/TaskService"

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # How do we dynamically build these?
    if choice == "Health":
        system = send_get_request(system_uri, idracuser, idracpswd)
        result = system[u'Status'][u'Health']
    elif choice == "Model":
        system = send_get_request(system_uri, idracuser, idracpswd)
        result = system[u'Model']
    elif choice == "BiosVersion":
        system = send_get_request(system_uri, idracuser, idracpswd)
        result = system[u'BiosVersion']
    elif choice == "AssetTag":
        system = send_get_request(system_uri, idracuser, idracpswd)
        result = system[u'AssetTag']
    elif choice == "Memory":
        system = send_get_request(system_uri, idracuser, idracpswd)
        result = system[u'MemorySummary'][u'TotalSystemMemoryGiB']
    elif choice == "CPU":
        system = send_get_request(system_uri, idracuser, idracpswd)
        result = system[u'ProcessorSummary'][u'Model']
    elif choice == "PowerRead":
        power = send_get_request(chassis_uri + "/Power/PowerControl", idracuser, idracpswd)
        result = power[u'PowerConsumedWatts']
    elif choice == "Selog":
        result = send_get_request(manager_uri + "/Logs/Sel", idracuser, idracpswd)
    # Catch-all: display Collections available
    else:
        result = send_get_request(root_uri + "odata", idracuser, idracpswd)

    module.exit_json(result=result)

if __name__ == '__main__':
    main()

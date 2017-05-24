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
  hostname:
    required: false
    default: None
    description:
      - server name as defined in /etc/ansible/hosts
  sharehost:
    required: false
    default: None
    description:
      - CIFS/SMB share hostname for managing SCP files
  sharename:
    required: false
    default: None
    description:
      - CIFS/SMB share name for managing SCP files
  shareuser:
    required: false
    default: None
    description:
      - CIFS/SMB share user for managing SCP files
  sharepswd:
    required: false
    default: None
    description:
      - CIFS/SMB share user password for managing SCP files
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
        system = requests.get(uri, verify=False, auth=(idrac['user'], idrac['pswd']))
        systemData = system.json()
    except:
        raise
    return systemData

def send_post_request(idrac, uri, pyld, hdrs):
    try:
        response = requests.post(uri,  data=json.dumps(pyld), headers=hdrs,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
        response_output = response.__dict__
        job_id = response_output["headers"]["Location"]
        job_id = re.search("JID_.+", job_id).group()
    except:
        raise
    return job_id

def send_patch_request(idrac, uri):
    try:
        system = requests.patch(uri, verify=False, auth=(idrac['user'], idrac['pswd']))
        systemData = system.json()
    except:
        raise
    return systemData

def send_delete_request(idrac, uri):
    try:
        system = requests.delete(uri, verify=False, auth=(idrac['user'], idrac['pswd']))
        systemData = system.json()
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
            hostname  = dict(required=False, type='str', default=None),
            sharehost = dict(required=False, type='str', default=None),
            sharename = dict(required=False, type='str', default=None),
            shareuser = dict(required=False, type='str', default=None),
            sharepswd = dict(required=False, type='str', default=None),
        ),
        supports_check_mode=True
    )

    params = module.params
    choice   = params['choice']
    hostname = params['hostname']

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
    SHARE_INFO = { 'host' : params['sharehost'],
                   'name' : params['sharename'],
                   'user' : params['shareuser'],
                   'pswd' : params['sharepswd']
                 }

    # Not sure this is the best approach. Final implementation might look very different.
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
    elif choice == "Memory":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'MemorySummary'][u'TotalSystemMemoryGiB']
    elif choice == "CPU":
        system = send_get_request(IDRAC_INFO, system_uri)
        result = system[u'ProcessorSummary'][u'Model']
    elif choice == "PowerRead":
        power = send_get_request(IDRAC_INFO, chassis_uri + "/Power/PowerControl")
        result = power[u'PowerConsumedWatts']
    elif choice == "Selog":
        result = send_get_request(IDRAC_INFO, manager_uri + "/Logs/Sel")
    elif choice == "SCP":
        # timestamp to add to SCP XML file name
        ts = str(datetime.strftime(datetime.now(), "_%Y%m%d_%H%M%S"))
        uri = manager_uri + "/Actions/Oem/EID_674_Manager.ExportSystemConfiguration"
        payload = { "ExportFormat" : "XML",
                    "ShareParameters" : { "Target" : "ALL",
                         "ShareType" : "CIFS",
                         "IPAddress" : SHARE_INFO['host'],
                         "ShareName" : SHARE_INFO['name'],
                         "UserName"  : SHARE_INFO['user'],
                         "Password"  : SHARE_INFO['pswd'],
                         "FileName"  : "SCP_" + hostname + ts + ".xml"}
                  }
        headers = {'content-type': 'application/json'}
        result = send_post_request(IDRAC_INFO, uri, payload, headers)
    # Catch-all: display Collections available
    else:
        result = send_get_request(IDRAC_INFO, root_uri + "odata")

    module.exit_json(result=result)

if __name__ == '__main__':
    main()

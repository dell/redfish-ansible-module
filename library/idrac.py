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
short_description: Manage Dell EMC hardware through iDRAC Redfish APIs
options:
  category:
    required: true
    default: None
    description:
      - Action category to execute on server
  command:
    required: true
    default: None
    description:
      - Command to execute on server
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
      - iDRAC user passwore used for authentication
  userid:
    required: false
    default: None
    description:
      - ID of iDRAC user to add/delete/modify
  username:
    required: false
    default: None
    description:
      - name of iDRAC user to add/delete/modify
  userpswd:
    required: false
    default: None
    description:
      - password of iDRAC user to add/delete/modify
  userrole:
    required: false
    default: None
    description:
      - role of iDRAC user to add/delete/modify
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

system_uri   = "/Systems/System.Embedded.1" 
chassis_uri  = "/Chassis/System.Embedded.1" 
manager_uri  = "/Managers/iDRAC.Embedded.1"
eventsvc_uri = "/EventService"
session_uri  = "/Sessions"
tasksvc_uri  = "/TaskService"

def send_get_request(idrac, uri):
    result = {}
    try:
        response = requests.get(uri, verify=False, auth=(idrac['user'], idrac['pswd']))
        result["statusCode"] = response.status_code
        result["json"] = response.json()
        result["dict"] = response.__dict__
    except:
        raise
    return result

def send_post_request(idrac, uri, pyld, hdrs):
    result = {}
    try:
        response = requests.post(uri, data=json.dumps(pyld), headers=hdrs,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
        result["statusCode"] = response.status_code
        # result["json"] = response.json()
        result["dict"] = response.__dict__
    except:
        raise
    return result

def send_patch_request(idrac, uri, pyld, hdrs):
    result = {}
    try:
        response = requests.patch(uri, data=json.dumps(pyld), headers=hdrs,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
        result["statusCode"] = response.status_code
        # result["json"] = response.json()
        result["dict"] = response.__dict__
    except:
        raise
    return result

def manage_scp(command, hostname, IDRAC_INFO, SHARE_INFO, root_uri):
    if command == "ExportSCP":
        # timestamp to add to SCP XML file name
        ts = str(datetime.strftime(datetime.now(), "_%Y%m%d_%H%M%S"))
        scpuri = root_uri + manager_uri + "/Actions/Oem/EID_674_Manager.ExportSystemConfiguration"
        headers = {'content-type': 'application/json'}
        payload = { "ExportFormat" : "XML",
                    "ShareParameters" : { "Target" : "ALL",
                         "ShareType" : "CIFS",
                         "IPAddress" : SHARE_INFO['host'],
                         "ShareName" : SHARE_INFO['name'],
                         "UserName"  : SHARE_INFO['user'],
                         "Password"  : SHARE_INFO['pswd'],
                         "FileName"  : "SCP_" + hostname + ts + ".xml"}
                  }
        data = send_post_request(IDRAC_INFO, scpuri, payload, headers)

        data_dict = data["dict"]
        job_id = data_dict["headers"]["Location"]
        # This returns the iDRAC Job ID: a string
        result = re.search("JID_.+", job_id).group()

    elif command == "ImportSCP":
        result = "Import option not yet implemented."

    else:
        result = "Invalid Option."
    return result

def manage_storage(command, IDRAC_INFO, root_uri):
    storageuri = root_uri + system_uri + "/Storage/Controllers/"

    # Get a list of all storage controllers and build respective URIs
    controller_list={}
    list_of_uris=[]
    data = send_get_request(IDRAC_INFO, storageuri)

    for controller in data["json"]["Members"]:
        for controller_name in controller.items():
            list_of_uris.append(storageuri + controller_name[1].split("/")[-1])

    # for each controller, get name and status
    for storuri in list_of_uris:
        data = send_get_request(IDRAC_INFO, storuri)
        # Only interested in PERC and PCIe? What about SATA?
        if "PERC" in data["json"]['Name'] or "PCIe" in data["json"]['Name']:
            # Execute based on what we want
            if command == "GetStorageInfo":
                # Returns a list of all controllers along with status
                controller_list[data["json"]['Name']] = data["json"]['Status']['Health']
            elif command == "ListDevices":
                # Returns a list of all controllers along with devices. Messy, clean up.
                controller_list[data["json"]['Name']] = data["json"]['Devices']
            else:
                controller_list['Invalid'] = "Invalid Option"
                break

    # Returning a list of all controllers along with status
    result = json.dumps(controller_list)
    return result

def manage_power(command, IDRAC_INFO, root_uri):
    headers = {'content-type': 'application/json'}
    reseturi = root_uri + system_uri + "/Actions/ComputerSystem.Reset"
    idracreseturi = root_uri + manager_uri + "/Actions/Manager.Reset"

    if command == "PowerState":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'PowerState']
    elif command == "PowerOn":
        payload = {'ResetType': 'On'}
        data = send_post_request(IDRAC_INFO, reseturi, payload, headers)
        result = data["statusCode"]
    elif command == "PowerOff":
        payload = {'ResetType': 'ForceOff'}
        data = send_post_request(IDRAC_INFO, reseturi, payload, headers)
        result = data["statusCode"]
    elif command == "GracefulRestart":
        payload = {'ResetType': 'GracefulRestart'}
        data = send_post_request(IDRAC_INFO, reseturi, payload, headers)
        result = data["statusCode"]
    elif command == "GracefulShutdown":
        payload = {'ResetType': 'GracefulShutdown'}
        data = send_post_request(IDRAC_INFO, reseturi, payload, headers)
        result = data["statusCode"]
    elif command == "IdracGracefulRestart":
        payload = {'ResetType': 'GracefulRestart'}
        data = send_post_request(IDRAC_INFO, idracreseturi, payload, headers)
        result = data["statusCode"]
    else:
        result = "Invalid Option."
    return result

def manage_users(command, IDRAC_INFO, USER_INFO, root_uri):
    headers = {'content-type': 'application/json'}
    uri = root_uri + manager_uri + "/Accounts/" + USER_INFO['userid']

    if command == "AddUser":
        plUserName = {'UserName': USER_INFO['username']}
        plPass     = {'Password': USER_INFO['userpswd']}
        plRoleID   = {'RoleId': USER_INFO['userrole']}
        for payload in plUserName,plPass,plRoleID:
            data = send_patch_request(IDRAC_INFO, uri, payload, headers)
        result = data["statusCode"]

    elif command == "UpdateUserPassword":
        payload = {'Password': USER_INFO['userpswd']}
        data = send_patch_request(IDRAC_INFO, uri, payload, headers)
        result = data["statusCode"]

    elif command == "UpdateUserRole":
        payload = {'RoleId': USER_INFO['userrole']}
        data = send_patch_request(IDRAC_INFO, uri, payload, headers)
        result = data["statusCode"]

    elif command == "DeleteUser":
        result = "Not yet implemented."

    else:
        result = "Invalid Option."
    return result

def get_logs(command, IDRAC_INFO, root_uri):
    if command == "GetSelog":
        data = send_get_request(IDRAC_INFO, root_uri + manager_uri + "/Logs/Sel")
    elif command == "GetLclog":
        data = send_get_request(IDRAC_INFO, root_uri + manager_uri + "/Logs/Lclog")
    else:
        data["json"] = "Invalid Option."
    return data["json"]

def get_firmware_inventory(command, IDRAC_INFO, root_uri):
    if command == "GetInventory":
        data = send_get_request(IDRAC_INFO, root_uri + "/UpdateService/FirmwareInventory/")

    result = "Not implemented yet"

    return result 

def get_inventory(command, IDRAC_INFO, root_uri):
    if command == "ServerStatus":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'Status'][u'Health']
    elif command == "ServerModel":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'Model']
    elif command == "BiosVersion":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'BiosVersion']
    elif command == "ServerManufacturer":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'Manufacturer']
    elif command == "ServerPartNumber":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'PartNumber']
    elif command == "SystemType":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'SystemType']
    elif command == "AssetTag":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'AssetTag']
    elif command == "MemoryGiB":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'MemorySummary'][u'TotalSystemMemoryGiB']
    elif command == "MemoryHealth":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'MemorySummary'][u'Status'][u'Health']
    elif command == "CPUModel":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'ProcessorSummary'][u'Model']
    elif command == "CPUHealth":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'ProcessorSummary'][u'Status'][u'Health']
    elif command == "CPUCount":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'ProcessorSummary'][u'Count']
    elif command == "ConsumedWatts":
        data = send_get_request(IDRAC_INFO, root_uri + chassis_uri + "/Power/PowerControl")
        result = data["json"][u'PowerConsumedWatts']
    elif command == "PowerState":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'PowerState']
    elif command == "ServiceTag":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'SKU']
    elif command == "SerialNumber":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        result = data["json"][u'SerialNumber']
    elif command == "IdracFirmwareVersion":
        data = send_get_request(IDRAC_INFO, root_uri + manager_uri)
        result = data["json"][u'FirmwareVersion']
    elif command == "IdracHealth":
        data = send_get_request(IDRAC_INFO, root_uri + manager_uri)
        result = data["json"][u'Status'][u'Health']
    elif command == "BootSourceOverrideMode":
        data = send_get_request(IDRAC_INFO, root_uri + system_uri)
        datadict = data["json"][u'Boot']
        if 'BootSourceOverrideMode' in datadict.keys():
            result = data["json"][u'Boot'][u'BootSourceOverrideMode']
        else:
            result = "14G only."
    else:
        result = "Invalid Command."

    return result

def main():
    module = AnsibleModule(
        argument_spec = dict(
            category = dict(required=True, type='str', default=None),
            command = dict(required=True, type='str', default=None),
            idracip = dict(required=True, type='str', default=None),
            idracuser = dict(required=False, type='str', default='root'),
            idracpswd = dict(required=False, type='str', default='calvin'),
            userid = dict(required=False, type='str', default=None),
            username = dict(required=False, type='str', default=None),
            userpswd = dict(required=False, type='str', default=None),
            userrole = dict(required=False, type='str', default=None),
            hostname  = dict(required=False, type='str', default=None),
            sharehost = dict(required=False, type='str', default=None),
            sharename = dict(required=False, type='str', default=None),
            shareuser = dict(required=False, type='str', default=None),
            sharepswd = dict(required=False, type='str', default=None),
        ),
        supports_check_mode=True
    )

    params = module.params
    category = params['category']
    command  = params['command']
    hostname = params['hostname']

    # Build initial URI
    root_uri = ''.join(["https://%s" % params['idracip'], "/redfish/v1"])

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
    USER_INFO = { 'userid'   : params['userid'],
                  'username' : params['username'],
                  'userpswd' : params['userpswd'],
                  'userrole' : params['userrole']
                 }

    # Execute based on what we want
    if category == "Inventory":
        result = get_inventory(command, IDRAC_INFO, root_uri)
    elif category == "Firmware":
        result = get_firmware_inventory(command, IDRAC_INFO, root_uri)
    elif category == "Logs":
        result = get_logs(command, IDRAC_INFO, root_uri)
    elif category == "Users":
        result = manage_users(command, IDRAC_INFO, USER_INFO, root_uri)
    elif category == "Power":
        result = manage_power(command, IDRAC_INFO, root_uri)
    elif category == "Storage":
        result = manage_storage(command, IDRAC_INFO, root_uri)
    elif category == "SCP":
        result = manage_scp(command, hostname, IDRAC_INFO, SHARE_INFO, root_uri)
    else:
        result = "Invalid Category"

    module.exit_json(result=result)

if __name__ == '__main__':
    main()

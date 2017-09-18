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

def send_get_request(idrac, uri):
    result = {}
    try:
        response = requests.get(uri, verify=False, auth=(idrac['user'], idrac['pswd']))
    except:
        raise			# Do we let module exit or should we return an error value?
    return response

def send_post_request(idrac, uri, pyld, hdrs):
    result = {}
    try:
        response = requests.post(uri, data=json.dumps(pyld), headers=hdrs,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
    except:
        raise			# Do we let module exit or should we return an error value?
    return response

def send_patch_request(idrac, uri, pyld, hdrs):
    result = {}
    try:
        response = requests.patch(uri, data=json.dumps(pyld), headers=hdrs,
                           verify=False, auth=(idrac['user'], idrac['pswd']))
    except:
        raise			# Do we let module exit or should we return an error value?
    return response

def manage_scp(command, hostname, IDRAC_INFO, SHARE_INFO, root_uri):
    if command == "ExportSCP":
        # timestamp to add to SCP XML file name
        ts = str(datetime.strftime(datetime.now(), "_%Y%m%d_%H%M%S"))
        scpuri = root_uri + "/Actions/Oem/EID_674_Manager.ExportSystemConfiguration"
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
        response = send_post_request(IDRAC_INFO, scpuri, payload, headers)
        data_dict = response.__dict__

        job_id = data_dict["headers"]["Location"]
        result = re.search("JID_.+", job_id).group()	# Returns Job ID

    elif command == "ImportSCP":
        result = "Not yet implemented."

    else:
        result = "Invalid Command."
    return result

def manage_storage(command, IDRAC_INFO, root_uri, rf_uri):
    result = []

    # Get a list of all storage controllers and build respective URIs
    controllers = []
    response = send_get_request(IDRAC_INFO, root_uri + rf_uri)
    data = response.json()

    for controller in data[u'Members']:
        c = controller[u'@odata.id']
        controllers.append(c)

    for c in controllers:
        uri = root_uri + c
        response = send_get_request(IDRAC_INFO, uri)
        data = response.json()

        if command == "GetControllerInfo":
            controller = {}
            controller['Name']   = data[u'Name']	# Name of storage controller
            controller['Health'] = data[u'Status'][u'Health']
            result.append(controller)

        elif command == "GetDiskInfo":
            for device in data[u'Devices']:
                disk = {}
                disk['Controller']   = data[u'Name']	# Name of storage controller
                disk['Name']         = device[u'Name']
                disk['Manufacturer'] = device[u'Manufacturer']
                disk['Model']        = device[u'Model']
                disk['State']        = device[u'Status'][u'State']
                disk['Health']       = device[u'Status'][u'Health']
                result.append(disk)

        else:
            result = "Invalid Command."

    return result

def manage_idrac_power(command, IDRAC_INFO, root_uri):
    headers = {'content-type': 'application/json'}
    uri = root_uri + "/Actions/Manager.Reset"

    if command == "IdracGracefulRestart":
        payload = {'ResetType': 'GracefulRestart'}
        response = send_post_request(IDRAC_INFO, uri, payload, headers)
        result = response.status_code

    else:
        result = "Invalid Command."

    return

def manage_system_power(command, IDRAC_INFO, root_uri):
    headers = {'content-type': 'application/json'}
    uri = root_uri + "/Actions/ComputerSystem.Reset"

    if command == "PowerOn":
        payload = {'ResetType': 'On'}
        response = send_post_request(IDRAC_INFO, uri, payload, headers)
        result = response.status_code

    elif command == "PowerOff":
        payload = {'ResetType': 'ForceOff'}
        response = send_post_request(IDRAC_INFO, uri, payload, headers)
        result = response.status_code

    elif command == "GracefulRestart":
        payload = {'ResetType': 'GracefulRestart'}
        response = send_post_request(IDRAC_INFO, uri, payload, headers)
        result = response.status_code

    elif command == "GracefulShutdown":
        payload = {'ResetType': 'GracefulShutdown'}
        response = send_post_request(IDRAC_INFO, uri, payload, headers)
        result = response.status_code

    else:
        result = "Invalid Command."
    return result

def manage_users(command, IDRAC_INFO, USER_INFO, root_uri):
    headers = {'content-type': 'application/json'}
    uri = root_uri + "/Accounts/" + USER_INFO['userid']

    if command == "AddUser":
        plUserName = {'UserName': USER_INFO['username']}
        plPass     = {'Password': USER_INFO['userpswd']}
        plRoleID   = {'RoleId': USER_INFO['userrole']}
        for payload in plUserName,plPass,plRoleID:
            response = send_patch_request(IDRAC_INFO, uri, payload, headers)
        result = response.status_code

    elif command == "UpdateUserPassword":
        payload = {'Password': USER_INFO['userpswd']}
        response = send_patch_request(IDRAC_INFO, uri, payload, headers)
        result = response.status_code

    elif command == "UpdateUserRole":
        payload = {'RoleId': USER_INFO['userrole']}
        response = send_patch_request(IDRAC_INFO, uri, payload, headers)
        result = response.status_code

    elif command == "DeleteUser":
        result = "Not yet implemented."

    else:
        result = "Invalid Command."
    return result

def get_logs(command, IDRAC_INFO, root_uri):
    result = []
    if command == "GetSelog":			# System Event logs
        response = send_get_request(IDRAC_INFO, root_uri + "/Logs/Sel")
        data = response.json()
        # I only extract some parameters, not all
        for logEntry in data[u'Members']:
            entry = {}
            entry['Name']    = logEntry[u'Name']
            entry['Created'] = logEntry[u'Created']
            entry['Message'] = logEntry[u'Message']
            result.append(entry)

    elif command == "GetLclog":			# Lifecycle controller logs
        response = send_get_request(IDRAC_INFO, root_uri + "/Logs/Lclog")
        data = response.json()
        # I only extract some parameters, not all
        for logEntry in data[u'Members']:
            entry = {}
            entry['Name']     = logEntry[u'Name']
            entry['Created']  = logEntry[u'Created']
            entry['Message']  = logEntry[u'Message']
            entry['Severity'] = logEntry[u'Severity']
            result.append(entry)
    else:
        result = "Invalid Command."
    return result

def get_firmware_inventory(command, IDRAC_INFO, root_uri, rf_uri):
    result = {}
    devices = []
    if command == "GetInventory":
        response = send_get_request(IDRAC_INFO, root_uri + rf_uri)
        if response.status_code == 200:		# success
            data = response.json()
            for device in data[u'Members']:
                d = device[u'@odata.id']
                d = d.replace(rf_uri, "")	# leave just device name
                if "Installed" in d:
                    # Get details for each device that is relevant
                    uri = root_uri + rf_uri + d
                    response = send_get_request(IDRAC_INFO, uri)
                    if response.status_code == 200:	# success
                        data = response.json()
                        result[data[u'Name']] = data[u'Version']

        # PropertyValueTypeError
        elif response.status_code == 400:
            result = "14G only"
        else:
            result = "error code %s" % response.status_code 
    else:
        result = "Invalid Command."
    return result 

def manage_bios(command, IDRAC_INFO, root_uri):
    result = {}
    if command == "GetAttributes":
        response = send_get_request(IDRAC_INFO, root_uri + "/Bios")
        if response.status_code == 200:		# success
            data = response.json()
            for attribute in data[u'Attributes'].items():
                result[attribute[0]] = attribute[1]
        # PropertyValueTypeError
        elif response.status_code == 400:
            result = "14G only"
        else:
            result = "error code %s" % response.status_code 

    elif command == "GetBootOrder":
        # Get boot mode first as it will determine what attribute to read
        response = send_get_request(IDRAC_INFO, root_uri + "/Bios")
        if response.status_code == 200:		# success
            data = response.json()
            boot_mode = data[u'Attributes']["BootMode"]
            response = send_get_request(IDRAC_INFO, root_uri + "/BootSources")
            if response.status_code == 200:		# success
                data = response.json()
                if boot_mode == "Uefi":
                    boot_seq = "UefiBootSeq"
                else:
                    boot_seq = "BootSeq"
                boot_devices = data[u'Attributes'][boot_seq]
                for b in boot_devices:
                    result["device%s" % b[u'Index']] = b[u'Name']
        # PropertyValueTypeError
        elif response.status_code == 400:
            result = "14G only"
        else:
            result = "error code %s" % response.status_code 
    else:
        result = "Invalid Command."
    return result 

def get_inventory(command, IDRAC_INFO, root_uri):
    result = {}
    if command == "GetInventory":
        response = send_get_request(IDRAC_INFO, root_uri)
        data = response.json()

        # There could be more information to extract
        result['Status']       = data[u'Status'][u'Health']
        result['HostName']     = data[u'HostName']
        result['PowerState']   = data[u'PowerState']
        result['Model']        = data[u'Model']
        result['Manufacturer'] = data[u'Manufacturer']
        result['PartNumber']   = data[u'PartNumber']
        result['SystemType']   = data[u'SystemType']
        result['AssetTag']     = data[u'AssetTag']
        result['ServiceTag']   = data[u'SKU']
        result['SerialNumber'] = data[u'SerialNumber']
        result['BiosVersion']  = data[u'BiosVersion']
        result['MemoryTotal']  = data[u'MemorySummary'][u'TotalSystemMemoryGiB']
        result['MemoryHealth'] = data[u'MemorySummary'][u'Status'][u'Health']
        result['CpuCount']     = data[u'ProcessorSummary'][u'Count']
        result['CpuModel']     = data[u'ProcessorSummary'][u'Model']
        result['CpuHealth']    = data[u'ProcessorSummary'][u'Status'][u'Health']

        datadict = data[u'Boot']
        if 'BootSourceOverrideMode' in datadict.keys():
            result['BootSourceOverrideMode'] = data[u'Boot'][u'BootSourceOverrideMode']
        else:
            result['BootSourceOverrideMode'] = "14G only"

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

    # Build initial URI
    root_uri = "https://" + params['idracip']

    # Execute based on what we want. Notice that some rf_uri values have an
    # ending slash ('/') and other don't. It's all by design and depends on
    # how the URI is used in each function.
    if category == "Inventory":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1/"
        result = get_inventory(command, IDRAC_INFO, root_uri + rf_uri)

    elif category == "Firmware":
        rf_uri = "/redfish/v1/UpdateService/FirmwareInventory/"
        result = get_firmware_inventory(command, IDRAC_INFO, root_uri, rf_uri)

    elif category == "Logs":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
        result = get_logs(command, IDRAC_INFO, root_uri + rf_uri)

    elif category == "Users":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/"
        result = manage_users(command, IDRAC_INFO, USER_INFO, root_uri + rf_uri)

    elif category == "SystemPower":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1/"
        result = manage_system_power(command, IDRAC_INFO, root_uri + rf_uri)

    elif category == "IdracPower":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
        result = manage_idrac_power(command, IDRAC_INFO, root_uri + rf_uri)

    elif category == "Storage":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1/Storage/Controllers/"
        result = manage_storage(command, IDRAC_INFO, root_uri, rf_uri)

    elif category == "SCP":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
        result = manage_scp(command, hostname, IDRAC_INFO, SHARE_INFO, root_uri + rf_uri)

    elif category == "Bios":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1"
        result = manage_bios(command, IDRAC_INFO, root_uri + rf_uri)

    else:
        result = "Invalid Category"

    module.exit_json(result=result)

if __name__ == '__main__':
    main()

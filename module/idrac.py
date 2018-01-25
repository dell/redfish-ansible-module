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
                    'metadata_version': '1.1'}

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
  hostname:
    required: false
    default: None
    description:
      - server name to add to filename when exporting SCP file
  scpfile:
    required: false
    default: None
    description:
      - SCP file to import
  bootdevice:
    required: false
    default: None
    description:
      - bootdevice when setting boot configuration
  bios_attributes:
    required: false
    default: None
    description:
      - dict where we specify BIOS attributes to set
  idrac_attributes:
    required: false
    default: None
    description:
      - dict where we specify IDRAC attributes to set
  FWPath:
    required: false
    default: None
    description:
      - firmware binary path which is used to upload firmware
  Model:
    required: false
    default: None
    description:
      - system model name like R940, R740
  InstallOption:
    required: false
    choices: [ Now, NowAndReboot, NextReboot ]
    default: None
    description:
      - firmware installation option like Now or NextReboot

author: "jose.delarosa@dell.com", github: jose-delarosa
"""

import os
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.rf_utils import RedfishUtils

def main():
    result = {}
    module = AnsibleModule(
        argument_spec = dict(
            category   = dict(required=True, type='str', default=None),
            command    = dict(required=True, type='str', default=None),
            idracip    = dict(required=True, type='str', default=None),
            idracuser  = dict(required=False, type='str', default='root'),
            idracpswd  = dict(required=False, type='str', default='calvin', no_log=True),
            userid     = dict(required=False, type='str', default=None),
            username   = dict(required=False, type='str', default=None),
            userpswd   = dict(required=False, type='str', default=None, no_log=True),
            userrole   = dict(required=False, type='str', default=None),
            hostname   = dict(required=False, type='str', default=None),
            scpfile    = dict(required=False, type='str', default=None),
            sharehost  = dict(required=False, type='str', default=None),
            sharename  = dict(required=False, type='str', default=None),
            shareuser  = dict(required=False, type='str', default=None),
            sharepswd  = dict(required=False, type='str', default=None, no_log=True),
            bootdevice = dict(required=False, type='str', default=None),
            idrac_attributes = dict(required=False, type='str', default=None),
            bios_attributes = dict(required=False, type='str', default=None),
	    FWPath     = dict(required=False, type='str', default=None),
	    Model      = dict(required=False, type='str', default=None),
	    InstallOption = dict(required=False, type='str', default=None, choices=['Now', 'NowAndReboot', 'NextReboot']),
        ),
        supports_check_mode=False
    )

    params = module.params
    category   = params['category']
    command    = params['command']
    hostname   = params['hostname']
    scpfile    = params['scpfile']
    bootdevice = params['bootdevice']

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

    # Get token
    # token = 
    rf_utils = RedfishUtils()

    # Execute based on what we want. Notice that some rf_uri values have an
    # ending slash ('/') and other don't. It's all by design and depends on
    # how the URI is used in each function.
    if category == "Inventory":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1/"
        if command == "GetSystemInventory":
            result = rf_utils.get_system_inventory(IDRAC_INFO, root_uri + rf_uri)
        elif command == "GetPsuInventory":
            result = rf_utils.get_psu_inventory(IDRAC_INFO, root_uri, rf_uri)
        elif command == "GetCpuInventory":
            rf_uri = "/redfish/v1/Systems/System.Embedded.1/Processors"
            result = rf_utils.get_cpu_inventory(IDRAC_INFO, root_uri, rf_uri)
        elif command == "GetNicInventory":
            rf_uri = "/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/"
            result = rf_utils.get_nic_inventory(IDRAC_INFO, root_uri, rf_uri)
        elif command == "GetFanInventory":
            rf_uri = "/redfish/v1/Chassis/System.Embedded.1/Thermal"
            result = rf_utils.get_fan_inventory(IDRAC_INFO, root_uri + rf_uri)
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Firmware":
        rf_uri = "/redfish/v1/UpdateService/FirmwareInventory/"
        if command == "GetInventory":
           result = rf_utils.get_firmware_inventory(IDRAC_INFO, root_uri, rf_uri)
	elif command == "UploadFirmware":
            result = rf_utils.upload_firmware(IDRAC_INFO, root_uri, params['FWPath'])
	elif command == "FirmwareCompare":
            result = rf_utils.compare_firmware(IDRAC_INFO, root_uri, "/tmp/Catalog", params['Model'])
        elif command == "InstallFirmware":
            result = rf_utils.schedule_firmware_update(IDRAC_INFO, root_uri, params['InstallOption'])
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Logs":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
        if command == "GetSELogs":
            result = rf_utils.get_selogs(IDRAC_INFO, root_uri + rf_uri)
        elif command == "GetLCLogs":
            result = rf_utils.get_lclogs(IDRAC_INFO, root_uri + rf_uri)
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Users":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
        if command == "ListUsers":
            result = rf_utils.list_users(IDRAC_INFO, USER_INFO, root_uri, rf_uri)
        else:
            result = rf_utils.manage_users(command, IDRAC_INFO, USER_INFO, root_uri, rf_uri)

    elif category == "Power":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1"
        result = rf_utils.manage_system_power(command, IDRAC_INFO, root_uri + rf_uri)

    elif category == "Storage":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1/Storage/Controllers/"
        if command == "GetControllerInventory":
            result = rf_utils.get_stor_cont_info(IDRAC_INFO, root_uri, rf_uri)
        elif command == "GetDiskInventory":
            result = rf_utils.get_disk_info(IDRAC_INFO, root_uri, rf_uri)
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "SCP":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager"
        if command == "ExportSCP":
            result = rf_utils.export_scp(IDRAC_INFO, SHARE_INFO, hostname, root_uri + rf_uri + ".ExportSystemConfiguration")
        elif command == "ImportSCP":
            result = rf_utils.import_scp(IDRAC_INFO, SHARE_INFO, scpfile, root_uri + rf_uri + ".ImportSystemConfiguration")
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Bios":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1"
        if command == "GetAttributes":
            result = rf_utils.get_bios_attributes(IDRAC_INFO, root_uri + rf_uri)
        elif command == "GetBootOrder":
            result = rf_utils.get_bios_boot_order(IDRAC_INFO, root_uri + rf_uri)
        elif command == "SetOneTimeBoot":
            result = rf_utils.set_one_time_boot_device(IDRAC_INFO, bootdevice, root_uri + rf_uri)
        elif command == "SetDefaultSettings":
            rf_uri = "/redfish/v1/Systems/System.Embedded.1/Bios/Actions/Bios.ResetBios/"
            result = rf_utils.set_bios_default_settings(IDRAC_INFO, root_uri + rf_uri)
        elif command == "SetAttributes":
	    rf_uri = '/redfish/v1/Systems/System.Embedded.1/Bios/Settings'
	    result = rf_utils.set_bios_attributes(IDRAC_INFO, root_uri + rf_uri, params['bios_attributes'])
        elif command == "ConfigJob":
            rf_uri = '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs'
            result = rf_utils.create_bios_config_job(IDRAC_INFO, root_uri + rf_uri)
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Idrac":
        if command == "SetDefaultSettings":
            rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/DellManager.ResetToDefaults"
            result = rf_utils.set_idrac_default_settings(IDRAC_INFO, root_uri + rf_uri)
        elif command == "GracefulRestart":
            rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
            result = rf_utils.restart_idrac_gracefully(IDRAC_INFO, root_uri + rf_uri)
        elif command == "GetAttributes":
            rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
            result = rf_utils.get_idrac_attributes(IDRAC_INFO, root_uri + rf_uri)
        elif command == "SetAttributes":
            rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Attributes"
            result = rf_utils.set_idrac_attributes(IDRAC_INFO, root_uri + rf_uri, params['idrac_attributes'])
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    else:
        result = { 'ret': False, 'msg': 'Invalid Category'}

    # Return data back or fail with proper message
    if result['ret'] == True:
        del result['ret']		# Don't want to pass this back
        module.exit_json(result=result)
    else:
        module.fail_json(msg=result['msg'])

if __name__ == '__main__':
    main()

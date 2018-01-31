#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
module: redfish
version_added: "2.3"
short_description: Out-Of-Band management using Redfish APIs
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
  baseuri:
    required: true
    default: None
    description:
      - Base URI of OOB controller
  user:
    required: false
    default: root
    description:
      - User for authentication with OOB controller
  password:
    required: false
    default: calvin
    description:
      - Password for authentication with OOB controller
  userid:
    required: false
    default: None
    description:
      - ID of user to add/delete/modify
  username:
    required: false
    default: None
    description:
      - name of user to add/delete/modify
  userpswd:
    required: false
    default: None
    description:
      - password of user to add/delete/modify
  userrole:
    required: false
    default: None
    description:
      - role of user to add/delete/modify
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
            baseuri    = dict(required=True, type='str', default=None),
            user       = dict(required=False, type='str', default='root'),
            password   = dict(required=False, type='str', default='calvin', no_log=True),
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

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    category   = module.params['category']
    command    = module.params['command']
    hostname   = module.params['hostname']
    scpfile    = module.params['scpfile']
    bootdevice = module.params['bootdevice']

    # admin credentials used for authentication
    creds = { 'user': module.params['user'],
              'pswd': module.params['password']
    }
    # share information for exporting/importing SCP files
    share = { 'host' : module.params['sharehost'],
                   'name' : module.params['sharename'],
                   'user' : module.params['shareuser'],
                   'pswd' : module.params['sharepswd']
    }
    # user to add/modify/delete
    user = { 'userid'   : module.params['userid'],
             'username' : module.params['username'],
             'userpswd' : module.params['userpswd'],
             'userrole' : module.params['userrole']
    }

    # Build root URI
    root_uri = "https://" + module.params['baseuri']
    rf_utils = RedfishUtils(creds, root_uri)

    # Organize actions by Categories / Commands
    if category == "UserManagement":
        result = rf_utils._find_account_service()     # find accounts_uri
        if result['ret'] == True:	# Go on only if we find an account service
            if command == "ListUsers":
                result = rf_utils.list_users(user)
            elif command == "AddUser":
                result = rf_utils.add_user(user)
            elif command == "EnableUser":
                result = rf_utils.enable_user(user)
            elif command == "DeleteUser":
                result = rf_utils.delete_user(user)
            elif command == "DisableUser":
                result = rf_utils.disable_user(user)
            elif command == "UpdateUserRole":
                result = rf_utils.update_user_role(user)
            elif command == "UpdateUserPassword":
                result = rf_utils.update_user_password(user)
            else:
                result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Inventory":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1"
        if command == "GetSystemInventory":
            result = rf_utils.get_system_inventory(creds, root_uri + rf_uri)
        elif command == "GetPsuInventory":
            result = rf_utils.get_psu_inventory(creds, root_uri, rf_uri)
        elif command == "GetCpuInventory":
            result = rf_utils.get_cpu_inventory(creds, root_uri, rf_uri + "/Processors")
        elif command == "GetNicInventory":
            result = rf_utils.get_nic_inventory(creds, root_uri, rf_uri + "/EthernetInterfaces")
        elif command == "GetFanInventory":
            rf_uri = "/redfish/v1/Chassis/System.Embedded.1/Thermal"
            result = rf_utils.get_fan_inventory(creds, root_uri + rf_uri)
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Firmware":
        rf_uri = "/redfish/v1/UpdateService/FirmwareInventory"
        if command == "GetInventory":
            result = rf_utils.get_firmware_inventory(creds, root_uri, rf_uri)
	elif command == "FirmwareCompare":
            result = rf_utils.compare_firmware(creds, root_uri, rf_uri, "/tmp/Catalog", module.params['Model'])
	elif command == "UploadFirmware":
            result = rf_utils.upload_firmware(creds, root_uri, rf_uri, module.params['FWPath'])
        elif command == "InstallFirmware":
            result = rf_utils.schedule_firmware_update(creds, root_uri, rf_uri, module.params['InstallOption'])
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Power":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1"
        result = rf_utils.manage_system_power(command, creds, root_uri + rf_uri)

    elif category == "Storage":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1"
        if command == "GetControllerInventory":
            result = rf_utils.get_storage_controller_info(creds, root_uri, rf_uri + "/Storage/Controllers/")
        elif command == "GetDiskInventory":
            result = rf_utils.get_disk_info(creds, root_uri, rf_uri + "/Storage/Controllers/")
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    elif category == "Bios":
        rf_uri = "/redfish/v1/Systems/System.Embedded.1"
        if command == "GetAttributes":
            result = rf_utils.get_bios_attributes(creds, root_uri + rf_uri)
        elif command == "GetBootOrder":
            result = rf_utils.get_bios_boot_order(creds, root_uri + rf_uri)
        elif command == "SetOneTimeBoot":
            result = rf_utils.set_one_time_boot_device(creds, bootdevice, root_uri + rf_uri)
        elif command == "SetDefaultSettings":
            result = rf_utils.set_bios_default_settings(creds, root_uri + rf_uri + "/Bios/Actions/Bios.ResetBios")
        elif command == "SetAttributes":
	    result = rf_utils.set_bios_attributes(creds, root_uri + rf_uri + "/Bios/Settings",
                                                   module.params['bios_attributes'])
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    # Dell-specific
    elif category == "Logs":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
        if command == "GetSELogs":
            result = rf_utils.get_se_logs(creds, root_uri + rf_uri + "/Logs/Sel")
        elif command == "GetLCLogs":
            result = rf_utils.get_lc_logs(creds, root_uri + rf_uri + "/Logs/Lclog")
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    # Dell-specific
    elif category == "SCP":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
        if command == "ExportSCP":
            result = rf_utils.export_scp(creds, share, hostname,
                              root_uri + rf_uri + "/Actions/Oem/EID_674_Manager.ExportSystemConfiguration")
        elif command == "ImportSCP":
            result = rf_utils.import_scp(creds, share, scpfile,
                              root_uri + rf_uri + "/Actions/Oem/EID_674_Manager.ImportSystemConfiguration")
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}

    # Dell-specific
    elif category == "Idrac":
        rf_uri = "/redfish/v1/Managers/iDRAC.Embedded.1"
        if command == "SetDefaultSettings":
            result = rf_utils.set_idrac_default_settings(creds,
                                     root_uri + rf_uri + "/Actions/Oem/DellManager.ResetToDefaults")
        elif command == "GracefulRestart":
            result = rf_utils.restart_idrac_gracefully(creds, root_uri + rf_uri)
        elif command == "GetAttributes":
            result = rf_utils.get_idrac_attributes(creds, root_uri + rf_uri)
        elif command == "SetAttributes":
            result = rf_utils.set_idrac_attributes(creds,
                                     root_uri + rf_uri + "/Attributes", module.params['idrac_attributes'])
        elif command == "ConfigJob":
            result = rf_utils.create_bios_config_job(creds, root_uri + rf_uri + "/Jobs")
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

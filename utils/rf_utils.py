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

import os
import requests
import json
import re
import xml.etree.ElementTree as ET
from distutils.version import LooseVersion
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

HEADERS = {'content-type': 'application/json'}

class RedfishUtils(object):

    def __init__(self):
        return

    def send_get_request(self, creds, uri):
        headers = {}
        if 'token' in creds:
            headers = {"X-Auth-Token": creds['token']}
        try:
            response = requests.get(uri, headers, verify=False, auth=(creds['user'], creds['pswd']))
        except:
            raise			# Do we let module exit or should we return an error value?
        return response
    
    def send_post_request(self, creds, uri, pyld, hdrs, fileName=None):
        headers = {}
        if 'token' in creds:
            headers = {"X-Auth-Token": creds['token']}
        try:
            response = requests.post(uri, data=json.dumps(pyld), headers=hdrs, files=fileName,
                               verify=False, auth=(creds['user'], creds['pswd']))
        except:
            raise			# Do we let module exit or should we return an error value?
        return response
    
    def send_patch_request(self, creds, uri, pyld, hdrs):
        try:
            response = requests.patch(uri, data=json.dumps(pyld), headers=hdrs,
                               verify=False, auth=(creds['user'], creds['pswd']))
        except:
            raise			# Do we let module exit or should we return an error value?
        return response
    
    def init_session(self, creds, sessions_uri):
        response = self.send_post_request(creds,
                                   sessions_uri,
                                   {"Password": creds["pswd"], "UserName": creds["user"]},
                                   HEADERS)

        token = response.headers["X-Auth-Token"]
        return token

    def import_scp(self, creds, share, scpfile, root_uri):
        result = {}
        payload = { "ShutdownType" : "Forced",
                    "ShareParameters" : { "Target" : "ALL",
                         "ShareType" : "CIFS",
                         "IPAddress" : share['host'],
                         "ShareName" : share['name'],
                         "UserName"  : share['user'],
                         "Password"  : share['pswd'],
                         "FileName"  : scpfile }
                  }
        response = self.send_post_request(creds, root_uri, payload, HEADERS)
        if response.status_code == 202:		# success
            result['ret'] = True
            '''
            I return the Job ID but not returning success/fail status unless I
            wait for the task to complete (which can take 45-90 seconds).
            There isn't a way to know if the task finished successfully other
            then checking if the configuration settings in the SCP file were
            applied to the server.
            '''
            data_dict = response.__dict__
            job_id_full = data_dict["headers"]["Location"]
            job_id = re.search("JID_.+", job_id_full).group()
            result = { 'ret': True, 'msg': "Job ID %s" % job_id }
        else:
            result = { 'ret': False, 'msg': "Status code %s" % response.status_code }
        return result
    
    def export_scp(self, creds, share, hostname, root_uri):
        result = {}
        # timestamp to add to SCP XML file name
        ts = str(datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S"))
        payload = { "ExportFormat" : "XML",
                    "ExportUse" : "Default",
                    "ShareParameters" : { "Target" : "ALL",
                         "ShareType" : "CIFS",
                         "IPAddress" : share['host'],
                         "ShareName" : share['name'],
                         "UserName"  : share['user'],
                         "Password"  : share['pswd'],
                         "FileName"  : hostname + "_SCP_" + ts + ".xml" }
                  }
        response = self.send_post_request(creds, root_uri, payload, HEADERS)
        if response.status_code == 202:		# success
            result['ret'] = True
            '''
            I return the Job ID but not returning success/fail status unless I
            wait for the task to complete (which can take 45-90 seconds).
            There isn't a way to know if the task finished successfully other
            than waiting to see if the SCP file is dropped in the SMB share.
            '''
            data_dict = response.__dict__
            job_id_full = data_dict["headers"]["Location"]
            job_id = re.search("JID_.+", job_id_full).group()
            result = { 'ret': True, 'msg': "Job ID %s" % job_id }
        else:
            result = { 'ret': False, 'msg': "Status code %s" % response.status_code }
        return result
    
    def get_storage_controller_info(self, creds, root_uri, rf_uri):
        result = {}
        controllers_details = []
    
        # Get a list of all storage controllers and build respective URIs
        controller_list = []
        response = self.send_get_request(creds, root_uri + rf_uri)
        if response.status_code == 200:             # success
            result['ret'] = True
            data = response.json()
    
            for controller in data[u'Members']:
                controller_list.append(controller[u'@odata.id'])
    
            for c in controller_list:
                uri = root_uri + c
                response = self.send_get_request(creds, uri)
                if response.status_code == 200:             # success
                    data = response.json()
    
                    controller = {}
                    controller['Name']   = data[u'Name']	# Name of storage controller
                    controller['Health'] = data[u'Status'][u'Health']
                    controllers_details.append(controller)
                else:
                    result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
                    return result		# no need to go through the whole loop
    
            result["entries"] = controllers_details
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def get_disk_info(self, creds, root_uri, rf_uri):
        result = {}
        disks_details = []
    
        # Get a list of all storage controllers and build respective URIs
        controller_list = []
        response = self.send_get_request(creds, root_uri + rf_uri)
        if response.status_code == 200:             # success
            result['ret'] = True
            data = response.json()
    
            for controller in data[u'Members']:
                controller_list.append(controller[u'@odata.id'])
    
            for c in controller_list:
                uri = root_uri + c
                response = self.send_get_request(creds, uri)
                if response.status_code == 200:             # success
                    data = response.json()
    
                    for device in data[u'Devices']:
                        disk = {}
                        disk['Controller']   = data[u'Name']	# Name of storage controller
                        disk['Name']         = device[u'Name']
                        disk['Manufacturer'] = device[u'Manufacturer']
                        disk['Model']        = device[u'Model']
                        disk['State']        = device[u'Status'][u'State']
                        disk['Health']       = device[u'Status'][u'Health']
                        disks_details.append(disk)
                else:
                    result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
                    return result		# no need to go through the whole loop
    
            result["entries"] = disks_details
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def restart_idrac_gracefully(self, creds, root_uri):
        result = {}
        uri = root_uri + "/Actions/Manager.Reset"
        payload = {'ResetType': 'GracefulRestart'}
        response = self.send_post_request(creds, uri, payload, HEADERS)
        if response.status_code == 204:		# success
            result['ret'] = True
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def manage_system_power(self, command, creds, root_uri):
        result = {}
        uri = root_uri + "/Actions/ComputerSystem.Reset"
    
        if command == "PowerOn":
            payload = {'ResetType': 'On'}
            response = self.send_post_request(creds, uri, payload, HEADERS)
    
        elif command == "PowerOff":
            payload = {'ResetType': 'ForceOff'}
            response = self.send_post_request(creds, uri, payload, HEADERS)
    
        elif command == "GracefulRestart":
            payload = {'ResetType': 'GracefulRestart'}
            response = self.send_post_request(creds, uri, payload, HEADERS)
    
        elif command == "GracefulShutdown":
            payload = {'ResetType': 'GracefulShutdown'}
            response = self.send_post_request(creds, uri, payload, HEADERS)
    
        else:
            result = { 'ret': False, 'msg': 'Invalid Command'}
    
        if response.status_code == 204:		# success
            result['ret'] = True
        elif response.status_code == 400:
            result = { 'ret': False, 'msg': 'Not supported on this platform'}
        elif response.status_code == 405:
            result = { 'ret': False, 'msg': "Resource not supported" }
        elif response.status_code == 409:		# verify this
            result = { 'ret': False, 'msg': "Action already implemented" }
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def list_users(self, creds, user, root_uri, rf_uri):
        result = {}
        uri = root_uri + rf_uri + "/Accounts/"
        allusers = []
        allusers_details = []
    
        response = self.send_get_request(creds, uri)
        if response.status_code == 200:		# success
            result['ret'] = True
            data = response.json()
            for users in data[u'Members']:
                allusers.append(users[u'@odata.id'])	# Here user_list[] are URIs
    
            # for each user, get details
            for uri in allusers:
                response = self.send_get_request(creds, root_uri + uri)
                # check status_code again?
                data = response.json()
                if not data[u'UserName'] == "": # only care if name is not empty
                    user = {}
                    user['Id']       = data[u'Id']
                    user['Name']     = data[u'Name']
                    user['UserName'] = data[u'UserName']
                    user['RoleId']   = data[u'RoleId']
                    allusers_details.append(user)
                result["entries"] = allusers_details
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def manage_users(self, command, creds, user, root_uri, rf_uri):
        result = {}
        uri = root_uri + rf_uri + "/Accounts/" + user['userid']
    
        if command == "AddUser":
            username = {'UserName': user['username']}
            pswd     = {'Password': user['userpswd']}
            roleid   = {'RoleId': user['userrole']}
            enabled  = {'Enabled': True}
            for payload in username,pswd,roleid,enabled:
                response = self.send_patch_request(creds, uri, payload, HEADERS)
                if response.status_code == 200:		# success
                    result['ret'] = True
                else:
                    result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        elif command == "DisableUser":
            payload = {'Enabled': False}
            response = self.send_patch_request(creds, uri, payload, HEADERS)
            if response.status_code == 200:		# success
                result['ret'] = True
            else:
                result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        elif command == "EnableUser":
            payload = {'Enabled': True}
            response = self.send_patch_request(creds, uri, payload, HEADERS)
            if response.status_code == 200:		# success
                result['ret'] = True
            else:
                result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        elif command == "UpdateUserRole":
            payload = {'RoleId': user['userrole']}
            response = self.send_patch_request(creds, uri, payload, HEADERS)
            if response.status_code == 200:		# success
                result['ret'] = True
            else:
                result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        elif command == "UpdateUserPassword":
            payload = {'Password': user['userpswd']}
            response = self.send_patch_request(creds, uri, payload, HEADERS)
            if response.status_code == 200:		# success
                result['ret'] = True
            else:
                result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        elif command == "DeleteUser":
            payload = {'UserName': ""}
            response = self.send_patch_request(creds, uri, payload, HEADERS)
            if response.status_code == 200:		# success
                result['ret'] = True
            else:
                result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        else:
            result = { 'ret': False, 'msg': "Invalid Command" }
    
        return result
    
    def get_se_logs(self, creds, uri):
        # System Event logs
        result = {}
        allentries = []
        response = self.send_get_request(creds, uri)
        if response.status_code == 200:		# success
            result['ret'] = True
            data = response.json()
            for logEntry in data[u'Members']:
                # I only extract some fields
                entry = {}
                entry['Name']    = logEntry[u'Name']
                entry['Created'] = logEntry[u'Created']
                entry['Message'] = logEntry[u'Message']
                allentries.append(entry)
            result["entries"] = allentries
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        # This looks like: result{allentries[entry{}]}
        return result
    
    def get_lc_logs(self, creds, uri):
        # Lifecycle Controller logs
        result = {}
        allentries = []
        response = self.send_get_request(creds, uri)
        if response.status_code == 200:		# success
            result['ret'] = True
            data = response.json()
            for logEntry in data[u'Members']:
                # I only extract some fields
                entry = {}
                entry['Name']     = logEntry[u'Name']
                entry['Created']  = logEntry[u'Created']
                entry['Message']  = logEntry[u'Message']
                entry['Severity'] = logEntry[u'Severity']
                allentries.append(entry)
            result["entries"] = allentries
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        # This looks like: result{allentries[entry{}]}
        return result
    
    def get_firmware_inventory(self, creds, root_uri, rf_uri):
        result = {}
        devices = []
    
        response = self.send_get_request(creds, root_uri + rf_uri)
        if response.status_code == 200:		# success
            result['ret'] = True
            data = response.json()
            for device in data[u'Members']:
                d = device[u'@odata.id']
                d = d.replace(rf_uri, "")	# leave just device name
                if "Installed" in d:
                    # Get details for each device that is relevant
                    uri = root_uri + rf_uri + d
                    response = self.send_get_request(creds, uri)
                    if response.status_code == 200:	# success
                        data = response.json()
                        result[data[u'Name']] = data[u'Version']
    
        # PropertyValueTypeError
        elif response.status_code == 400:
            result = { 'ret': False, 'msg': 'Not supported on this platform'}
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        return result
    
    # This function compares the firmware levels in the system vs. the firmware levels
    # available in the Catalog.gz file that it downloaded from ftp.dell.com
    def compare_firmware(self, creds, root_uri, rf_uri, catalog_file, model):
        fw = []
        fw_list = {'ret':True, 'Firmwares':[]}
    
        response = self.send_get_request(creds, root_uri + rf_uri)
    
        if response.status_code == 400:
            return { 'ret': False, 'msg': 'Not supported on this platform'}
    
        elif response.status_code == 200:
            data = response.json()
    
            for i in data['Members']:
                if 'Installed' in i['@odata.id']:
                    fw.append(i['@odata.id'])
    
            # read catalog file
            tree = ET.parse(catalog_file)
            root = tree.getroot()
            for inv in fw:
                ver = inv.split('-')[1]
                version = '0'
                path = ""
                for i in root.findall('.//Category/..'):
                            for m in i.findall('.//SupportedDevices/Device'):
                                if m.attrib['componentID'] == ver:
                                    for nx in i.findall('.//SupportedSystems/Brand/Model/Display'):
                                        if nx.text == model:
                                            if LooseVersion(i.attrib['vendorVersion']) > LooseVersion(version):
                                                version = i.attrib['vendorVersion']
                                                path = i.attrib['path']
    
    	    if path != "":
    		fw_list['Firmwares'].append({ 'curr':'%s' % os.path.basename(inv).replace('Installed-%s-'%ver,''), 'latest':'%s' % version, 'path':'%s' % path })
        else:
            fw_list['ret'] = False
        return fw_list
    
    def upload_firmware(self, creds, root_uri, rf_uri, FWPath):
        result = {}
        response = self.send_get_request(creds, root_uri + rf_uri)
    
        if response.status_code == 400:
            return { 'ret': False, 'msg': 'Not supported on this platform'}
    
        elif response.status_code == 200:
            ETag = response.headers['ETag']
    
        else:
            result = { 'ret': False, 'msg': 'Failed to get update service etag %s' % str(root_uri)}
            return result
    
        files = {'file': (os.path.basename(FWPath), open(FWPath, 'rb'), 'multipart/form-data')}
        headers = {"if-match": ETag}
    
        # Calling POST directly rather than use send_post_request() - look into it?
        response = requests.post(root_uri + rf_uri, files=files, auth=(creds['user'], creds['pswd']), headers=headers, verify=False)
        if response.status_code == 201:
            result = { 'ret': True, 'msg': 'Firmare uploaded successfully', 'Version': '%s' % str(response.json()['Version']), 'Location':'%s' % response.headers['Location']}
        else:
            result = { 'ret': False, 'msg': 'Error uploading firmware; status_code=%s' % response.status_code }
        return result
    
    def schedule_firmware_update(self, creds, root_uri, rf_uri, InstallOption):
        fw = []
        response = self.send_get_request(creds, root_uri + rf_uri)
    
        if response.status_code == 200:
            data = response.json()
            for i in data['Members']:
                if 'Available' in i['@odata.id']:
                    fw.append(i['@odata.id'])
        else:
            return { 'ret': False, 'msg': 'Error getting firmware inventory; status_code=%s' % response.status_code }
    
        url = root_uri + '/redfish/v1/UpdateService/Actions/Oem/DellUpdateService.Install'
        payload = {'SoftwareIdentityURIs': fw, 'InstallUpon': InstallOption}
        response = self.send_post_request(creds, url, payload, HEADERS)
    
        if response.status_code == 202:
            result = { 'ret': True, 'msg': 'Firmware install job accepted' }
        else:
            result =  { 'ret': False, 'msg': 'Error accepting firmware install; status_code=%s' % response.status_code }
        return result
    
    def get_idrac_attributes(self, creds, root_uri):
        result = {}
        response = self.send_get_request(creds, root_uri + "/Attributes")
        if response.status_code == 200:             # success
            data = response.json()
            for attribute in data[u'Attributes'].items():
                result[attribute[0]] = attribute[1]
            result['ret'] = True
        # PropertyValueTypeError
        elif response.status_code == 400:
            result = { 'ret': False, 'msg': 'Not supported on this platform'}
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        return result
    
    def get_bios_attributes(self, creds, root_uri):
        result = {}
        response = self.send_get_request(creds, root_uri + "/Bios")
        if response.status_code == 200:		# success
            data = response.json()
            for attribute in data[u'Attributes'].items():
                result[attribute[0]] = attribute[1]
            result['ret'] = True
        # PropertyValueTypeError
        elif response.status_code == 400:
            result = { 'ret': False, 'msg': 'Not supported on this platform' }
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        return result
    
    def get_bios_boot_order(self, creds, root_uri):
        # Get boot mode first as it will determine what attribute to read
        result = {}
        response = self.send_get_request(creds, root_uri + "/Bios")
        if response.status_code == 200:		# success
            result['ret'] = True
            data = response.json()
            boot_mode = data[u'Attributes']["BootMode"]
            response = self.send_get_request(creds, root_uri + "/BootSources")
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
            result = { 'ret': False, 'msg': 'Not supported on this platform' }
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        return result
    
    def get_fan_inventory(self, creds, root_uri):
        result = {}
        fan_details = []
        response = self.send_get_request(creds, root_uri)
        if response.status_code == 200:             # success
            result['ret'] = True
            data = response.json()
    
            for device in data[u'Fans']:
                # There is more information available but this is most important
                fan = {}
                fan['Name']   = device[u'FanName']
                fan['RPMs']   = device[u'Reading']
                fan['State']  = device[u'Status'][u'State']
                fan['Health'] = device[u'Status'][u'Health']
                fan_details.append(fan)
            result["entries"] = fan_details
    
        elif response.status_code == 400:
            result = { 'ret': False, 'msg': 'Not supported on this platform' }
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
    
        return result
    
    def set_bios_default_settings(self, creds, root_uri):
        result = {}
        payload = {}
        response = self.send_post_request(creds, root_uri, payload, HEADERS)
        if response.status_code == 200:		# success
            result = { 'ret': True, 'msg': 'SetBiosDefaultSettings completed'}
        elif response.status_code == 405:
            result = { 'ret': False, 'msg': "Resource not supported" }
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def set_one_time_boot_device(self, creds, bootdevice, root_uri):
        result = {}
        payload = {"Boot": {"BootSourceOverrideTarget": bootdevice}}
        response = self.send_patch_request(creds, root_uri, payload, HEADERS)
        if response.status_code == 200:		# success
            result = { 'ret': True, 'msg': 'SetOneTimeBoot completed'}
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def set_idrac_default_settings(self, creds, root_uri):
        result = {}
        payload = {"ResetType": "All"}
        response = self.send_post_request(creds, root_uri, payload, HEADERS)
        if response.status_code == 200:		# success
            result = { 'ret': True, 'msg': 'SetIdracDefaultSettings completed'}
        elif response.status_code == 405:
            result = { 'ret': False, 'msg': "Resource not supported" }
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def set_idrac_attributes(self, creds, root_uri, idrac_attributes):
        result = {}
        idrac_attributes = idrac_attributes.replace("'","\"")
        payload = {"Attributes": json.loads(idrac_attributes) }
        response = self.send_patch_request(creds, root_uri, payload, HEADERS)
        if response.status_code == 200:
            result = { 'ret': True, 'msg': 'iDRac Attributes set as pending values'}
        elif response.status_code == 405:
            result = { 'ret': False, 'msg': "Resource not supported" }
        else:
            pp = response.json()
            result = { 'ret': False, 'msg': "Error code %s" % str(pp) }
        return result
    
    def set_bios_attributes(self, creds, root_uri, bios_attributes):
        result = {}
        bios_attributes=bios_attributes.replace("'","\"")
        payload = {"Attributes": json.loads(bios_attributes) }
        response = self.send_patch_request(creds, root_uri, payload, HEADERS)
        if response.status_code == 200:
            result = { 'ret': True, 'msg': 'BIOS Attributes set as pending values'}
        elif response.status_code == 400:
            result = { 'ret': False, 'msg': 'Not supported on this platform'}
        elif response.status_code == 405:
            result = { 'ret': False, 'msg': "Resource not supported" }
        else:
            result = { 'ret': False, 'msg': "Error code %s" % str(response.status_code) }
        return result
    
    def create_bios_config_job(self, creds, url):
        payload = {"TargetSettingsURI":"/redfish/v1/Systems/System.Embedded.1/Bios/Settings", "RebootJobType":"PowerCycle"}
        response = self.send_post_request(creds, url, payload, HEADERS)
        if response.status_code == 200:
            result = { 'ret': True, 'msg': 'Config job created'}
        elif response.status_code == 400:
            result = { 'ret': False, 'msg': 'Not supported on this platform'}
        elif response.status_code == 405:
            result = { 'ret': False, 'msg': "Resource not supported" }
        else:
            result = { 'ret': False, 'msg': "Error code %s" % str(response.status_code) }
        return result
    
    def get_cpu_inventory(self, creds, root_uri, rf_uri):
        result = {}
        cpu_details = []
    
        # Get a list of all CPUs and build respective URIs
        cpu_list = []
        response = self.send_get_request(creds, root_uri + rf_uri)
        if response.status_code == 200:		# success
            result['ret'] = True
            data = response.json()
    
            for cpu in data[u'Members']:
                cpu_list.append(cpu[u'@odata.id'])
    
            for c in cpu_list:
                uri = root_uri + c
                response = self.send_get_request(creds, uri)
                if response.status_code == 200:             # success
                    data = response.json()
                    cpu = {}
                    cpu['Name']         = data[u'Id']
                    cpu['Manufacturer'] = data[u'Manufacturer']
                    cpu['Model']        = data[u'Model']
                    cpu['MaxSpeedMHz']  = data[u'MaxSpeedMHz']
                    cpu['TotalCores']   = data[u'TotalCores']
                    cpu['TotalThreads'] = data[u'TotalThreads']
                    cpu['State']        = data[u'Status'][u'State']
                    cpu['Health']       = data[u'Status'][u'Health']
                    cpu_details.append(cpu)
    
                else:
                    result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
                    return result           # no need to go through the whole loop
    
            result["entries"] = cpu_details
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def get_nic_inventory(self, creds, root_uri, rf_uri):
        result = {}
        nic_details = []
    
        # Get a list of all network controllers and build respective URIs
        nic_list = []
        response = self.send_get_request(creds, root_uri + rf_uri)
        if response.status_code == 200:		# success
            result['ret'] = True
            data = response.json()
    
            for nic in data[u'Members']:
                nic_list.append(nic[u'@odata.id'])
    
            for n in nic_list:
                uri = root_uri + n
                response = self.send_get_request(creds, uri)
                if response.status_code == 200:             # success
                    data = response.json()
                    nic = {}
                    nic['Name']  = data[u'Name']
                    nic['FQDN']  = data[u'FQDN']
                    for d in data[u'IPv4Addresses']:
                        nic['IPv4']       = d[u'Address']
                        nic['Gateway']    = d[u'GateWay']
                        nic['SubnetMask'] = d[u'SubnetMask']
                    for d in data[u'IPv6Addresses']:
                        nic['IPv6']   = d[u'Address']
                    for d in data[u'NameServers']:
                        nic['NameServers'] = d
                    nic['MACAddress'] = data[u'PermanentMACAddress']
                    nic['SpeedMbps']  = data[u'SpeedMbps']
                    nic['MTU']        = data[u'MTUSize']
                    nic['AutoNeg']    = data[u'AutoNeg']
                    if 'Status' in data:    # not available when power is off
                        nic['Health'] = data[u'Status'][u'Health']
                        nic['State']  = data[u'Status'][u'State']
                    nic_details.append(nic)
    
                else:
                    result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
                    return result           # no need to go through the whole loop
    
            result["entries"] = nic_details
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def get_psu_inventory(self, creds, root_uri, rf_uri):
        result = {}
        psu_details = []
    
        # Get a list of all PSUs and build respective URIs
        psu_list = []
        response = self.send_get_request(creds, root_uri + rf_uri)
        if response.status_code == 200:		# success
            result['ret'] = True
            data = response.json()
    
            for psu in data[u'Links'][u'PoweredBy']:
                psu_list.append(psu[u'@odata.id'])
    
            for p in psu_list:
                uri = root_uri + p
                response = self.send_get_request(creds, uri)
                if response.status_code == 200:             # success
                    data = response.json()
    
                    psu = {}
                    psu['Name']            = data[u'Name']
                    psu['Model']           = data[u'Model']
                    psu['SerialNumber']    = data[u'SerialNumber']
                    psu['PartNumber']      = data[u'PartNumber']
                    if 'Manufacturer' in data:   # not available in all generations
                        psu['Manufacturer']    = data[u'Manufacturer']
                    psu['FirmwareVersion'] = data[u'FirmwareVersion']
                    psu['PowerCapacityWatts'] = data[u'PowerCapacityWatts']
                    psu['PowerSupplyType'] = data[u'PowerSupplyType']
                    psu['Status']          = data[u'Status'][u'State']
                    psu['Health']          = data[u'Status'][u'Health']
                    psu_details.append(psu)
    
                else:
                    result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
                    return result           # no need to go through the whole loop
    
            result["entries"] = psu_details
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result
    
    def get_system_inventory(self, creds, root_uri):
        result = {}
        response = self.send_get_request(creds, root_uri)
        if response.status_code == 200:		# success
            result['ret'] = True
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
                # Not available in earlier server generations
                result['BootSourceOverrideMode'] = "Not available"
    
            if 'TrustedModules' in data:
                for d in data[u'TrustedModules']:
                    if 'InterfaceType' in d.keys():
                        result['TPMInterfaceType'] = d[u'InterfaceType']
                    result['TPMStatus']        = d[u'Status'][u'State']
            else:
                # Not available in earlier server generations
                result['TPMInterfaceType'] = "Not available"
                result['TPMStatus']        = "Not available"
        else:
            result = { 'ret': False, 'msg': "Error code %s" % response.status_code }
        return result

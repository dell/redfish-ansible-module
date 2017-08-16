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

DOCUMENTATION = '''
---
module: idrac
author: "jose.delarosa@dell.com"
short_description: Manage Dell PowerEdge Servers through iDRAC Redfish APIs
requirements: [ ]
description: Manage Dell PowerEdge servers BIOS, NIC, PERC, iDRAC

options:
    subsystem:
        required: true
        default: None
        choices: [ system, chassis, event, sessions, idrac, jobs, FW ]
        description:
            - sub modules in Redfish Service Root
    cmd:
        required: true
        default: None
        description:
            - sub module command is going to execute 
    idracip:
        required: true
        default: None
        description:
          - iDRAC IP address
    idracuser:
        required: true
        default: root
        description:
          - iDRAC user name
    idracpswd:
        required: true
        default: calvin
        description:
          - iDRAC user password
      
    
'''
ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '0.1'}
import requests
import os
from ansible.module_utils.basic import AnsibleModule
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class iDRAC(object):
    def __init__(self,module):
        self.module=module
        root_uri = ''.join(["https://%s" %module.params['idracip'] , "/redfish/v1"])
        self.system_uri   = root_uri + "/Systems/System.Embedded.1"
        self.chassis_uri  = root_uri + "/Chassis/System.Embedded.1"
        self.manager_uri  = root_uri + "/Managers/iDRAC.Embedded.1"
        self.eventsvc_uri = root_uri + "/EventService"
        self.session_uri  = root_uri + "/Sessions"
        self.tasksvc_uri  = root_uri + "/TaskService"
        self.updatesvc_uri = root_uri + "/UpdateService"
    def send_get_request(self,uri):
        try:
            response = requests.get(uri, verify=False, auth=( self.module.params['idracuser'], self.module.params['idracpswd']))
            systemData = response.json()
        except:
            raise

        return systemData
    
    def get_system_health(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'Status'][u'Health'])
    
    def get_system_serial_number(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'SerialNumber'])
    
    def get_system_service_tag(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'SKU'])
    
    def get_server_part_number(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'PartNumber'])
    
    def get_system_Manufacturer(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'Manufacturer'])
    
    def get_system_bios_version(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'BiosVersion'])
    
    def get_system_type(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'SystemType'])
    
    def get_system_power_state(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'PowerState'])
    
    def get_system_memory_health(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'MemorySummary'][u'Status'][u'Health'])
    
    def get_system_memory_in_GB(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'MemorySummary'][u'TotalSystemMemoryGiB'])
    
    def get_processor_count(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'ProcessorSummary'][u'Count'])
    
    def get_processor_health(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'ProcessorSummary'][u'Status'][u'Health'])
    
    def get_processor_model(self):
        resp = self.send_get_request(self.system_uri)
        return str(resp[u'ProcessorSummary'][u'Model'])
    def get_boot_sources(self):
        sources=[]
        resp = self.send_get_request(self.system_uri+'/BootSources')
        if 'UefiBootSeq' in resp[u'Attributes']:
                for i in resp[u'Attributes']['UefiBootSeq']:
                        sources.append(i['Name'])
        return " ".join(str(x) for x in sources)
        
    def get_system_ethernet_interfaces(self):
        eth=[]
        resp = self.send_get_request(self.system_uri+'/EthernetInterfaces')
        for i in resp[u'Members']:
            eth.append(os.path.basename(i['@odata.id']))
        return " ".join(str(x) for x in eth)

    def get_system_ethernet_permanent_MAC_address(self):
        resp = self.send_get_request(self.system_uri+'/EthernetInterfaces/%s'%self.module.params['eth_interface'])
        return resp[u'PermanentMACAddress']
    def get_system_secure_boot_status(self):
        resp = self.send_get_request(self.system_uri+'/SecureBoot')
        return resp[u'SecureBootCurrentBoot']
    def get_system_secure_boot_certificates(self):
        cert=[]
        resp = self.send_get_request(self.system_uri+'/SecureBoot/Certificates')
        for i in resp[u'Members']:
            cert.append(os.path.basename(i['@odata.id']))
        return " ".join(str(x) for x in cert)

    def get_system_storage_controllers(self):
        ctrls=[]
        resp = self.send_get_request(self.system_uri+'/Storage/Controllers')
        for i in resp[u'Members']:
            ctrls.append(os.path.basename(i['@odata.id']))
        return " ".join(str(x) for x in ctrls)

    def get_system_storage_controller_disks(self):
        disk=[]
        resp = self.send_get_request(self.system_uri+'/Storage/Controllers/%s'%self.module.params['controller'])
        return resp[u'Devices']
    
    def get_firmware_inventory(self):
        fw=dict()
        resp = self.send_get_request(self.updatesvc_uri+'/FirmwareInventory')
        for i in resp[u'Members']:
            fw_info=self.send_get_request(self.updatesvc_uri+'/FirmwareInventory/'+ '%s'%os.path.basename(i['@odata.id']))
            fw[fw_info['Name']]=fw_info['Version']
        return " ".join(str(x) for x in fw)
        

    
def main():
    # Parsing argument file
    module=AnsibleModule(
            argument_spec=dict(
                subsystem = dict(required=True, type='str', default=None),
                idracip = dict(required=True, type='str', default=None),
                idracuser = dict(required=True, type='str', default=None),
                idracpswd = dict(required=True, type='str', default=None),
                cmd = dict(required=True, type='str', default=None),
                
            ),
            supports_check_mode=True
    )
    idrac=iDRAC(module)
    params = module.params
    rc=None
    out=''
    err=''
    result={}

    # Disable insecure-certificate-warning message
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    if not 'subsystem' in params.keys():
        module.fail_json(msg="You haven't specified a subsystem name")
        
    if not 'cmd' in params.keys():
        module.fail_json(msg="You haven't specified a subsystem command")
        
    result['subsystem']=params['subsystem']
    
    if params['subsystem']  == "System":
        if params['cmd'] == 'Health':
            
            out=idrac.get_system_health()
            
        if params['cmd'] == 'SerialNumber':
            out=idrac.get_system_serial_number()
            
        if params['cmd'] == 'ServiceTag':
            out=idrac.get_system_service_tag()
            
        if params['cmd'] == 'AssetTag':
            out=idrac.get_boot_sources()
            
        if params['cmd'] == 'Manufacturer':
            out=idrac.get_system_Manufacturer()
            
        if params['cmd'] == 'BiosVersion':
            out=idrac.get_system_bios_version()
            
        if params['cmd'] == 'SystemType':
            out=idrac.get_system_type()
            
        if params['cmd'] == 'PowerState':
            out=idrac.get_system_power_state()
            
        if params['cmd'] == 'MemoryHealth':
            out=idrac.get_system_memory_health()
            
        if params['cmd'] == 'TotalSystemMemoryGiB':
            out=idrac.get_system_memory_in_GB()
            
        if params['cmd'] == 'ProcessorCount':
            out=idrac.get_processor_count()
            
        if params['cmd'] == 'ProcessorHealth':
            out=idrac.get_processor_health()
            
        if params['cmd'] == 'ProcessorModel':
            out=idrac.get_processor_model()
            
        if params['cmd'] == 'BootSources':
            out=idrac.get_boot_sources()
            
        if params['cmd'] == 'EthernetInterfaces':
            out=idrac.get_system_ethernet_interfaces()
            
        if params['cmd'] == 'PermanentMACAddress':
            out=idrac.get_system_ethernet_permanent_MAC_address()
            
        if params['cmd'] == 'SecureBoot':
            out=idrac.get_system_secure_boot_status()
            
        if params['cmd'] == 'SecureBootCerts':
            out=idrac.get_system_secure_boot_certificates()
            
        if params['cmd'] == 'StorageControllers':
            out=idrac.get_system_storage_controllers()
            
        if params['cmd'] == 'StorageControllerDisks':
            out=idrac.get_system_storage_controller_disks()
            
        if params['cmd'] == 'FirmwareInventory':
            out=idrac.get_firmware_inventory()
            
    if rc is None:
        result['changed']=False
    else:
        result['changed']=True
    if out:
        result['stdout']=out
    if err:
        result['stderr']=err
        
    module.exit_json(**result)

if __name__ == '__main__':
    main()
    
    

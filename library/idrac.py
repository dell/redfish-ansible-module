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
        return resp[u'Status'][u'Health']
    
    def get_system_serial_number(self):
        resp = self.send_get_request(self.system_uri)
        return resp[u'SerialNumber']
    
    def get_system_service_tag(self):
        resp = self.send_get_request(self.system_uri)
        return resp[u'SKU']
    
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
    
    

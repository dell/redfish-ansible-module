#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.

import os
import sys
import shutil

try:
    import ansible
except ImportError:
    print "Error: Ansible is not installed"
    sys.exit(1)

ansible_path = ansible.__path__[0]
redfish_module_path = ansible_path + '/modules/remote_management/redfish'
module_utils_path = ansible_path + '/module_utils/'
redfish_utils_file = module_utils_path + 'redfish_utils.py' 

if os.path.isdir(redfish_module_path): shutil.rmtree(redfish_module_path)
if os.path.isfile(redfish_utils_file): os.remove(redfish_utils_file)
print("Done")

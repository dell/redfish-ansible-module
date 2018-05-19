#!/usr/bin/python
# _*_ coding: utf-8 _*_

# Copyright © 2017-2018 Dell EMC Inc.
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# This script uninstalls the Ansible modules from their default location.

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
redfish_utils_bytecode = module_utils_path + 'redfish_utils.pyc'

if os.path.isdir(redfish_module_path):
    shutil.rmtree(redfish_module_path)
    print("Removing %s" % redfish_module_path)
if os.path.isfile(redfish_utils_file):
    os.remove(redfish_utils_file)
    print("Removing %s" % redfish_utils_file)
if os.path.isfile(redfish_utils_bytecode):
    os.remove(redfish_utils_bytecode)
    print("Removing %s" % redfish_utils_bytecode)
print("Done")

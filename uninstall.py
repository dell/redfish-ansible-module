#! /usr/bin/env python
# _*_ coding: utf-8 _*_

# Copyright © 2017-2018 Jose Delarosa
#
# This script uninstalls the Ansible modules from their default location.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

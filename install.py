#!/usr/bin/env python
# _*_ coding: utf-8 _*_

# Copyright © 2017-2018 Dell Inc.
#
# This script installs the Ansible modules to their default location.
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
green="\033[92m"
end="\033[0m"

try:
    import ansible
except ImportError:
    print ("Error: Ansible is not installed")
    sys.exit(1)

ansible_path = ansible.__path__[0]
remote_management_path = ansible_path + '/modules/remote_management'
redfish_path = remote_management_path + '/redfish'
module_utils_path = ansible_path + '/module_utils/'

def copy_files(src, dest):
    import shutil
    src_files = os.listdir(src)

    for file_name in src_files:
        if file_name.split('.')[-1] == "py":	# only python files
            src_file = os.path.join(src, file_name)
            dst_file = os.path.join(dest, file_name)
            if os.path.isfile(src_file):
                shutil.copy(src_file, dst_file)
                print("- " + src_file + " ---> " + green + dst_file + end)
    return

# Create directory for the main module
if not os.path.isdir(redfish_path): os.makedirs(redfish_path)

# Copy module to ansible module location
copy_files(os.getcwd() + '/library', redfish_path)

# Copy common files to module_util
copy_files(os.getcwd() + '/utils', module_utils_path)

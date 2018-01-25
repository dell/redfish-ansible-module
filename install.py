#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.

import os
import sys

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
                print("- " + src_file + "  ===>  " + dst_file)
    return

# Create directory for the main module
if not os.path.isdir(redfish_path): os.makedirs(redfish_path)

# Copy module to ansible module location
copy_files(os.getcwd() + '/module', redfish_path)

# Copy common files to module_util
copy_files(os.getcwd() + '/utils', module_utils_path)

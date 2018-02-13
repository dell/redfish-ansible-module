# redfish

## Synopsis

* Out-of-band management using Redfish APIs

## Requirements

* python >= 2.6
* ansible >= 2.3
* *requests* python library

## Options

| paramater       | required | default | choices  | comments                  |
|-----------------|----------|---------|----------|-----------------------------------|
| category        | yes      |         | <ul><li>Inventory</li><li>Update</li><li>System</li><li>Chassis</li><li>Manager</li><li>Accounts</li></ul>| Type of action to run |
| command         | yes      |         |          | Command within each category   |
| baseuri         | yes      |         |          | Name/IP addr of OOB controller |
| user            | yes      | root    |          | Login credentials         |
| password        | yes      | calvin  |          | Login credentials         |
| userid          | no       |         |          | For managing users        |
| username        | no       |         |          | For managing users        |
| userpswd        | no       |         |          | For managing users        |
| userrole        | no       |         |          | For managing users        |
| sharehost       | no       |         |          | For managing SCP files    |
| sharename       | no       |         |          | For managing SCP files    |
| shareuser       | no       |         |          | For managing SCP files    |
| sharepswd       | no       |         |          | For managing SCP files    |
| hostname        | no       |         |          | For managing SCP files    |
| scpfile         | no       |         |          | For managing SCP files    |
| bootdevice      | no       |         |          | For setting boot configuration     |
| bios_attr_name  | no       |         |          | Name of BIOS attributes to set     |
| bios_attr_value | no       |         |          | Value of BIOS attributes to set    |
| mgr_attr_name   | no       |         |          | Name of Manager attributes to set  |
| mgr_attr_value  | no       |         |          | Value of Manager attributes to set |
| FWPath          | no       |         |          | Firmware location (for FW upgrade) |
| Model           | no       |         |          | Server model (for FW upgrade) |
| InstallOption   | no       |         | <ul><li>Now</li><li>NowAndReboot</li><li>NextReboot</li></ul>| Action to take after upgrade |

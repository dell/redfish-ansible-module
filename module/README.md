# idrac - manage Dell EMC iDRAC using Redfish APIs

## Synopsis

* Out-of-band management of Dell EMC PowerEdge servers

## Requirements

* python >= 2.6
* ansible >= 2.3

## Options

| paramater       | required | default | choices  | comments                  |
|-----------------|----------|---------|----------|---------------------------|
| category        | yes      |         | <ul><li>Bios</li><li>Firmware</li><li>Idrac</li><li>Inventory</li><li>Logs</li><li>SCP</li><li>Users</li></ul>| Type of action to run         |
| command         | yes      |         |          | Each category has unique commands  |
| idracip         | yes      |         |          |                           |
| idracuser       | yes      | root    |          | User credentials          |
| idracpswd       | yes      | calvin  |          | User credentials          |
| bios_attributes | no       |         |          |                           |
| bootdevice      | no       |         |          |                           |
| sharehost       | no       |         |          | For managing SCP files    |
| sharename       | no       |         |          | For managing SCP files    |
| shareuser       | no       |         |          | For managing SCP files    |
| sharepswd       | no       |         |          | For managing SCP files    |
| hostname        | no       |         |          | For managing SCP files    |
| userid          | no       |         |          | For managing users        |
| username        | no       |         |          | For managing users        |
| userpswd        | no       |         |          | For managing users        |
| userrole        | no       |         |          | For managing users        |

## Examples

The best way to learn how to use these playbooks is by looking at each one in the <i>playbooks</i> directory. Most playbooks can be run as-is, whereas others require that you run specific sections using tags or by commenting out what you don't want.

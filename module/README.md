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

```bash
  tasks:

  - name: Prepare output file
    include: setupoutputfile.yml

  - name: Getting system inventory
    local_action: >
       idrac category=Inventory command=GetInventory idracip={{idracip}}
       idracuser={{idracuser}} idracpswd={{idracpswd}}
    register: result

  - name: Copying results to file
    local_action: copy content={{ result | to_nice_json }}
       dest={{template}}_inventory.json

  - name: Update iDRAC user password
    local_action: >
       idrac category=Users command=UpdateUserPassword idracip={{ idracip }}
       idracuser={{ idracuser }} idracpswd={{ idracpswd }} userid={{ userid }}
       userpswd={{ userpswd }}
    tags: updatepassword

```

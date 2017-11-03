# idrac - manage Dell EMC iDRAC using Redfish APIs

## Synopsis

* Out-of-band management of Dell EMC PowerEdge servers

## Requirements

* python >= 2.6
* ansible >= 2.3

| <ul> <li>Dedicated</li>  <li>LOM1</li>  <li>LOM2</li>  <li>LOM3</li>  <li>LOM4</li> </ul>


## Options

| paramater       | required | default | choices  | comments                  |
|-----------------|----------|---------|----------|---------------------------|
| category        | yes      |         | <ul><li>Bios</li><li>Firmware</li><li>Inventory</li><li>Logs</li></ul>| Type of action to run         |
| command         | yes      |         |          | Each category has unique commands  |
| idracip         | yes      |         |          |                           |
| idracuser       | yes      | root    |          | Credentials                |
| idracpswd       | yes      | calvin  |          | Credentials               |
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
  - name: Getting system inventory
    local_action: >
       idrac category=Inventory command=GetInventory idracip={{idracip}}
       idracuser={{idracuser}} idracpswd={{idracpswd}}
    register: result

  - name: Get Firmware Inventory
    local_action: >
       idrac category=Firmware command=GetInventory idracip={{idracip}}
       idracuser={{idracuser}} idracpswd={{idracpswd}}
    register: result
    ignore_errors: yes

  - name: Get SE Logs
    local_action: >
       idrac category=Logs command=GetSeLogs idracip={{ idracip }}
            idracuser={{ idracuser }} idracpswd={{ idracpswd }}
    register: result
    tags: selog

  - name: Get LC Logs
    local_action: >
       idrac category=Logs command=GetLcLogs idracip={{ idracip }}
            idracuser={{ idracuser }} idracpswd={{ idracpswd }}
    register: result
    tags: lclog

  - name: Get BIOS attributes
    local_action: >
       idrac category=Bios command=GetAttributes idracip={{idracip}}
       idracuser={{idracuser}} idracpswd={{idracpswd}}
    register: result
    ignore_errors: yes
    tags: getattributes


```


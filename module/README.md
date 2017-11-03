# idrac - manage Dell EMC iDRAC using Redfish APIs

## Synopsis

* Out-of-band management of Dell EMC PowerEdge servers

## Requirements

* python >= 2.6
* ansible >= 2.3

## Options

| paramater       | required | default | choices  | comments                  |
|-----------------|----------|---------|----------|---------------------------|
| category        | yes      |         |          |                           |
| command         | yes      |         |          |                           |
| idracip         | yes      |         |          |                           |
| idracuser       | yes      | root    |          |                           |
| idracpswd       | yes      | calvin  |          |                           |
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

```


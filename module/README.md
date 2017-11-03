## idrac - manage Dell EMC iDRAC using Redfish APIs

# Synopsis

* out-of-band management of Dell EMC PowerEdge servers
*

# Requirements

* python >= 2.6
* ansible >= 2.3

# Options

| paramater       | required | default  | choices  | comments                  |
|-----------------|----------|----------|----------|---------------------------|
| category        | yes      |          |          |                           |
| command         | yes      |          |          |                           |
| idracip         | yes      |          |          |                           |
| idracuser       | yes      |          |          |                           |
| idracpswd       | yes      |          |          |                           |
| bios_attributes | no       |          |          |                           |
| bootdevice      | no       |          |          |                           |
| sharehost       | no       |          |          | For managing SCP files    |
| sharename       | no       |          |          | For managing SCP files    |
| shareuser       | no       |          |          | For managing SCP files    |
| sharepswd       | no       |          |          | For managing SCP files    |
| hostname        | no       |          |          | For managing SCP files    |
| userid          | no       |          |          | For managing users        |
| username        | no       |          |          | For managing users        |
| userpswd        | no       |          |          | For managing users        |
| userrole        | no       |          |          | For managing users        |

# Examples

The best way to learn how to use these playbooks is by looking at each one. Most playbooks can be run as-is, whereas others require that you run specific sections using tags or by commenting out what you don't want.

## Get system inventory

```bash
$ ansible-playbook get_system_inventory.yml
```

Sample:

```bash
  - name: Getting system inventory
    local_action: >
       idrac category=Inventory command=GetInventory idracip={{idracip}}
       idracuser={{idracuser}} idracpswd={{idracpswd}}
    register: result

  - name: Copying results to file
    local_action: copy content={{ result | to_nice_json }}
       dest={{template}}_inventory.json
```

## Get firmware inventory

```bash
$ ansible-playbook get_firmware_inventory.yml
```

```bash
  - name: Get Firmware Inventory
    local_action: >
       idrac category=Firmware command=GetInventory idracip={{idracip}}
       idracuser={{idracuser}} idracpswd={{idracpswd}}
    register: result
    ignore_errors: yes

  - name: Copy inventory to file
    local_action: copy content={{ result | to_nice_json }}
       dest={{template}}_firmware_inventory.json

```

## Get system logs

```bash
$ ansible-playbook get_system_logs.yml
```

```bash
  # ------------------------------------------------------------------------
  - name: Get SE Logs
    local_action: >
       idrac category=Logs command=GetSeLogs idracip={{ idracip }}
            idracuser={{ idracuser }} idracpswd={{ idracpswd }}
    register: result
    tags: selog

  - name: Place SE Logs in file
    local_action: copy content={{ result | to_nice_json }}
             dest={{template}}_SELog.json
    tags: selog

  # ------------------------------------------------------------------------
  - name: Get LC Logs
    local_action: >
       idrac category=Logs command=GetLcLogs idracip={{ idracip }}
            idracuser={{ idracuser }} idracpswd={{ idracpswd }}
    register: result
    tags: lclog

  - name: Place LC Logs in file
    local_action: copy content={{ result | to_nice_json }}
             dest={{template}}_LCLog.json
    tags: lclog
```

More coming soon

# Ansible modules for Dell EMC PowerEdge iDRAC (using Redfish APIs)

Ansible modules and playbooks that use the Redfish API to manage PowerEdge servers via the integrated Dell Remote Access Controller (iDRAC).

## Why Ansible

Ansible is an open source automation engine that automates complex IT tasks such as cloud provisioning, application deployment and a wide variety of IT tasks. It is a one-to-many agentless mechanism where complicated deployment tasks can be controlled and monitored from a central control machine.

To learn more about Ansible, click [here](http://docs.ansible.com/).

## Why Redfish

Redfish is an open industry-standard specification and schema designed for modern and secure management of platform hardware. On PowerEdge servers the Redfish management APIs are available via the iDRAC, which can be used by IT administrators to easily monitor and manage at scale their entire infrastructure using a wide array of clients on devices such as laptops, tablets and smart phones. 

To learn more about Redfish, click [here](https://www.dmtf.org/standards/redfish).

To learn more about the Redfish APIs available in the PowerEdge iDRAC, click [here](http://en.community.dell.com/techcenter/extras/m/white_papers/20443207).

## Ansible and Redfish together

Together, Ansible and Redfish can be used by system administrators to fully automate at large scale server monitoring, alerting, configuration and firmware update tasks from one central location, significantly reducing complexity and helping improve the productivity and efficiency of IT administrators.

## How it works

A client talks to iDRAC via its IP address by sending Redfish URIs that the iDRAC will then process and send information back.

Your */etc/ansible/hosts* should look like this:

```
[myhosts]
# Hostname        iDRAC IP               Host alias
host1.domain.com  idracip=192.168.0.101  host=webserver1
host2.domain.com  idracip=192.168.0.102  host=webserver2
host3.domain.com  idracip=192.168.0.103  host=dbserver1
...
```

## Modules

  - idrac_logs: Collect System Event and Lifecycle Controller Logs
  - idrac_scp: Manages [Server Configuration Profile](http://en.community.dell.com/techcenter/extras/m/white_papers/20269601) files.
  - idrac_sysinfo: Collects System Information (Health, CPUs, RAM, etc.)
  - idrac_users (coming soon): Manages iDRAC users (add/delete/update)
  - idrac_power (coming soon): Manages system power (status/on/off)
  - idrac_raid (coming soon): Manages PERC RAID configuration
  - idrac_config (coming soon): Manages iDRAC configuration
  - idrac_license (coming soon): Manages iDRAC licenses
  - idrac_provision (coming soon): Manages OS provisioning
  - idrac_fw (coming soon): Manages Firmware updates

## Example

Clone this repository. The idrac modules are in the *library* directory, they can be left there or placed somewhere else. If you move them, be sure to define the ANSIBLE_LIBRARY environment variable.

```bash
$ export ANSIBLE_LIBRARY=<directory-with-modules>

$ ansible-playbook idrac_sysinfo.yml
  ...
PLAY [PowerEdge iDRAC] *********************************************************

TASK [Set timestamp variable] **************************************************
ok: [webserver1]
ok: [webserver2]
ok: [dbserver1]
  --- snip ---
```

You will see the usual task execution output, but please note that all server information retrieved is collected and put into text files defined by the *rootdir* variable in the playbook. The playbook creates a directory per server and places files there. For example:

```bash
$ cd <rootdir>/webserver1
$ ls
webserver1_sysinfo_20170728_142202.info
$ cat webserver1_sysinfo_20170728_142202.info
Health: OK
Model: PowerEdge M620
BiosVersion: 2.5.4
AssetTag:
Memory: 64
CPU: Intel(R) Xeon(R) CPU E5-2620 0 @ 2.00GHz
ConsumedWatts: 71
PowerState: On
```

These files are in the format *{{host}}_{{datatype}}_{{datestamp}}* and each contains valuable server information. 

All server data is returned in JSON format and where appropriate it is extracted into an easy-to-read format. In this case, the file *webserver1_sysinfo_20170728_142202.txt* contains server data that has already been parsed for consumption.

With the idrac_logs module, the SELogs file is in JSON format but its relevant data can be easily read with any JSON parser. For example, using the [jq](https://stedolan.github.io/jq/) parser:

```
$ jq '.result.Members[] | {Date: .Created, Message: .Message}' webserver1_SELogs_20170615_132201.json
{
  "Date": "2017-05-22T19:12:57-05:00",
  "Message": "The system halted because system power exceeds capacity."
}
{
  "Date": "2017-01-05T18:50:43-06:00",
  "Message": "The process of installing an operating system or hypervisor is successfully completed."
}
  --- snip ---

```

## Prerequisites

  - PowerEdge 12G/13G servers only (not tested in 14G yet, but should work)
  - Minimum iDRAC 7/8 FW 2.40.40.40
  - SMB share to place SCP files
  - [jq](https://stedolan.github.io/jq/) JSON parser

## Contributors

  - jose_delarosa@dell.com
  - bhavesh_bharadiya@dell.com

## Limitations and Disclaimers

  - These Ansible modules are for demonstration purposes only (for now).

## Support

Please note this code is provided as-is and currently not supported by Dell EMC.

## Report problems or provide feedback

If you run into any problems or would like to provide feedback, please open an issue [here](https://github.com/dell/idrac-ansible-module/issues).

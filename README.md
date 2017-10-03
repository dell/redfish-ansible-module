# Ansible module for Dell EMC PowerEdge iDRAC using Redfish APIs

Ansible module and playbooks that use the Redfish API to manage PowerEdge servers via the integrated Dell Remote Access Controller (iDRAC). For more details, see these [slides](https://www.slideshare.net/JoseDeLaRosa7/s111013-delarosa).

## Why Ansible

Ansible is an open source automation engine that automates complex IT tasks such as cloud provisioning, application deployment and a wide variety of IT tasks. It is a one-to-many agentless mechanism where complicated deployment tasks can be controlled and monitored from a central control machine.

To learn more about Ansible, click [here](http://docs.ansible.com/).

## Why Redfish

Redfish is an open industry-standard specification and schema designed for modern and secure management of platform hardware. On PowerEdge servers the Redfish management APIs are available via the iDRAC, which can be used by IT administrators to easily monitor and manage at scale their entire infrastructure using a wide array of clients on devices such as laptops, tablets and smart phones. 

To learn more about Redfish, click [here](https://www.dmtf.org/standards/redfish).

To learn more about the Redfish APIs available in iDRAC, click [here](http://topics-cdn.dell.com/pdf/iDRAC9-lifecycle-controller-v3.00.00.00_API%20Guide_en-us.pdf).

## Ansible and Redfish together

Together, Ansible and Redfish can be used by system administrators to fully automate at large scale server monitoring, alerting, configuration and firmware update tasks from one central location, significantly reducing complexity and helping improve the productivity and efficiency of IT administrators.

## How it works

A client talks to iDRAC via its IP address by sending Redfish URIs that the iDRAC will then process and send information back.

![alt text](http://linux.dell.com/images/ansible-redfish-overview.png)

Your */etc/ansible/hosts* should look like this:

```
[myhosts]
# Hostname        iDRAC IP               Host alias
host1.domain.com  idracip=192.168.0.101  host=webserver1
host2.domain.com  idracip=192.168.0.102  host=webserver2
host3.domain.com  idracip=192.168.0.103  host=dbserver1
...
```

## Categories

  - Inventory: Collects System Information (Health, CPUs, RAM, etc.)
  - Logs: Collect System Event and Lifecycle Controller Logs
  - Power: Manages system power (status/on/off/restart)
  - Storage: Manages storage controllers, HDDs and VDs
  - Bios: Manages BIOS settings
  - SCP: Manages [Server Configuration Profile](http://en.community.dell.com/techcenter/extras/m/white_papers/20269601) files.
  - Users: Manages iDRAC users (add/delete/update)
  - IdracSettings (coming soon): Manages iDRAC settings (network, time, etc.)
  - Firmware (coming soon): Manages system firmware

Note: Some of these categories might be combined later on (Users and IdracSettings, for example), but for the sake of simplicity they are listed separately for now.

## Requirements

  - PowerEdge 12G/13G/14G servers
  - Minimum iDRAC 7/8/9 FW 2.40.40.40
  - SMB share to place SCP files

## Example

Clone this repository. The idrac module is in the *library* directory, it can be left there or placed somewhere else. If you move it, be sure to define the ANSIBLE_LIBRARY environment variable.

```bash
$ export ANSIBLE_LIBRARY=<directory-with-module>

$ ansible-playbook system-inventory.yml
  ...
PLAY [PowerEdge iDRAC Get System Inventory] ************************************

TASK [Define timestamp] ********************************************************
ok: [webserver1]
ok: [webserver2]
ok: [dbserver1]
  --- snip ---
```

You will see the usual task execution output. Playbooks that collect system information will place it in files in JSON format in a directory defined by the *rootdir* variable in file *group_vars/myhosts*. The playbook creates a directory for each server and places files there. For example:

```bash
$ cd <rootdir>/webserver1
$ ls
webserver1_20170912_104953_inventory.json
webserver1_20170912_103733_storagecontrollers.json
$ cat webserver1_20170912_104953_inventory.json
{
    "changed": false,
    "result": {
        "AssetTag": "",
        "BiosVersion": "2.4.3",
        "BootSourceOverrideMode": "14G only.",
        "CpuCount": 2,
        "CpuHealth": "OK",
        "CpuModel": "Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz",
        "HostName": "webserver1.lab.dell.com",
        "Manufacturer": "Dell Inc.",
        "MemoryHealth": "OK",
        "MemoryTotal": 128.0,
        "Model": "PowerEdge R630",
        "PartNumber": "0CNCJWA00",
        "PowerState": "On",
        "SerialNumber": "CN74YYYYYXXXXX",
        "ServiceTag": "XXXYYYY",
        "Status": "OK",
        "SystemType": "Physical"
    }
}
$ cat webserver1_20170912_103733_storagecontrollers.json
{
    "changed": false,
    "result": [
        {
            "Health": "OK",
            "Name": "PERC H330 Mini"
        },
        {
            "Health": "OK",
            "Name": "PCIe Extender 1"
        },
        {
            "Health": null,
            "Name": "C610/X99 series chipset sSATA Controller [AHCI mode]"
        },
        {
            "Health": null,
            "Name": "C610/X99 series chipset 6-Port SATA Controller [AHCI mode]"
        }
    ]
}
```

These files are in the format *{{host}}_{timestamp}}_{{datatype}}* and each contains valuable server information. 

We will be providing scripts to easily parse through these JSON files and consolidate all server information in easy-to-read formats, including in CSV format for easy import into spreadsheets.

## Parsing through JSON files

All data collected from servers is returned in JSON format. Any JSON parser can then be used to extract the specific data you are looking for, which can come in handy since in some cases the amount of data collected can be more than you need.

I found the [jq](https://stedolan.github.io/jq/) parser to be easy to install and use, here are some examples using the output files above:

```bash
$ jq .result.BiosVersion webserver1_20170912_104953_inventory.json 
"2.4.3"

$ jq '.result | {Manufacturer: .Manufacturer, Name: .Model}' webserver1_20170912_104953_inventory.json
{
  "Manufacturer": "Dell Inc.",
  "Name": "PowerEdge R630"
}

$ jq '.result[] | .Health' webserver1_20170912_103733_storagecontrollers.json 
"OK"
"OK"
null
null
```

It should be straight-forward to extract the same data from hundreds of files using shell scripts and organize it accordingly. In the near future scripts will be made available to facilitate data orgnization. For additional help with qt, refer to this [manual](https://shapeshed.com/jq-json/). 

## Support

Please note this code is provided as-is and not supported by Dell EMC.

## Report problems or provide feedback

If you run into any problems or would like to provide feedback, please open an issue [here](https://github.com/dell/idrac-ansible-module/issues).

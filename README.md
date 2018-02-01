# Ansible module for Dell EMC PowerEdge iDRAC using Redfish APIs

Ansible module and playbooks that use the Redfish API to manage PowerEdge servers via the integrated Dell Remote Access Controller (iDRAC). For more details, see these [slides](https://www.slideshare.net/JoseDeLaRosa7/automated-outofband-management-with-ansible-and-redfish).

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

A client talks to Dell EMC servers via its iDRAC by sending Redfish URIs. The Redfish APIs will then either 1) perform an action (ex: upgrade firmware, reboot server) or 2) send information back (ex: system inventory, power consumption). Ansible provides automation so that this process can be scaled up to thousands of servers.

![alt text](http://linux.dell.com/images/ansible-redfish-overview.png)

## Categories

  - Inventory: Collects system inventory
  - Firmware: Manages system firmware
  - Bios: Manages BIOS settings
  - Power: Manages system power
  - Storage: Manages storage controllers
  - Users: Manages iDRAC users
  - SCP: Manages [Server Configuration Profiles](http://en.community.dell.com/techcenter/extras/m/white_papers/20269601).
  - Logs: Collect System Event (SE) and Lifecycle Controller (LC) logs
  - Idrac: Manages iDRAC settings

For more details on what options are available in each category, refer to this [README](https://github.com/dell/idrac-ansible-module/tree/master/playbooks).

## Requirements

  - PowerEdge 12G/13G/14G servers (some features only available in 14G)
  - Minimum iDRAC 7/8/9 FW 2.40.40.40

## Installation

Clone this repository:
```
$ git clone https://github.com/dell/idrac-ansible-module
```
Install Ansible + required Python libraries (make sure you have the proper repositories available):
```
pip install requirements.txt
```
Copy module to default system location:
```
$ python install.py
```

## Examples

The file */etc/ansible/hosts* should look like this:

```
[myhosts]
# hostname     OOB controller IP/NAME
webserver1     baseuri=192.168.0.101
webserver2     baseuri=192.168.0.102
dbserver1      baseuri=192.168.0.103
...
```

The OOB controller (i.e. BMC, iDRAC, iLo) IP is necessary as this is how we communicate with the host. We are not connecting to the host OS via ssh, but to the OOB controller via https, so be sure this information is correct. Please note that *baseuri* can also be a DNS-resolvable name.

The playbook names are self-explanatory, and they are the best source to learn how to use them. Every Redfish API supported by the Ansible module is included in the playbooks. If it's not in a playbook, a Redfish API has not been coded into the module yet.

```bash

$ cd playbooks
$ ansible-playbook get_system_inventory.yml
  ...
PLAY [Get System Inventory] ****************************************************

TASK [Define timestamp] ********************************************************
ok: [webserver1]
ok: [webserver2]
ok: [dbserver1]
  --- snip ---
```

Playbooks that collect system information will place it in files in JSON format in a directory defined by the *rootdir* variable in file *group_vars/myhosts*. The playbook creates a directory for each server and places files there. For example:

```bash
$ cd <rootdir>/webserver1
$ ls
webserver1_SystemInventory_20170912_104953.json
webserver1_StorageControllerInventory_20170912_103733.json
$ cat webserver1_SystemInventory_20170912_104953.json
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
$ cat webserver1_StorageControllerInventory_20170912_103733.json
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

These files are in the format *<host>_<timestamp>_<datatype>* and each contains valuable server inventory.

Some Redfish APIs are only available in 14G PowerEdge servers. In addition, availability of Redfish APIs varies in 13G and 12G servers (though we are working to make them uniform across all supported servers). If you run a task for a Redfish API that is not available in a server, you will see an error displayed during playbook execution:

```
TASK [Get Firmware Inventory] *********************************************************************
fatal: [r630 -> localhost]: FAILED! => {"changed": false, "failed": true, "msg": "14G only"}
...ignoring
ok: [r740-1 -> localhost]
```

## Parsing through JSON files

All data collected from servers is returned in JSON format. Any JSON parser can then be used to extract the specific data you are looking for, which can come in handy since in some cases the amount of data collected can be more than you need.

The [jq](https://stedolan.github.io/jq/) parser to be easy to install and use, here are some examples using the output files above:

```bash
$ jq .result.BiosVersion webserver1_SystemInventory_20170912_104953.json
"2.4.3"

$ jq '.result | {Manufacturer: .Manufacturer, Name: .Model}' webserver1_SystemInventory_20170912_104953.json
{
  "Manufacturer": "Dell Inc.",
  "Name": "PowerEdge R630"
}

$ jq '.result[] | .Health' webserver1_StorageControllerInventory_20170912_103733.json
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

# Ansible module for Dell EMC PowerEdge iDRAC (using Redfish APIs)

Ansible module and playbook that use the Redfish API to manage PowerEdge servers via the integrated Dell Remote Access Controller (iDRAC).

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
# Hostname iDRAC IP               Host alias
server1    idracip=192.168.0.101  host=web_server1
server2    idracip=192.168.0.102  host=web_server2
server3    idracip=192.168.0.103  host=db_server
...
```

## Example

Clone this repository. The idrac module is in the *library* directory, it can be left there or it can be placed somewhere else. If you move it, be sure to define the ANSIBLE_LIBRARY environment variable.

```bash
$ export ANSIBLE_LIBRARY=<directory-with-modules>

$ ansible-playbook idrac.yml
  ...
  TASK [report information] ******************************************************
ok: [t630] => {
  --- snip ---
            }, 
            "Manufacturer": "Dell Inc.", 
            "MemorySummary": {
                "Status": {
                    "Health": "OK", 
                    "HealthRollUp": "OK", 
                    "State": "Enabled"
                }, 
                "TotalSystemMemoryGiB": 64.0
            }, 
            "Model": "PowerEdge T630", 
            "Name": "System", 
            "PartNumber": "", 
            "PowerState": "On", 
            "ProcessorSummary": {
                "Count": 2, 
                "Model": "Intel(R) Xeon(R) CPU E5-2640 v3 @ 2.60GHz", 
                "Status": {
                    "Health": "OK", 
                    "HealthRollUp": "OK", 
                    "State": "Enabled"
                }
            }, 
  --- snip ---
```

## Limitations and Disclaimers

  - This module is for testing and demonstration purposes only.
  - Only a few GET requests are available. Support for POST, PATCH and DELETE requests coming soon.
  - For demonstration purposes, the playbook redirects stdout to text files in JSON format. Ideally, they should be stored in a database or be formatted for easy import into a spreadsheet or audit tool.

## Support

Please note this code is provided as-is and currently not supported by Dell EMC.

## Report problems or provide feedback

If you run into any problems or would like to provide feedback, please open an issue [here](https://github.com/dell/idrac-ansible-module/issues).

# Ansible playbooks and roles for iDRACs using Redfish APIs 

This repository contains the Ansible playbook samples and Ansible roles for automating the PowerEdge server lifecycle management using iDRACs and OpenManage Enterprise. The examples highlight the capabilities of the modules and their ability to be integrated into more complex playbooks, workflows, and applications.

These [playbooks](playbooks) should give you a very good idea of how to create your own playbooks for your own needs.

Here is a sample [inventory](inventory.yml) file.

Example playbooks and roles use the following collection and modules:

- [dellemc.openmanage](https://galaxy.ansible.com/dellemc/openmanage) collection: This collection is officially supported by DellEMC. For more information, please visit the [GitHub repository](https://github.com/dell/dellemc-openmanage-ansible-modules)
- [community.general](https://galaxy.ansible.com/community/general) collection - Following is the list of the modules that are being used from this collection:
    - [redfish_info](https://docs.ansible.com/ansible/latest/collections/community/general/redfish_info_module.html)
    - [redfish_command](https://docs.ansible.com/ansible/latest/collections/community/general/redfish_command_module.html)
    - [redfish_config](https://docs.ansible.com/ansible/latest/collections/community/general/redfish_config_module.html)
    - [idrac_redfish_info](https://docs.ansible.com/ansible/latest/collections/community/general/idrac_redfish_info_module.html)
    - [idrac_redfish_command](https://docs.ansible.com/ansible/latest/collections/community/general/idrac_redfish_command_module.html)
    - [idrac_redfish_config](https://docs.ansible.com/ansible/latest/collections/community/general/idrac_redfish_config_module.html)

## Requirements

### Ansible
* These example playbooks and roles have been developed and tested with [maintained](https://docs.ansible.com/ansible/devel/reference_appendices/release_and_maintenance.html) version of Ansible core (>= ```2.11```)
* When using ansible-core, you will also need to install the following collections:
    ```yaml
    ---
    collections:
      - name: community.general
        version: 3.7.0
      - name: dellemc.openmanage
        version: 4.1.0
    ```
    **Note:** You can alternatively install the Ansible community distribution ```(pip install ansible)```  if you don't want to manage individual collections.
* Instructions on how to install Ansible can be found in the [Ansible website](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

### Jinja2

* This role uses Jinja2 templates. Ansible core installs Jinja2 by default, but depending on your install and/or upgrade path, you might be running an outdated version of Jinja2. The minimum version of Jinja2 required for the role to properly function is `2.11`.
* Instructions on how to install Jinja2 can be found in the [Jinja2 website](https://jinja.palletsprojects.com/en/2.11.x/intro/#installation).


## Installation

### Git
Use ```git clone https://github.com/dell/redfish-ansible-module.git``` to pull the latest commit of the playbooks and role from GitHub

## Documentation
Each Ansible role contains a README with instructions on prerequisites, installation, and usage. Be sure to also review supported resource versions and follow installation instructions for the underlying modules used in the examples per their documentation.

## Support
The examples are provided as is with no warranties. Some basic knowledge of the Red Hat Ansible Automation Platform and additional technology integration is expected. 

If you run into any problems or would like to provide feedback, please open an issue [here](https://github.com/dell/redfish-ansible-module/issues)

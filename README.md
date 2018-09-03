# Ansible module for Out-Of-Band (OOB) controllers using Redfish APIs

This project is now part of the Ansible repository:

- [ansible_facts](https://docs.ansible.com/ansible/devel/modules/redfish_facts_module)
- [ansible_command](https://docs.ansible.com/ansible/devel/modules/redfish_command_module)
- [ansible_config](https://docs.ansible.com/ansible/devel/modules/redfish_config_module)

To use them, clone the Ansible repository and follow the examples:

```
$ git clone https://github.com/ansible/ansible.git
```

## Older development work

I have left 2 development branches in this repository. These are no longer maintained but I am leaving here (for now) for reference ONLY:

- [fordell](https://github.com/dell/idrac-ansible-module/tree/fordell) - Original master branch specific to Dell PowerEdge servers. Please note that I have not updated this branch in quite some time and the code base is quite old.

- [old_master](https://github.com/dell/idrac-ansible-module/tree/old_master) - Module was updated to be vendor agnostic. Code here is also quite outdated.

## Sample playbooks coming soon

Though there should be enough documentation available upstream to create your own playbooks, I will dump here as many sample playbooks as possible to get you started quickly.

## Report problems or provide feedback

If you run into any problems or would like to provide feedback, please open an issue [here](https://github.com/ansible/ansible/issues).

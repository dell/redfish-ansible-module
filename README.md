# Ansible module for Out-Of-Band (OOB) controllers using Redfish APIs

This project is now part of the upstream Ansible repository:

- [ansible_facts](https://docs.ansible.com/ansible/devel/modules/redfish_facts_module)
- [ansible_command](https://docs.ansible.com/ansible/devel/modules/redfish_command_module)
- [ansible_config](https://docs.ansible.com/ansible/devel/modules/redfish_config_module)

To use them, clone the Ansible repository and follow the examples:

```
$ git clone https://github.com/ansible/ansible.git
```

## Sample playbooks

These [playbooks](playbooks) should give you a very good idea of how to create your own playbooks for your own needs.

## Old development work

I left 2 development branches in this repository. They are no longer maintained and are for reference ONLY:

- [fordell](https://github.com/dell/idrac-ansible-module/tree/fordell) - Original module specific to Dell servers. I have not updated this branch in quite some time and the code base is quite old.

- [old_master](https://github.com/dell/idrac-ansible-module/tree/old_master) - Module was updated to be vendor agnostic. Code here is also quite outdated.

## Report problems or provide feedback

If you run into any problems or would like to provide feedback, please open an issue [here](https://github.com/ansible/ansible/issues).

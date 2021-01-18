idrac_facts
=========

Role to get iDRAC facts.

Requirements
------------

- ansible >= 2.9
- iDRAC 7/8 firmware >= 2.50.50.50
- iDRAC 9 firmware >= 3.00.00.00

Role Variables
--------------

None

Dependencies
------------

None

Example Playbook
----------------

```
    - hosts: servers
      connection: local
      gather_facts: no

      roles:
        - role: idrac_facts
          vars:
            idrac_ip: "{{ inventory_hostname }}"
            idrac_user: "{{ idrac_user }}"
            idrac_password: "{{ idrac_password }}"
          tags:
            - always

      tasks:
        - name: get idrac firmware version
          ansible.builtin.debug:
            msg: "{{ idrac_firmware_version }}"
```

License
-------

Apache 2.0

Author Information
------------------

Anupam Aloke ([@anupamaloke](https://github.com/anupamaloke))
Dell Technologies &copy;2021

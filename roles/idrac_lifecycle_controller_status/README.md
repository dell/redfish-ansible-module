idrac_lifecyle_controller_status
=========

Role to get the Lifecycle Controller status using iDRACs for Dell EMC PowerEdge servers.

Requirements
------------

- ansible >= 2.9
- iDRAC 7/8 firmware >= 2.50.50.50
- iDRAC 9 firmware >= 3.00.00.00

Role Variables
--------------

| Parameter | Required | Type | Choices/Default | Example | Description |
|-----------|----------|------|-----------------|---------|-------------|
| idrac_ip  | yes | str | None | "192.168.10.10"<br/>"abc.xyz.com" | IP address or hostname of iDRAC |
| idrac_user | yes | str | None | "admin" | iDRAC user with privileges to import the server configuration profile |
| idrac_password | yes | str | None | "Passw0rd" | iDRAC user password |
| idrac_https_port | no | int | 443 | 443 | iDRAC web server https port |

Dependencies
------------

None

Example Playbook
----------------

```
- name: Get lifecycle controller status
  include_role:
    name: idrac_lifecycle_controller_status
  vars:
    idrac_ip: "{{ inventory_hostname }}"
    idrac_user: "{{ idrac_user }}"
    idrac_password: "{{ idrac_password }}"

- ansible.builtin.debug:
    msg: "{{ idrac_lc_status }}"
```

Author Information
------------------

Anupam Aloke ([@anupamaloke](https://github.com/anupamaloke))
Dell Technologies &copy;2021

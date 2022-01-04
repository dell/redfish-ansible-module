ome_quick_deploy
=========

Role to configure the Quick Deploy settings for a chassis device. The Quick Deploy feature enables you to configure the password to access iDRAC user interface, IOMs, and IPv4 and IPv6 settings.

Requirements
------------

- Ansible >= 2.11
- OpenManage Enterprise-Modular >= 1.30.00

Role Variables
--------------

| Parameter | Required | Type | Choices/Default | Example | Description |
|-----------|----------|------|-----------------|---------|-------------|
| ome_hostname | yes | str | None | "192.168.10.10"<br>"ome.example.com" | OME-Modular IP address or hostname |
| ome_username | yes | str | None | "admin" | OME user name |
| ome_password | yes | str | None | "Passw0rd" | OME user password |
| device_id | no | int | None | 12345 | Device ID of the target chassis |
| device_service_tag | no | str | None | "123ABCD" | Service Tag of the target chassis |
| quick_deploy_options | no | dict | None | { "password": "Passw0rd", "ipv4_enabled": True, "ipv4_network_type": "Static", "ipv4_subnet_mask": "255.255.255.0", "ipv4_gateway": "192.168.10.1", "slots":  [ {"slot_id": 1, "slot_ipv4_address": "192.168.10.11", "vlan_id": 1}, {"slot_id": 2, "slot_ipv4_address": "192.168.10.12", "vlan_id": 1} ]} | Quick deploy option settings |

Dependencies
------------

- dellemc.openmanage

Example Playbook
----------------

- Configure Static IPv4 settings for a lead chassis or a standalone chassis

```
  tasks:
  - name: configure quick deploy
    include_role:
      name: ome_quick_deploy
    vars:
      ome_hostname: "{{ inventory_hostname }}"
      ome_username: "{{ user }}"
      ome_password: "{{ password }}"
      quick_deploy_options:
        ipv4_enabled: True
        ipv4_network_type: "Static"
        ipv4_subnet_mask: "255.255.255.0"
        ipv4_gateway: "192.168.10.1"
        password: "calvin"
        slots:
          - slot_id: 1
            slot_ipv4_address: "192.168.10.11"
            vlan_id: 1
          - slot_id: 2
            slot_ipv4_address: "192.168.10.12"
            vlan_id: 1
```

- Configure Static IPv4 settings for a member chassis (identified by device ID) using a lead chassis

```
  tasks:
  - name: configure quick deploy
    include_role:
      name: ome_quick_deploy
    vars:
      ome_hostname: "{{ inventory_hostname }}"
      ome_username: "{{ user }}"
      ome_password: "{{ password }}"
      device_id: 12345
      quick_deploy_options:
        ipv4_enabled: True
        ipv4_network_type: "Static"
        ipv4_subnet_mask: "255.255.255.0"
        ipv4_gateway: "192.168.10.1"
        password: "calvin"
        slots:
          - slot_id: 1
            slot_ipv4_address: "192.168.10.11"
            vlan_id: 1
          - slot_id: 2
            slot_ipv4_address: "192.168.10.12"
            vlan_id: 1
```

- Configure Static IPv4 settings for a member chassis (identified by device servicetag) using a lead chassis

```
  tasks:
  - name: configure quick deploy
    include_role:
      name: ome_quick_deploy
    vars:
      ome_hostname: "{{ inventory_hostname }}"
      ome_username: "{{ user }}"
      ome_password: "{{ password }}"
      device_service_tag: "ABC1234"
      quick_deploy_options:
        ipv4_enabled: True
        ipv4_network_type: "Static"
        ipv4_subnet_mask: "255.255.255.0"
        ipv4_gateway: "192.168.10.1"
        password: "calvin"
        slots:
          - slot_id: 1
            slot_ipv4_address: "192.168.10.11"
            vlan_id: 1
          - slot_id: 2
            slot_ipv4_address: "192.168.10.12"
            vlan_id: 1
```

- Configure DHCP IPv4 settings for a lead chassis or standalone chassis

```
  tasks:
  - name: configure quick deploy
    include_role:
      name: ome_quick_deploy
    vars:
      ome_hostname: "{{ inventory_hostname }}"
      ome_username: "{{ user }}"
      ome_password: "{{ password }}"
      quick_deploy_options:
        ipv4_enabled: True
        ipv4_network_type: "DHCP"
        password: "calvin"
        slots:
          - slot_id: 1
            vlan_id: 1
          - slot_id: 2
            vlan_id: 1
```

- Configure DHCP IPv4 settings for a member chassis (identified using a device ID) using a lead chassis

```
  tasks:
  - name: configure quick deploy
    include_role:
      name: ome_quick_deploy
    vars:
      ome_hostname: "{{ inventory_hostname }}"
      ome_username: "{{ user }}"
      ome_password: "{{ password }}"
      device_id: 12345
      quick_deploy_options:
        ipv4_enabled: True
        ipv4_network_type: "DHCP"
        password: "calvin"
        slots:
          - slot_id: 1
            vlan_id: 1
          - slot_id: 2
            vlan_id: 1
```

- Configure DHCP IPv4 settings for a member chassis (identified using a device servicetag) using a lead chassis

```
  tasks:
  - name: configure quick deploy
    include_role:
      name: ome_quick_deploy
    vars:
      ome_hostname: "{{ inventory_hostname }}"
      ome_username: "{{ user }}"
      ome_password: "{{ password }}"
      device_service_tag: "ABC1234"
      quick_deploy_options:
        ipv4_enabled: True
        ipv4_network_type: "DHCP"
        password: "calvin"
        slots:
          - slot_id: 1
            vlan_id: 1
          - slot_id: 2
            vlan_id: 1
```



License
-------

Apache 2.0

Author Information
------------------

Anupam Aloke ([@anupamaloke](https://github.com/anupamaloke))
Dell Technologies &copy;2022

ome_device_inventory
=========

Role to run the inventory task for a device (servers, chassis, I/O modules etc.) or a device group (static or query) in OpenManage Enterprise (OME) using:
  - a device service tag, OR
  - a device ID, OR
  - a static or a query group name

Requirements
------------
- Ansible >= 2.9
- Jinja2 >= 2.10
- OpenManage Enterprise >= 3.5
- You must set the ```ANSIBLE_JINJA2_NATIVE``` environment variable to ```true``` before using this role. There are two ways in which you can set it. See [Ansible Documentation](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-jinja2-native) for more details.
  - **Using Environment Variable**
    ```
    $ export ANSIBLE_JINJA2_NATIVE=true
    ```
  - **ansible.cfg**: 
Open your ```ansible.cfg``` file in an editor and add the following key in the ```[defaults]``` section:
    ```
    jinja2_native=true
    ```

Role Variables
--------------

| Parameter | Required | Type | Choices/Default | Example | Description |
|-----------|----------|------|-----------------|---------|-------------|
| ome_hostname | yes | str | None | "192.168.10.10"<br>"ome.example.com" | OME IP address or hostname |
| ome_username | yes | str | None | "admin" | OME user name |
| ome_password | yes | str | None | "Passw0rd" | OME user password |
| device_id | no | int | None | 12345 | ID of the target device |
| device_service_tag | no | str | None | "123ABCD" | Service Tag of the target device |
| ome_group_name | no | str | None | "OME-Static-Group-A" | Group name of a static or a query group |

Dependencies
------------

* dellemc.openmanage

Example Playbook
----------------

* Run inventory task for a server device using device ID

  ```
      - name: "Refresh inventory for a server using ID {{ device_id }}"
        include_role:
          name: ome_device_inventory
        vars:
          ome_hostname: "{{ inventory_hostname }}"
          ome_username: "{{ user }}"
          ome_password: "{{ password }}"
          device_id: 12345
  ```

* Run inventory task for a server device using service tag

  ```
      - name: "Refresh inventory for a server using service tag {{ device_service_tag }}"
        include_role:
          name: ome_device_inventory
        vars:
          ome_hostname: "{{ inventory_hostname }}"
          ome_username: "{{ user }}"
          ome_password: "{{ password }}"
          device_service_tag: "123ABCD"
  ```

* Run inventory task for a static or a query group using group name

  ```
      - name: "Refresh inventory for group {{ ome_group_name }}"
        include_role:
          name: ome_device_inventory
        vars:
          ome_hostname: "{{ inventory_hostname }}"
          ome_username: "{{ user }}"
          ome_password: "{{ password }}"
          ome_group_name: "OME-Static-Group-A"
  ```

Author Information
------------------

Anupam Aloke ([@anupamaloke](https://github.com/anupamaloke))
Dell Technologies &copy;2021

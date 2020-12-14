idrac_import_server_config_profile
=========

Role to import a server configuration profile (SCP) file (xml or json) from a local path or a remote network share (NFS, CIFS, HTTP, HTTPS) using iDRACs (iDRAC7/8 and iDRAC9 only) for Dell EMC PowerEdge servers.

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
| share_parameters | yes | dict | None | {</br>  "ipaddress": "192.168.20.20",</br>  "share_type": "HTTPS",</br>  "share_name": "scp",</br>  "filename": "scp.xml",</br>  "target": "ALL",</br>  "ignore_certificate_warning": "Enabled"</br>} | Share parameters:</br><ul><li>*ipaddress*:<ul><li>Required: no</li><li>Description: IP address of network share (for CIFS, NFS, HTTP and HTTPS only)</li></ul></li><li>*share_name*:<ul><li>Required: no</li><li>Description: network share name</li></ul></li><li>*share_type*:<ul><li>Required: yes</li><li>Choice: [LOCAL, CIFS, NFS, HTTP, HTTPS]</li></ul></li><li>*filename*:<ul><li>Required: yes</li><li>Description: File name for the SCP</li></ul></li><li>*username*:<ul><li>Required: no</li><li>Description: User name to log on to the share (for CIFS share only)</li></ul></li><li>*password*:<ul><li>Required: no</li><li>Description: Password to log on to the share (for CIFS share only)</li></ul></li><li>*workgroup*:<ul><li>Required: no</li><li>Description: Workgroup name to log on to the share</li></ul></li><li>*target*:<ul><li>Required: no</li><li>Description: SCP target components</li><li>Choices: ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID']. Default is 'ALL'</li></ul></li><li>*ignore_certificate_warning*:<ul><li>Required: no</li><li>Description: ignore certificate warning</li><li>Choice: ['Enabled', 'Disabled']. Default is 'Enabled'</li></ul></li></ul> |
| host_power_state | no | str  | <ul><li>'On' *(default)*</li><li>'Off'</li> | 'On' | Host power state after import of server configuration profile |
| shutdown_type | no | str  | <ul><li>'Graceful' *(default)*</li><li>'Forced'</li><li>'NoReboot"</li></ul> | 'Graceful' | Server shutdown type |


Dependencies
------------

None

Example Playbook
----------------

* Import server configuration profile using a file **locally**. In the following example, the server configuration profile is located at ```{{ playbook_dir }}/scp/scp.xml```

  ```
       - name: import scp from a local path
         include_role:
           name: idrac_import_server_config_profile
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ user }}"
           idrac_password: "{{ password }}"
           share_parameters:
             share_type: "LOCAL"
             share_name: "scp"
             filename: "scp.xml"
  ```

* Import server configuration profile using a file located on a **HTTPS** share. In the following playbook example, the server configuration profile is located at ```https://192.168.10.10/scp/scp.xml"

  ```
       - name: import scp from a HTTPS share
         include_role:
           name: idrac_import_server_config_profile
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ user }}"
           idrac_password: "{{ password }}"
           share_parameters:
             ipaddress: "192.168.10.10"
             share_type: "HTTPS"
             share_name: "scp"
             filename: "scp.xml"
  ```

* Import server configuration profile using a file located on a **NFS** share. In the following playbook example, the server configuration profile is located at ```192.168.10.10:/scp/scp.xml```

  ```
       - name: import scp from a NFS share
         include_role:
           name: idrac_import_server_config_profile
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ user }}"
           idrac_password: "{{ password }}"
           share_parameters:
             ipaddress: "192.168.10.10"
             share_type: "NFS"
             share_name: "scp"
             filename: "scp.xml"
  ```

* Import server configuration profile using a file located on a **CIFS** share. In the following playbook example, the server configuration profile is located at ```\\\\192.168.10.10\\scp\\scp.xml```

  ```
       - name: import scp from a CIFS share
         include_role:
           name: idrac_import_server_config_profile
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ user }}"
           idrac_password: "{{ password }}"
           share_parameters:
             ipaddress: "192.168.10.10"
             share_type: "CIFS"
             share_name: "scp"
             filename: "scp.xml"
             username: "{{ cifs_share_username }}"
             password: "{{ cifs_share_password }}"
  ```

Author Information
------------------

Anupam Aloke ([@anupamaloke](https://github.com/anupamaloke))
Dell Technologies &copy;2020

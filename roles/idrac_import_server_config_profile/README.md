idrac_import_server_config_profile
=========

Role to import server configuration profile (SCP) from a file (xml or json) locally or on a remote network share (NFS, CIFS, HTTP, HTTPS) on iDRACs (iDRAC7/8 and iDRAC9 only) for PowerEdge servers.

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
| share_parameters | yes | dict | None | share_parameters: {"ipaddress": "192.168.20.20", "share_type": "HTTPS", "share_name": "scp", "filename": "scp.xml", target: "ALL", "ignore_certificate_warning": "Enabled"} | Share parameters: <ul><li>ipaddress: IP address of network share (for CIFS, NFS, HTTP and HTTPS only)</li><li>share_name: Name of network share - share_type: LOCAL, CIFS, NFS, HTTP, or HTTPS</li><li>filename: File name for the SCP</li><li>username: User name to log on to the share (for CIFS share only)</li><li>password: Password to log on to the share (for CIFS share only)</li><li>workgroup: Workgroup name to log on to the share</li><li>target: 'ALL', 'IDRAC', 'BIOS', 'NIC', or 'RAID'. Default is 'ALL'</li><li>ignore_certificate_warning: 'Enabled', or 'Disabled'</li></ul> |
| host_power_state | no | str  | Choice:  - 'On' (default) - 'Off' | 'On' | Host power state after import of server configuration profile |


Dependencies
------------

None

Example Playbook
----------------

* Import server configuration profile using a file locally.
  In the following example, the server configuration profile is located at ```{{ playbook_dir }}\scp\scp.xml```

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

* Import server configuration profile using a file located on a HTTPS share. In the following playbook example, the server configuration profile is located at ```https://192.168.10.10/scp/scp.xml"

  ```
       - name: import scp from a local path
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

* Import server configuration profile using a file located on a NFS share. In
the following playbook example, the server configuration profile is located at `
``192.168.10.10:/scp/scp.xml"

  ```
       - name: import scp from a local path
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

* Import server configuration profile using a file located on a CIFS share. In
the following playbook example, the server configuration profile is located at `
``192.168.10.10:/scp/scp.xml"

  ```
       - name: import scp from a local path
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

Dell Technologies
Anupam Aloke (@anupamaloke) 2020

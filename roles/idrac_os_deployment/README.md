idrac_os_deployment
=========

Role to perform the below OS deployment tasks on a iDRAC7/8 or iDRAC9:
  - Boot to an ISO image from a remote network share (CIFS or NFS)
  - Detach an ISO image
  - Get the attach status of the ISO image and the Drivers pack

Requirements
------------
- Ansible >= 2.10

Role Variables
--------------

| Parameter | Required | Type | Choices/Default | Example | Description |
|-----------|----------|------|-----------------|---------|-------------|
| idrac_ip | yes | str | None | "192.168.10.10"<br/>"idrac-xyz.example.com" | IP address or hostname of iDRAC |
| idrac_user | yes | str | None | "admin" | iDRAC user name |
| idrac_password | yes | str | None | "Passw0rd" | iDRAC user password |
| command | no | str | <ul><li>'GetAttachStatus' *(default)*</li><li>'BootToNetworkISO'</li><li>'DetachISOImage'</li></ul> | 'GetAttachStatus' | <ul><li>'GetAttachStatus' - attach status of the ISO image and the Drivers packs</li><li>'BootToNetworkISO' - boot to an ISO image from a remote network share (CIFS, NFS)</li><li>'DetachISOImage' - detach an ISO image</li></ul> |
| share_name | no | str | None | "\\\\192.168.11.11\\cifs_share"<br/>"192.168.11.11:/nfsfileshare" | CIFS or NFS network share. This is a **required** argument when I(command=BootToNetworkISO) |
| iso_image | no | str | None | "VMware-VMvisor-Installer-7.0.0-15843807.x86_64-DellEMC_Customized-A00.iso" | ISO filename. This is a **required** argument when I(command=BootToNetworkISO) |
| expose_duration | no | str | 1080 | 30 | Time (in minutes) for the ISO image file to be exposed as a local CD-ROM device to the host server. When the time expires, the ISO image gets automatically detached. This is **optional** when I(command=BootToNetworkISO) |

Dependencies
------------

* dellemc.openmanage

Example Playbook
----------------

* Boot To Network ISO

  ```
      - name: Boot to a network ISO image from a NFS network share
        include_role:
          name: idrac_os_deployment
        vars:
          idrac_ip: "{{ inventory_hostname }}"
          idrac_user: "{{ idrac_user }}"
          idrac_password: "{{ idrac_password }}"
          share_name: "192.168.11.11:/nfs_file_share"
          iso_image: "VMware-VMvisor-Installer-7.0.0-15843807.x86_64-DellEMC_Customized-A00.iso"
          expose_duration: 180
          command: "BootToNetworkISO"
  ```

* Get attach status

  ```
      - name: "Get attach status"
        include_role:
          name: idrac_os_deployment
        vars:
          idrac_ip: "{{ inventory_hostname }}"
          idrac_user: "{{ idrac_user }}"
          idrac_password: "{{ idrac_password }}"
          command: "GetAttachStatus"
  ```

* Detach ISO image

  ```
      - name: "Detach ISO image"
        include_role:
          name: idrac_os_deployment
        vars:
          idrac_ip: "{{ inventory_hostname }}"
          idrac_user: "{{ idrac_user }}"
          idrac_password: "{{ idrac_password }}"
          command: "DetachISOImage"
  ```

Author Information
------------------

Anupam Aloke ([@anupamaloke](https://github.com/anupamaloke))
Dell Technologies &copy;2021

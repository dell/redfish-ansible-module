idrac_lifecycle_controller_job
=========

Role to get a lifecycle controller job information or to delete a lifecycle controller job or to clear the lifecycle controller job queue using iDRACs for Dell EMC PowerEdge servers.

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
| job_id | no | str | None | 'JID_082547249914' | Job ID.<br/>I(job_id) is mandatory if I(command) is either C(Info) or C(Delete). |
| command | no | str | <ul><li>'Info' *(default)*</li><li>'Delete'</li><li>'DeleteJobQueue'</li><li>'DeleteJobQueueForce'</li></ul> | 'Info' | <ul><li>'Info' - get the lifecycle controller job info for a Job ID</li><li>'Delete' - delete the lifecycle controller job for a job ID</li><li>'DeleteJobQueue' - clear the lifecycle controller job queue</li><li>'DeleteJobQueueForce' - force clear the lifecycle controller job queue. This also restarts the Lifecycle Controller services, so please make sure that Lifecycle Controller is in "Ready" state before you run any further tasks on iDRAC. </li></ul> |

Dependencies
------------

None

Example Playbook
----------------

* Get the job info

  ```
       - name: get job info
         include_role:
           name: idrac_lifecycle_controller_job
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           job_id: "JID_082547249914"
  ```

* Delete a job

  ```
       - name: get job info
         include_role:
           name: idrac_lifecycle_controller_job
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           job_id: "JID_082547249914"
           command: "Delete"
  ```

* Clear job queue

  ```
       - name: get job info
         include_role:
           name: idrac_lifecycle_controller_job
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           command: "DeleteJobQueue"
  ```

* Force clear job queue

  ```
       - name: get job info
         include_role:
           name: idrac_lifecycle_controller_job
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           command: "DeleteJobQueueForce"
  ```

Author Information
------------------

Anupam Aloke ([@anupamaloke](https://github.com/anupamaloke))
Dell Technologies &copy;2020

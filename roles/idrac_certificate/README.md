idrac_certificate
=========

Role to manage the iDRAC SSL/TLS certificates - Generate CSR, Import/Export SSL certificates, and Reset SSL configuration - for PowerEdge servers

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
| command | no | str | <ul><li>'Info' *(default)*</li><li>'GenerateSSLCSR'</li><li>'ImportSSLCertificate'</li><li>'ExportSSLCertificate'</li><li>'SSLResetCfg'</li></ul> | 'Info' | <ul><li>'Info' - get the iDRAC web-server SSL certificate details</li><li>'GenerateSSLCSR' - create the certificate signing request (CSR) and return it. The certificate is copied to the file provided in I(csr_file). Please note that the following iDRAC security attributes must be configured prior to sending a CSR request to iDRAC: (1). Security.1.CsrCommonName, (2). Security.1.CsrOrganizationName, (3). Security.1.CsrOrganizationUnit, (4). Security.1.CsrLocalityName, (5). Security.1.CsrStateName, (6). Security.1.CsrCountryCode, (7). Security.1.CsrEmailAddr. </li><li>'ImportSSLCertificate' - import the SSL certificate provided in the argument I(ssl_cert_file) to iDRAC, on the basis of I(ssl_cert_type). After importing the certificate, iDRAC will automatically restart.</li><li>'ExportSSLCertificate' - export the iDRAC SSL certificate and write it to a file provided in the argument I(ssl_cert_file). </li><li>'SSLResetCfg' - restore the iDRAC web-server certificate to factory defaults. After performing SSL reset, iDRAC might need to be restarted to apply the default certificate.</li></ul> |
| ssl_cert_type | no | str | <ul><li>'Server' *(default)*</li><li>'CA'</li><li>'CSC'</li><li>'Client Trust Certificate'</li></ul> | 'Server' | Type of certificate to be imported.</br>This argument should be provided only when I(command=ImportSSLCertificate) or I(command=ExportSSLCertificate). |
| ssl_cert_file | yes | path | None | "{{ playbook_dir }}/{{ inventory_hostname }}.cert" | A base 64 encoded string of the XML Certificate file. This is a **required** argument when I(command=ImportSSLCertificate).<br/>Note: For importing CSC certificate, user has to convert PKCS file to base64 format. Use the openssl command. The CTC file content has to be in PEM format (base 64 encoded). |
| csr_file | no | path | "{{ idrac_ip }}.csr" | "{{ playbook_dir }}/{{ inventory_hostname }}.csr" | File name to copy the CSR.<br/>This argument is only applicable when I(command=GenerateSSLCSR) |
| idrac_firmware_version | no | str | None | "4.00.00.00" | This variable is defined in the role ***idrac_facts*** and used within this role to determine the Redfish API capability currently being supported by the iDRAC. See U(https://github.com/dell/redfish-ansible-module/tree/master/roles/idrac_facts) for an overview of the ***idrac_facts*** role. |

Dependencies
------------

- idrac_facts
  - Re-uses 'idrac_firmware_version' variable to determine the current iDRAC firmware version and thus the current Redfish API capability. 

Example Playbook
----------------

* **Get SSL Certificate information**

```
     - block:
       - name: get iDRAC SSL certificate information
         include_role:
           name: idrac_certificate
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           command: "Info"
       tags:
         - info
```

* **Generate SSL Certificate Signing Request (CSR)**

```
     - block:
       - name: generate certificate signing request
         include_role:
           name: idrac_certificate
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           command: "GenerateSSLCSR"
           csr_file: "{{ idrac_ip }}.csr"
       tags:
         - generatesslcsr
```

* **Import SSL Certificate**

```
   roles:
     - role: idrac_facts
       vars:
         idrac_ip: "{{ inventory_hostname }}"
         idrac_user: "{{ idrac_user }}"
         idrac_password: "{{ idrac_password }}"
       tags:
         - always

   tasks:
     - block:
       - name: import ssl certificate
         include_role:
           name: idrac_certificate
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           command: "ImportSSLCertificate"
           ssl_cert_type: "Server"
           ssl_cert_file: "{{ idrac_ip }}_ssl_cert.pem"
       tags:
         - importsslcertificate
```

* **Export SSL Certificate**

```
   roles:
     - role: idrac_facts
       vars:
         idrac_ip: "{{ inventory_hostname }}"
         idrac_user: "{{ idrac_user }}"
         idrac_password: "{{ idrac_password }}"
       tags:
         - always

   tasks:
     - block:
       - name: export ssl certificate
         include_role:
           name: idrac_certificate
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           command: "ExportSSLCertificate"
           ssl_cert_type: "Server"
           ssl_cert_file: "{{ playbook_dir }}/{{ idrac_ip }}.cert"
       tags:
         - exportsslcertificate
```

* **SSL Reset to Factory Defaults**

```
   roles:
     - role: idrac_facts
       vars:
         idrac_ip: "{{ inventory_hostname }}"
         idrac_user: "{{ idrac_user }}"
         idrac_password: "{{ idrac_password }}"
       tags:
         - always

   tasks:
     - block:
       - name: reset ssl config to factory defaults
         include_role:
           name: idrac_certificate
         vars:
           idrac_ip: "{{ inventory_hostname }}"
           idrac_user: "{{ idrac_user }}"
           idrac_password: "{{ idrac_password }}"
           command: "SSLResetCfg"
       tags:
         - sslresetcfg
```

License
-------

Apache 2.0

Author Information
------------------

Anupam Aloke ([@anupamaloke](https://github.com/anupamaloke))
Dell Technologies &copy;2021

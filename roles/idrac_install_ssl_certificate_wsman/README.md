idrac_install_ssl_certificate_wsman
=========

role to leverage the WSMAN SOAP api to manage SSL certificates for iDRACs on Dell Poweredge Systems. This role supports importing private + public keys from SSL certificates created externaly.

Requirements
------------

Requirements can be found inside of the requirements files.

## Python requirements
### Development
```
ansible
docker
molecule
pre-commit
pip-tools
omsdk
pyOpenSSL


```
### Production
```
ansible
omsdk
pyOpenSSL
```

## Ansible
### Development
```
ansible.core
dellemc.openmanage
```

### Production
```
ansible.core
```


Role Variables
--------------

| Name | Required | Default Value | Example | Description |
| ------- | ------------ | ------------------ | ------------ | -------------|
| ca_cert_file | no |  None | "files/ca.crt" | Path to root ca cert to validate target SSL cert against |
| certificate_file | no |  None | "files/public-signed-certificate.pem" | Path to signed CSR public key |
| certificate_format | yes |  "PEM" | "PKCS" | Key format of the SSL keys being used |
| change_certificate | yes |  false | true | switch to force replacement of keys. If set to 'false' the role will decide if a replacement is needed |
| idrac_https_port | yes |  443 | 8443 | Port the iDRAC API is rechable on |
| idrac_user | yes |  root | admin | User with privileges to change the SSL certificate |
| idrac_user_password | yes |  calvin | "Passw0rd." | Password for the iDRAC user being used |
| pkcs12_password | no |  None | "Passw0rd." | Password for the PKCS file if it was set|
| privatekey_file | no |  None | files/private_key.pem | Path to the private key file if it should be imported together with the private key |


Example Playbook
----------------

idrac1.yml
```
---

ansible_user: root
idrac_address: 10.113.0.46
idrac_user: root
idrac_user_password: calvin
idrac_https_port: 443
ca_cert_file: "./test_files/root-ca.pem"
certificate_file: "./test_files/signed-certificate.pem"
privatekey_file: "./test_files/private-key.pem"
certificate_format: "PEM"
```

hosts
```
idrac1

```

main.yml
```
---

- name: manage SSL certificate
  hosts: all
  gather_facts: no
  tasks:
    - name: "Include idrac_manage_ssl_certificate_wsman"
      include_role:
        name: "idrac_manage_ssl_certificate_wsman"

```


Author Information
------------------

Dell Technologies
Simon Lichtenauer (Simon.Lichtenauer@Dell.com) 2020

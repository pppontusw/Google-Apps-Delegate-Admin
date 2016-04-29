# Google-Apps-Delegate-Admin

## What is it?

This is a tool to manage Mail delegations on Google Apps.

## What do you have to do?

1. Edit config.py to a proper random secret for CSRF
2. Generate and put your own client_secrets.json

## How can I use this role?

We can use this role to install a preconfigured version of Google Apps Group Sync to any Debian/Ubuntu/RedHat/CentOS server

For example we can pass the following settings (no service account):

```
#example-playbook.yml

- name: example
  hosts: groupsyncservers
  become: true
  vars: 
    - gapps_group_sync_user: 'root'
    - LDAPBaseDN: 'OU=OrgUnit,DC=example,DC=com'
    - LDAPUrl: 'ldap://example.com'
    - LDAPUserDN: 'gadgs@example'
    - LDAPUserPassword: 'notapassword'
    - LDAPAllUserGroupDN: 'CN=GoogleUsers,OU=OrgUnit,DC=example,DC=com'
    - CLIENT_SECRET_FILE_PATH: 'client_secret.json'
    - CLIENT_SECRET_JSON: <jsonfileetc>
  roles:
    - gapps-group-sync
```

and a JSON file that looks like this:

```
#initdb.json.j2

[{
    "gappslist": "nordics@example.com",
    "members": [
        {
        "attribute": "physicalDeliveryOfficeName",
        "value": "Denmark"
        },
        {
        "attribute": "physicalDeliveryOfficeName",
        "value": "Sweden"
        },
        {
        "attribute": "physicalDeliveryOfficeName",
        "value": "Norway"
        },
        {
        "attribute": "physicalDeliveryOfficeName",
        "value": "Finland"
        }
    ],
    "type": "AND"
    },
    {
    "gappslist": "US-IT@example.com",
    "members": [
        {
        "attribute": "physicalDeliveryOfficeName",
        "value": "US"
        },
        {
        "attribute": "Department",
        "value": "IT"
        }
    ],
    "type": "OR"
}]
```

``` ansible-playbook example-playbook.yml ```

## Compability

Tested on:

Debian 8 & CentOS 7


Edit config.py with a proper random secret (for CSRF)

```
pip install flask
pip install flask-wtf
pip install xmltodict
```

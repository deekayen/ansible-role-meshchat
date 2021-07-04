# mesh chat

Install [Trevor Paskett](http://www.trevorsbench.com/meshchat-messaging-for-mesh-networks/)'s mesh chat for [AREDN](https://www.arednmesh.org/).

Requirements
------------

Outbound Internet to download the installer from AWS S3.

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

```
pi_zone: MeshChat
local_meshchat_node: localnode
```

Dependencies
------------

ansible.builtin:>=1.5

Example Playbook
----------------

```
---
- name: Install mesh chat.
  hosts: all
  become: yes

  roles:
    - role: deekayen.meshchat
      vars:
        local_meshchat_node: N4DKN-BM2XW-OMNI-204
```

License
-------

BSD-3-Clause

Author Information
------------------

Role created by [David Norman](https://github.com/deekayen) - N4DKN.

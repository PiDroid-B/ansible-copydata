# Ansible Role : copydata

[![Ansible Role](https://img.shields.io/ansible/role/53409?label=Galaxy)](https://galaxy.ansible.com/pidroid_b/copydata)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/PiDroid-B/ansible-copydata)](https://galaxy.ansible.com/pidroid_b/copydata)
[![Ansible Quality Score](https://img.shields.io/ansible/quality/53409?label=Ansible%20Quality)](https://galaxy.ansible.com/pidroid_b/copydata)
![Ansible Role](https://img.shields.io/ansible/role/d/53409)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

| Branch | master | dev | 
|:----|:----|:---:| 
| CI | [![Ansible Molecule](https://github.com/PiDroid-B/ansible-copydata/workflows/Ansible%20Molecule/badge.svg?branch=master)](https://github.com/PiDroid-B/ansible-copydata/actions?query=workflow%3A%22Ansible+Molecule%22) | [![Ansible Molecule](https://github.com/PiDroid-B/ansible-copydata/workflows/Ansible%20Molecule/badge.svg?branch=dev)](https://github.com/PiDroid-B/ansible-copydata/actions?query=workflow%3A%22Ansible+Molecule%22) |


Ansible role to copy files and directories according to the hostnames and groupnames  

- copy only files included in "data inventory" to the target
- remove all other files on the target (optional)

## Table of Contents  
* [How it works](#how-it-works)
* [copydata vs ansible.builtin.copy](#copydata-vs-ansiblebuiltincopy)
* [Role Variables](#role-variables)
* [Example Playbook](#example-playbook)
* [Installation](#installation)
* [Platforms](#platforms)
* [How to build data inventory](#how-to-build-data-inventory)
* [Use cases](#use-cases)
  * [Copy : resolv.conf](#copy--resolvconf)
  * [Append : iptables rules](#append--iptables-rules)
* [License](#license)
* [Author Information](#author-information)
* [Feedback, bug-reports, requests, ...](#feedback-bug-reports-requests-)


## How it works 
[:arrow_up:](#table-of-contents)  
Files are read in the following directories (cf [How to build data inventory](#how-to-build-data-inventory) for more information) :
- `{copydata_datadir}/group/all/{copydata_src}`
- `{copydata_datadir}/group/{group_names|list}/{copydata_src}`
- `{copydata_datadir}/host/{inventory_hostname}/{copydata_src}`

Three modes :
- copy : When files with same name found, only the most precise will be kept
- append : When files with same name found, the target file is concatenated from all sources' files 
  (from most global to most precise)
- append_reverse : When files with same name found, the target file is concatenated from all sources' files 
  (from most precise to most global)

## copydata vs ansible.builtin.copy
[:arrow_up:](#table-of-contents)  

- `ansible.builtin.copy`
The `copy` module copies a file from the local or remote machine to a location on the remote machine.
[(source)](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html)

- `copydata`
Manage files' list to copy or concat files from data inventory tree
This role can manage copy of concatenation of files from data inventory tree on the local machine 
  to a location on the remote machine with prioritization.

## Role Variables
[:arrow_up:](#table-of-contents)  

| variable | mandatory | description | example | 
|:----|:----:|:----|:----|
| copydata_datadir | :heavy_check_mark: | path of the data inventory contains host and group folders (see [How to build data inventory](#how-to-build-data-inventory))  | `/path/of/data/` |
| copydata_src | :heavy_check_mark: | subfolder of host or group, can be a role-name (see [How to build data inventory](#how-to-build-data-inventory)) | `myfeature` |
| copydata_dest | :heavy_check_mark: | full path of target on the remote hosts | `/tmp/target/` |
| copydata_patterns | | array of patterns defined files' type will be copied (default='`*`') | `[*.conf, *.tmp]` |
| copydata_remove_other_files | | remove files not found in source folders and according with `copydata_patterns`<br>:warning: wrong usage can remove wrong files, please check before use :warning: | `False` |:
| copydata_owner | :heavy_check_mark: | owner of the copied files  | `root` |
| copydata_group | :heavy_check_mark: | group of the copied files  | `root` |
| copydata_mode | :heavy_check_mark: | mode of the copied files  | `755` | 
| copydata_copy_type | | select one of those mode : copy, append or append_reverse (default='`copy`') | `append` |
| copydata_template | | only for append or append_reverse, define an alternative template  | `path/to/my/template` |
| copydata_debug | | show summary of all files will be copied to the target | `True` |

## Output variable
| variable | description | values |
|:----|:----|:----:|
| copydata_changed | workaround about missing "changed" attribute of the role | `True`,`False` |

## Example Playbook
[:arrow_up:](#table-of-contents)
```yaml
---
- name: Converge
  hosts: all
  tasks:
    - name: "Copydata"
      include_role:
        name: "copydata"
      vars:
        copydata_datadir: "{{data_dir}}"
        copydata_src: 'scenario_default/'
        copydata_dest: '/tmp/testcopy/'
        copydata_owner: 'root'
        copydata_group: 'root'
        copydata_mode: 770
        copydata_debug: True
    - name: "Result"
      debug:
        msg: |
          copydata_changed : {{ copydata_changed }}
```

## Installation
[:arrow_up:](#table-of-contents)

Tested on Ansible's versions :
- 2.8
- 2.9
- 2.10

Latest stable release 

* Ansible Galaxy : coming soon 
* GitHub : `git clone https://github.com/PiDroid-B/ansible-copydata.git`



## Platforms
[:arrow_up:](#table-of-contents)

Tested on :
* Debian 9 (Stretch)
* Debian 10 (Buster)
* Ubuntu 16.04 LTS (Xenial Xerus)
* Ubuntu 18.04 LTS (Bionic Beaver)
* Ubuntu 20.04 LTS (Focal Fossa)


## How to build data inventory
[:arrow_up:](#table-of-contents)  

Data inventory tree must be built as following :
`<copydata_datadir>`/`(group|host)`/`<item>`/`<copydata_src>`/

Example :
if we define : `copydata_datadir: "{{ inventory_dir }}/../data/"`
Our inventory and data inventory should be strutured as following
```
├── data
│   ├── group
│   │   ├── all
│   │   │   └── myrole
│   │   │       ├── file_for_everybody_1
│   │   │       └── file_for_everybody_2
│   │   └── gp1
│   │       └── myrole
│   │           └── file_just_for_group_gp1
│   └── host
│       ├── myhost
│       │   └── myrole
│       │       └── any_file
│       └── anotherhost
│           └── myrole
│               └── other_file
└── inventory
    ├── group_vars
    │   ├── all
    │   └── gp1
    ├── host_vars
    │   ├── myhost
    │   │   └── great_var
    │   └── anotherhost
    └── main.yml
```

## Use cases
[:arrow_up:](#table-of-contents)

**Note :**
- Inventory is present only to show structure, it can be replaced by only one file or whatever you want  

### Copy : resolv.conf
[:arrow_up:](#table-of-contents)

Playbook to set the resolv.conf of several hosts (one dns server, some other hosts and an offsite host)

#### Inventory and Data Inventory
```
├── data
│   ├── group
│   │   ├── all
│   │   │   └── myplaybook
│   │   │       └── resolv.conf
│   │   └── dns
│   │       └── myplaybook
│   │           └── resolv.conf
│   └── host
│       └── external-machine
│           └── myplaybook
│               └── resolv.conf
└── inventory
    ├── group_vars
    │   ├── all
    │   └── dns
    ├── host_vars
    │   ├── external-machine
    │   └── my-dns
    └── main.yml
```

#### Playbook
```yaml
---
- hosts: all
  roles:
    - role: copydata
      vars:
        # path of data inventory
        copydata_datadir: "{{ inventory_dir }}/../data/"
        # subdir of entries in data inventory
        copydata_src: 'myplaybook/'
        # target folder
        copydata_dest: '/etc/'
        # all actions will be limited by this pattern
        copydata_patterns: "resolv.conf"
        # owner/group/mode to apply to the target files
        copydata_owner: 'root'
        copydata_group: 'root'
        copydata_mode: '644'
```

#### Result
Hosts:
  - my-dns (server dns on site, in group `dns`) : `/etc/resolv.conf` == `data/group/dns/myplaybook/resolv.conf`
  - external-machine (an offsite machine with specific dns) : `/etc/resolv.conf` == `data/host/external-machine/myplaybook/resolv.conf` 
  - all other (don't match with previous cases, client dns of my-dns) : `/etc/resolv.conf` == `data/group/all/myplaybook/resolv.conf`

### Append : iptables rules
[:arrow_up:](#table-of-contents)

Playbook to build files of ipv4 and ipv6 rules (used on each machine with `iptables-restore` and `ip6tables-restore` ). 
For each filename, all according files will be concatened from most global to most precise.
All other files according with the pattern `*.rules` must be removed.  
In this example, we have the following hosts/groups :  

| group | hosts |
|:---|:---|
| dbms | sv-dbms1, sv-dbms2 |
| web | sv-web1, sv-web2, sv-web3 |

#### Inventory and Data Inventory
```
└── data
    ├── group
    │   ├── all
    │   │   └── my_ip_rules
    │   │       ├── ipv4.rules
    │   │       └── ipv6.rules
    │   ├── dbms
    │   │   └── my_ip_rules
    │   │       ├── ipv4.rules
    │   │       └── ipv6.rules
    │   └── web
    │       └── my_ip_rules
    │           ├── ipv4.rules
    │           └── ipv6.rules
    └── host
        ├── sv-web1
        │   └── my_ip_rules
        │       ├── ipv4.rules
        │       └── ipv6.rules
        ├── sv-web2
        │   └── my_ip_rules
        │       ├── ipv4.rules
        │       └── ipv6.rules
        └── sv-web3
            └── my_ip_rules
                ├── ipv4.rules
                └── ipv6.rules
```

#### Playbook
```yaml
---
- hosts: all
  roles:
    - role: copydata
      vars:
        # path of data inventory
        copydata_datadir: "{{ inventory_dir }}/../data/"
        # subdir of entries in data inventory
        copydata_src: 'my_ip_rules/'
        # target folder
        copydata_dest: '/etc/firewall/'
        # all actions will be limited by this pattern
        copydata_patterns: "*.rules"
        # remove all other files in according with the patterns ("*.rules")
        copydata_remove_other_files: True
        # owner/group/mode to apply to the target files
        copydata_owner: 'root'
        copydata_group: 'root'
        copydata_mode: '644'
```

#### Result
Hosts:
  - sv-dbms1 and sv-dbms2
    - ipv4.rules is the concatenation of the following files in this order
      - `data/group/all/my_ip_rules/ipv4.rules`
      - `data/group/dbms/my_ip_rules/ipv4.rules`
    - ipv6.rules (idem)
  - sv-web1
    - ipv4.rules is the concatenation of the following files in this order
      - `data/group/all/my_ip_rules/ipv4.rules`
      - `data/group/web/my_ip_rules/ipv4.rules`
      - `data/host/sv-web1/my_ip_rules/ipv4.rules`
    - ipv6.rules (idem)
  - sv-web2
    - ipv4.rules is the concatenation of the following files in this order
      - `data/group/all/my_ip_rules/ipv4.rules`
      - `data/group/web/my_ip_rules/ipv4.rules`
      - `data/host/sv-web2/my_ip_rules/ipv4.rules`
    - ipv6.rules (idem)
  - sv-web3
    - ipv4.rules is the concatenation of the following files in this order
      - `data/group/all/my_ip_rules/ipv4.rules`
      - `data/group/web/my_ip_rules/ipv4.rules`
      - `data/host/sv-web3/my_ip_rules/ipv4.rules`
    - ipv6.rules (idem)  
  

## License
[:arrow_up:](#table-of-contents)  

> Creative Commons : Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)   
[![CC BY-NC-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-nc-sa.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

## Author Information
[:arrow_up:](#table-of-contents)  

PiDroid-B 

## Feedback, bug-reports, requests, ...
[:arrow_up:](#table-of-contents)  

Are [welcome](https://github.com/PiDroid-B/ansible-copydata/issues) !

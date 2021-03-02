# Tests Molecule/Docker

## Table of Contents  
* [Notes](#notes)
* [Directories and scenarios](#directories-and-scenarios)
  * [_common/](#_common)
  * [default (copy)](#default-copy)
  * [default_append](#default_append)
  * [default_append_reverse](#default_append_reverse)
  
## Notes
`molecule test --all`

- Python < 3.6 on old release :
  - F String must be replaced by `" ".format()`

## Directories and scenarios
[:arrow_up:](#table-of-contents)

### _common/
[:arrow_up:](#table-of-contents)  
shared folder between all tests

- `_common/data/` > data inventory, inputs for this role
- `_common/inventory/` > ansible inventory
- `Dockerfile.j2` > Template dockerfile for test with Docker

#### default (copy)
[:arrow_up:](#table-of-contents)  

test the Copy feature
(converge with become: True)

##### Step 1 Default - copy to new path (default options)

**options :** nothing

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/gp_lv1 |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/gp_lv2 |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |  

##### Step 2 path exists - copy to an already existing path without remove other files

**options :** nothing

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/gp_lv1 |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/gp_lv2 |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |  

##### Step 3 remove - copy to an already existing path with remove other files

**options :**  
- remove other files

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | |  
| other_file.dummy | X | | |  
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/gp_lv1 |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/gp_lv2 |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance |
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 4 pattern - copy to an already existing path with pattern

**options :**  
- pattern = "*host1.dummy"

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| other_file.dummy | X | | X |  
| all.dummy | | group/all | |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 5 remove pattern - copy to an already existing path with remove other files and pattern

**options :**   
- remove other files
- pattern = ["*host1.dummy", "other_file.dummy"]

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| other_file.dummy | X | | |  
| all.dummy | | group/all | |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 6 become - role launched with ansible_become: True

**options :** ansible_become: True

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| onlyhost1.dummy | | host/instance | host/instance |  

#### default_append
[:arrow_up:](#table-of-contents)  

test the Append feature (files sorted from global to precise) 

##### Step 1 Default - append to new path (default options)

**options :** nothing

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/all<BR>group/gp_lv1 |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/all<BR>group/gp_lv1<BR>group/gp_lv2 |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 2 path exists - append to an already existing path without remove other files

**options :** nothing

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/all<BR>group/gp_lv1 |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/all<BR>group/gp_lv1<BR>group/gp_lv2 |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 3 remove - append to an already existing path with remove other files

**options :**  
- remove other files

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | |  
| other_file.dummy | X | | |  
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/all<BR>group/gp_lv1 |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/all<BR>group/gp_lv1<BR>group/gp_lv2 |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 4 pattern - append to an already existing path with pattern

**options :**  
- pattern = "*host1.dummy"

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| other_file.dummy | X | | X |  
| all.dummy | | group/all | |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 5 remove pattern - append to an already existing path with remove other files and pattern

**options :**   
- remove other files
- pattern = ["*host1.dummy", "other_file.dummy"]

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| other_file.dummy | X | | |  
| all.dummy | | group/all | |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 6 become - role launched with ansible_become: True

**options :** ansible_become: True

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| onlyhost1.dummy | | host/instance | host/instance |  

#### default_append_reverse
[:arrow_up:](#table-of-contents)  

test the Append_reverse feature (files sorted from precise to global)

##### Step 1 Default - append to new path (default options)

**options :** nothing

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/gp_lv1<BR>group/all |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/gp_lv2<BR>group/gp_lv1<BR>group/all |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance<BR>group/gp_lv2<BR>group/gp_lv1<BR>group/all |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 2 path exists - append to an already existing path without remove other files

**options :** nothing

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/gp_lv1<BR>group/all |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/gp_lv2<BR>group/gp_lv1<BR>group/all |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance<BR>group/gp_lv2<BR>group/gp_lv1<BR>group/all |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 3 remove - append to an already existing path with remove other files

**options :**  
- remove other files

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | |  
| other_file.dummy | X | | |  
| all.dummy | | group/all | group/all |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | group/gp_lv1<BR>group/all |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | group/gp_lv2<BR>group/gp_lv1<BR>group/all |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance<BR>group/gp_lv2<BR>group/gp_lv1<BR>group/all |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 4 pattern - append to an already existing path with pattern

**options :**  
- pattern = "*host1.dummy"

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| other_file.dummy | X | | X |  
| all.dummy | | group/all | |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance<BR>group/gp_lv2<BR>group/gp_lv1<BR>group/all |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 5 remove pattern - append to an already existing path with remove other files and pattern

**options :**   
- remove other files
- pattern = ["*host1.dummy", "other_file.dummy"]

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| other_file.dummy | X | | |  
| all.dummy | | group/all | |  
| gp1.dummy | | group/all<BR>group/gp_lv1 | |  
| gp2.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2 | |  
| host1.dummy | | group/all<BR>group/gp_lv1<BR>group/gp_lv2<BR>host/instance | host/instance<BR>group/gp_lv2<BR>group/gp_lv1<BR>group/all |  
| onlyhost1.dummy | | host/instance | host/instance |

##### Step 6 become - role launched with ansible_become: True

**options :** ansible_become: True

| File | Prepare | Data Inventory | Verify |
|:---|:---|:---|:---|
| other_file | X | | X |  
| other_file.dummy | X | | | 
| onlyhost1.dummy | | host/instance | host/instance |  
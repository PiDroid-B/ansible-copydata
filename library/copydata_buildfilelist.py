#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Pidroid-B
# Creative Common BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)

from __future__ import absolute_import, division, print_function

DOCUMENTATION = '''
module: copydata_buildfilelist
author: Pidroid-B 
short_description: Manage files' list to copy or concat files from data inventory tree
description: 
    - copy : only kept the most precise file through a data inventory tree for each filename
    - append : concat from most global to most precise files (or vice-versa) for each filename
    - use modules : find, copy, file, template 

options:
    find_list:
        description:
        - array of registered variables coming from find module (with or without loop)
        - must be sorted from most precise to most global
        type: array
        required: yes
    merge:
        description:
        - copy : only kept the most precise file when several files with same filename
        - append : concat from most global to most precise files
        - append_reverse : concat from most precise to most global files 
        type: str
        default: 'copy'
        required: yes
    debug:
        description:
        - show some information about execution
        type: bool
        default: False
'''

EXAMPLES = '''
- name: "main > all : scan"
  find:
    paths: "data/group/all/myrole/"
  register: _copydata_filelist_tmp_all
  delegate_to: "localhost"

- name: "main > group : scan"
  find:
    paths: "data/group/{{ item }}/myrole/"
  register: _copydata_filelist_tmp_gp
  loop: "{{ group_names }}"
  delegate_to: "localhost"

- name: "main > host : scan"
  find:
    paths: "data/host/{{ inventory_hostname }}/myrole/"
  register: _copydata_filelist_tmp_host
  delegate_to: "localhost"

- name: "main > build files' list"
  copydata_buildfilelist:
    merge: "copy"
    debug: "{{ copydata_debug }}"
    find_list:
      - "{{ _copydata_filelist_tmp_host }}"
      - "{{ _copydata_filelist_tmp_gp }}"
      - "{{ _copydata_filelist_tmp_all }}"
  register: _copydata_filelist_tmp
  
- name: "Result"
  debug:
    var: "{{ item }}"
  with_items:
    - _copydata_filelist_tmp.meta.filenames
    - _copydata_filelist_tmp.meta.sources
  when: copydata_debug|default()  
'''

RETURN = '''
filenames:
    description: list of all filenames
    returned: success
    type: list
    sample: ['file_1','file_2']
    
sources: 
    description: array of full paths' files for copy or (filename, [array of paths]) for append
    returned: success
    type: list
    sample: ['/my/path/file_1','/my/path2/file_2'] or ['file_1', ['/my/pathA','/my/pathB'], ['file_2', ['/my/pathA']]
'''

import os.path
import json

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type


def do_convert_to_record(module, dict_files, priority):
    """
    Return converted files path
    Input :
        files:[{path:}...]}
    Output :
        [{file: , path: , priority: }]
    """
    transformed_dict = []

    if "files" in dict_files:
        for item in dict_files["files"]:
            (spath, sfile) = os.path.split(item["path"])
            transformed_dict.append(
                {"file": sfile, "path": spath, "priority": priority}
            )
        return transformed_dict
    else:
        module.fail_json(
            msg="Wrong syntax in one of the dict/array of dict included in the array 'find_list', "
                "key files not found in : {}".format(json.dumps(dict_files))
        )


def do_flatten_and_convert(module, dict_find, priority):
    """
    Return flatten and converted result of find module with or without loop
    Input :
        single find : files:[{path:}...]}
        find with loop : results[{files:[{path:}...]},{files:[{path:}...]}]
    Output :
        [{file: , path: , priority: }]
    """
    transformed_dict = []

    # Find with loop clause contains
    if "results" in dict_find:
        for item in dict_find["results"]:
            transformed_dict = transformed_dict + do_convert_to_record(
                module, item, priority
            )
    else:
        transformed_dict = do_convert_to_record(module, dict_find, priority)

    return transformed_dict


def do_sort_array(arr_file_path_prio, reverse=False):
    """
    Return sorted array according to the wanted order (copy, append and append_reverse)
    Input :
        [{file: , path: , priority: }]
    Output :
        [{file: , path: , priority: }]
    """
    if reverse:
        # from most global to most precise
        # append : take all items found by priority
        #
        # order (priority DESC, path ASC):
        # - by path dest (for a same priority, last path is more global than the paths above
        # - by priority (highest priority to the lowest number)
        arr_file_path_prio.sort(key=lambda x: x["path"])
        arr_file_path_prio.sort(key=lambda x: x["priority"], reverse=True)
    else:
        # from most precise to most global
        # copy : take the first item found by priority
        # append_reverse : take all items found by priority
        #
        # order (priority ASC, path DESC) :
        # - by path dest (for a same priority, last path is more precise than the paths above
        # - by priority (highest priority to the lowest number)
        arr_file_path_prio.sort(key=lambda x: x["path"], reverse=True)
        arr_file_path_prio.sort(key=lambda x: x["priority"])

    return arr_file_path_prio


def do_build_array_copy(module, arr_file_path_prio):
    """
    Return sources (for copy) and filenames (for exlude files to remove step)
    If several files with the same name, only the most precise will be kept
    Input:
        [{file: , path: , priority: }]
    Output
        [{sources: [...], filenames: [...] }]
    """
    dict_sources = {}

    arr_file_path_prio = do_sort_array(arr_file_path_prio)

    for item in arr_file_path_prio:
        dict_sources.setdefault(item["file"], item["path"])

    # return an array of file (with path) on the source side
    return {
        "sources": [os.path.join(v, k) for k, v in dict_sources.items()],
        "filenames": [k for k in dict_sources.keys()],
    }


def do_build_array_template(module, arr_file_path_prio, reverse=False):
    """
    Return sources (for template) and filenames (for exlude files to remove step)
    If append (reverse=False), then concat from global to precise
    If append_reverse (reverse=True), then concat from precise to global
    Input:
        [{file: , path: , priority: }]
    Output
        [{sources: [(filename),[list of paths]...], filenames: [...] }]
    """
    dict_sources = {}

    # append need a reverse sort from copy
    arr_file_path_prio = do_sort_array(arr_file_path_prio, not reverse)

    for item in arr_file_path_prio:
        dict_sources.setdefault(item["file"], [])
        dict_sources[item["file"]].append(os.path.join(item["path"], item["file"]))

    # return an array of file (with path) on the source side
    return {
        "sources": [(k, v) for k, v in dict_sources.items()],
        "filenames": [k for k in dict_sources.keys()],
    }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            find_list=dict(type="list", required=True),
            merge=dict(
                type="str", choices=["copy", "append", "append_reverse"], required=True
            ),
            debug=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    debug = module.params["debug"]
    if debug:
        module.warn("DEBUG > Type of copydata : {}".format(module.params['merge']))
        module.warn("DEBUG > find_list : {}".format(module.params['find_list']))

    # array of results of module find / find+loop
    array_finddict = module.params["find_list"]

    ipriority = 0
    arr_file_path_prio = []
    for findfict in array_finddict:
        arr_file_path_prio = arr_file_path_prio + do_flatten_and_convert(
            module, findfict, ipriority
        )
        ipriority += 1

    # module.warn(json.dumps())
    if module.params["merge"] == "copy":
        arr_tmp = do_build_array_copy(module, arr_file_path_prio)
    elif module.params["merge"] == "append":
        arr_tmp = do_build_array_template(module, arr_file_path_prio)
    else:
        arr_tmp = do_build_array_template(module, arr_file_path_prio, True)

    module.params = {}
    module.params.setdefault("sources", arr_tmp["sources"])
    module.params.setdefault("filenames", arr_tmp["filenames"])

    if debug:
        module.warn("DEBUG > sources : {}".format(arr_tmp['sources']))
        module.warn("DEBUG > filenames : {}".format(arr_tmp['filenames']))

    module.exit_json(changed=False, meta=module.params)


if __name__ == "__main__":
    main()

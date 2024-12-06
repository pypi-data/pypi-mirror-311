#!/usr/bin/env python3

from typing import Dict, List, NamedTuple
from pathlib import Path
import re
import json
from collections import defaultdict
from copy import deepcopy
# from JsonOperate.lib.output import PrintCaseInfoOutputByPanda
from JsonOperate.lib.replace_schema import schema_replace

def get_structure(data):
    list_dim = 0
    keys = []
    value = None
    if isinstance(data, list):
        #here we suppose if the first item is same as others list[0]->list[...]/ dict[0]->dict[...]/ directvalure[0]->directvalure[...] 
        for subvalue in data:
            sub_list_dim, sub_keys, sub_value = get_structure(subvalue)
            if sub_keys != []:
                keys = list(set(keys + sub_keys))
                # keys.append(sub_keys)
        
        if keys != []:
            list_dim = sub_list_dim + 1
        else:
            value = data
    elif isinstance(data, dict):
        # contain_dict = 1
        keys = [key for key in data.keys()]
    else:
        value = data
    
    return list_dim, keys, value

def is_in_list(value, search_data):
    for serch_value in search_data:
        if value == serch_value:
            return 1
    return 0

def is_all_lists(data):
    if isinstance(data, list):
        # If the current level is a list, check its elements recursively
        return all(is_all_lists(item) for item in data)
    elif isinstance(data, dict):
        # If the current level is a dictionary, check its values recursively
        return False
    else:
        # If the current level is neither a list nor a dictionary, it's not all lists
        return True

# def is_ul_case(cell_infos):
#     for cell_info in cell_infos:
#         if cell_info["uplink"]:
#             return True
#     return False

# def is_dl_case(cell_infos):
#     for cell_info in cell_infos:
#         if cell_info["downlink"]:
#             return True
#     return False
    
keys = ['key', 'name', 'feature', 'value', 'value_type']

# MAX_CHARACTER_NUMBER = 400
MAX_CHARACTER_NUMBER = 20000

class SplitJsonStructure:
    __slots__ = (
        '_keys_structure',
        '_embedding_level',
        '_case_name',
        '_area'
    )
    _keys_structure: Dict
    _embedding_level: int
    _case_name: list
    _area: str

    def __init__(self, path: Path, name:str, important_path: list):
        
        self._keys_structure = {key: [] for key in keys}
        self._embedding_level = 0
        self._case_name = important_path + name.split('_')
        self._case_name = list(set(self._case_name))
        if 'schema' in self._case_name:
            schema_replace(path)

        with open(path, 'r') as f:
            data = json.load(f)
            self._split_data(data, self._case_name, name)
            self._area = 'common'
            # is_ul = is_ul_case(data["cells"])
            # is_dl = is_dl_case(data["cells"])
            # if is_ul and is_dl:
            #     self._area = 'common'
            # elif is_dl:
            #     self._area = 'dl'
            # elif is_ul:
            #     self._area = 'ul'

    def _split_data(self, data, features, name, father_key = None):
        if isinstance(data, list):
            for id, v in enumerate(data):
                current_feature = deepcopy(features)
                current_feature.append(id)
                value = 'str__' + json.dumps(v)
                if father_key is not None:
                    if not isinstance(v, list) or is_all_lists(v):
                    #     self._split_data(v, features, father_key)
                    # else:
                        # length = str(value).count(' ') + str(value).count('_') + str(value).count('-')
                        # if length < 100 and '{' in value:
                        k_v = json.dumps(father_key)
                        self._keys_structure['key'].append(k_v)
                        # self._keys_structure['key'].append(father_key)
                        
                        train_features = deepcopy(current_feature)
                        # train_features.reverse()
                        features_value = json.dumps(train_features)
                        self._keys_structure['feature'].append(features_value)
                        self._keys_structure['name'].append(name)
                        if isinstance(v, dict) and len(value) > MAX_CHARACTER_NUMBER:
                            store_value = 'str__' + json.dumps([key for key, _ in v.items()])
                            self._keys_structure['value_type'].append("key")
                            self._keys_structure['value'].append(store_value)
                        else:
                            self._keys_structure['value_type'].append("value")
                            self._keys_structure['value'].append(value)
                    else:
                        list_value = 'str__' + json.dumps(len(v))
                        k_v = json.dumps(father_key)
                        self._keys_structure['key'].append(k_v)
                        train_features = deepcopy(current_feature)
                        # train_features.reverse()
                        features_value = json.dumps(train_features)
                        self._keys_structure['feature'].append(features_value)
                        self._keys_structure['name'].append(name)
                        if len(value) > MAX_CHARACTER_NUMBER:
                            self._keys_structure['value_type'].append("list_len")
                            self._keys_structure['value'].append(list_value)
                        else:
                            self._keys_structure['value_type'].append("value")
                            self._keys_structure['value'].append(value)
                # if len(value) > MAX_CHARACTER_NUMBER:
                self._split_data(v, current_feature, name, father_key)

        elif isinstance(data, dict):
            for k, v in data.items():
                if "user_defined_model_config" in k or "sct_description" in k or v == None or v == [] or isinstance(v, int):
                    continue
                father_key = k
                current_feature = deepcopy(features)
                current_feature.append(k)
                if isinstance(v, list) and not is_all_lists(v):
                    str_v = 'str__' + json.dumps(v)
                    value = 'str__' + json.dumps(len(v))
                    k_v = json.dumps(k)
                    self._keys_structure['key'].append(k_v)
                    train_features = deepcopy(current_feature)
                    # train_features.reverse()
                    features_value = json.dumps(train_features)
                    self._keys_structure['feature'].append(features_value)
                    self._keys_structure['name'].append(name)
                    if len(str_v) > MAX_CHARACTER_NUMBER:
                        self._keys_structure['value_type'].append("list_len")
                        self._keys_structure['value'].append(value)

                        # self._split_data(v, current_feature, father_key)
                    else:
                        self._keys_structure['value_type'].append("value")
                        self._keys_structure['value'].append(str_v)

                    self._split_data(v, current_feature, name, father_key)
                else:
                    value = 'str__' + json.dumps(v)
                    # length = str(value).count(' ') + str(value).count('_') + str(value).count('-')
                    # if length < 100 and '{' in value:
                    k_v = json.dumps(k)
                    self._keys_structure['key'].append(k_v)
                    train_features = deepcopy(current_feature)
                    # train_features.reverse()
                    features_value = json.dumps(train_features)
                    self._keys_structure['feature'].append(features_value)
                    self._keys_structure['name'].append(name)
                    if isinstance(v, dict) and len(value) > MAX_CHARACTER_NUMBER:
                        store_value = 'str__' + json.dumps([key for key, _ in v.items()])
                        self._keys_structure['value_type'].append("key")
                        self._keys_structure['value'].append(store_value)
                    else:
                        self._keys_structure['value_type'].append("value")
                        self._keys_structure['value'].append(value)
                    # if isinstance(v, dict) and len(value) > MAX_CHARACTER_NUMBER:
                    if isinstance(v, dict):
                        self._split_data(v, current_feature, name, father_key)
                    else:
                        pass
    
    def _check_diff_type(self, search_data, match_data, value):
        # for data in search_data:
            # if data['father_key'] == match_data['father_key'] and \
            #    data['list_dim'] == match_data['list_dim']:
            #    data['subkeys'] == match_data['subkeys']:

        if search_data['subkeys'] != match_data['subkeys']:
            search_data['subkeys'] = list(set(search_data['subkeys'] + match_data['subkeys']))

        if is_in_list(value, search_data['value']):
            pass
        else:
            search_data['value'].append(value)

                
    def _collect_subdata(self, f_k, v):
        if isinstance(v, Dict):
            self._split_data(v, f_k)
        elif isinstance(v, list):
            for sub_v in v:
                self._collect_subdata(f_k, sub_v)

    @property
    def keys_structure(self):
        return self._keys_structure, self._area

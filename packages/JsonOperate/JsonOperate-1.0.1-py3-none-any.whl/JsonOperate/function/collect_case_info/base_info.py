from typing import Dict, List, Tuple, Set, Optional
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
from basic_define import OptionalWayOfCommpare, SupportChannel
from pkg_resources import resource_filename

import re

class BaseInfo:
    __slots__ = (
        '_way_of_compare',
        '_filter_data',
        '_source_data',
        '_field_file_name',
    )
    _way_of_compare: Set[OptionalWayOfCommpare]
    _filter_data: Dict
    _source_data: Optional
    _field_file_name: List[str]

    def __init__(self, way_of_compare: Set[OptionalWayOfCommpare], source_data: Optional, field_file_name: List[str]):
        self._way_of_compare = way_of_compare
        self._source_data = source_data
        self._field_file_name = field_file_name
        self._filter_data = {}

    def get_info(self) -> Dict:
        if OptionalWayOfCommpare.BaseConfig == self._way_of_compare:
            # print(f"base info use {self._way_of_compare} now")
            field_list = []
            for sub_field_file in self._field_file_name:
                field_list += self._get_field_from_file(SupportChannel['Common'], sub_field_file)

            set_field_list = set(field_list)
            for field in set_field_list:
                value = self.find_key_value(field, self._source_data)
                self._filter_data.update({field : value})
            return self._filter_data

        elif OptionalWayOfCommpare.CustomConfig == self._way_of_compare:
            pass
        else:
            pass

    def _get_field_from_file(self, channel:SupportChannel, sub_field_file:List[str]) -> List:
        field_file_name = sub_field_file[channel.value]

        field_list = []
        field_file = Path(resource_filename('collect_case_info', field_file_name)) 
        # print(f"path {field_file}")

        with open(field_file, 'r') as f:
            for field in f:
                field = re.sub(r'\n', "", field)
                field_list.append(field)

        return field_list

    def find_key_value(self, key, data):
        if isinstance(data, dict):
            result_dict = None
            for k,v in data.items():
                if key == k:
                    result_dict = v
                    return result_dict
                else:
                    result_dict = self.find_key_value(key, v)
                    if not (result_dict is None):
                        return result_dict

            return result_dict
        elif isinstance(data, list):
            result_list = []
            for id in range(len(data)):
                find_data = self.find_key_value(key, data[id])
                if not (find_data is None):
                    result_list.append(find_data)

            if len(result_list) == 0:
                return None
            else:
                return result_list
        else:
            return None
    
    def is_sub_list(self, little_list, big_list):
        for sub_little in little_list:
            if sub_little not in big_list:
                return 0
        return 1

    def get_necessary_path(self, field, necessary_paths):
        for necessary_path in necessary_paths:
            if field in necessary_path:
                return necessary_path
        return []

    def find_key_path_value(self, key, data, key_path, necessary_path):
        if isinstance(data, dict):
            result_dict = None
            for k,v in data.items():
                if key == k:
                    if k not in key_path:
                        key_path.append(k)
                    
                    if self.is_sub_list(necessary_path, key_path) and v != "":
                        # add this for distinguishing 1 and [1] in excel
                        if isinstance(v, list) and "[]" not in key_path:
                            if len(v) == 1:
                                v = [v]
                        result_dict = v

                        return result_dict, key_path
                else:
                    current_path = key_path[:]
                    current_path.append(k)
                    result_dict, sub_path = self.find_key_path_value(key, v, current_path, necessary_path)
                    if not (result_dict is None):
                        return result_dict, sub_path

            return result_dict, key_path
        elif isinstance(data, list):
            result_list = []
            result_path = []
            # if "[]" not in key_path:
            key_path.append("[]")
        
            for id in range(len(data)):
                find_data, sub_path = self.find_key_path_value(key, data[id], key_path, necessary_path)
                if not (find_data is None):
                    num_of_bracket = key_path.count('[]')
                    if num_of_bracket > 1:
                        index = 0
                        count = 0
                        for i, elem in enumerate(sub_path):
                            if elem == '[]':
                                count += 1
                            if count == 2:
                                index = i
                                break
                        result_path = sub_path[:index]
                        result_list = data
                    else:
                        result_list.append(find_data)
                        result_path = sub_path
            # else:
            #     print(f"key is {key} key_path is {key_path}, data is {data}")
            #     result_list = data
            #     result_path = key_path

            if len(result_list) == 0:
                return None, []
            else:
                return result_list, result_path
        else:
            return None, []

    def set_key_value(self, key, source_data, value, key_path, necessary_path):
        if isinstance(source_data, dict):
            for k,v in source_data.items():
                if key == k:
                    key_path.append(k)
                    # if 'prbs' in k:
                    #     print(f"key_path is {key_path} value is {value}")
                    necessary_path = [x for x in necessary_path if x != '[]']
                    if self.is_sub_list(necessary_path, key_path):
                        source_data[k] = value
                else:
                    current_path = key_path[:]
                    current_path.append(k)
                    self.set_key_value(key, v, value, current_path, necessary_path)
            return source_data
        elif isinstance(source_data, list):
            for id in range(len(source_data)):
                self.set_key_value(key, source_data[id], value, key_path, necessary_path)
            return source_data
        else:
            return source_data
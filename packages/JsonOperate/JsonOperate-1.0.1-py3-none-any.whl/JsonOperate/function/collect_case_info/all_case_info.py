import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
# from base_info import BaseInfo
# from basic_define import OptionalWayOfCommpare, SupportChannel
from typing import Dict, List, Tuple, Set, Optional, Union
# import pandas as pd
from JsonOperate.lib import panda_processing
# from case_manage.function.print_case_info.print_case_info import fill_path_index
def fill_path_index(key_path, index):
    return [key if key != "[]" else index for key in key_path]


class AllCaseInfo():
    __slots__ = (
        '_source_data',
        '_title',
        '_mode',
    )
    _source_data: Optional
    _title: str
    _mode: str

    def __init__(self, source_data: Optional, title: str, mode: str):

        self._source_data = source_data
        self._title = title
        self._mode = mode

    def sort_iterate_data(self) -> Dict:
        index = 0
        level = 0
        key_path = []
        result = panda_processing.default_panda()
        output_data = {}
        result, output_data = self.loop_data_in_level(self._source_data, index, key_path, level, result, output_data, self._title)
        
        # if self._title == "cells" or self._title == "users":
        #     result = panda_processing.head_cell_id(result)
        
        output_data.update({self._title: result})
        sorted_dict = dict(sorted(output_data.items()))

        return sorted_dict

    def loop_data_in_level(self, data, index, key_path, level, result, output_data, title):
        if isinstance(data, dict):
            for k,v in data.items():
                level_key_path = key_path[:]
                level_key_path.append(k)
                if isinstance(v, dict) or isinstance(v, list):
                    result, output_data = self.loop_data_in_level(v, index, level_key_path, level, result, output_data, title)
                else:
                    if self._mode == 'comp':
                        if self.check_valid_data(v):
                            result = panda_processing.add_data_to_panda(result, v, index, level_key_path, title)
                    else:
                        result = panda_processing.add_data_to_panda(result, v, index, level_key_path, title)
            return result, output_data
        elif isinstance(data, list):
            if any(isinstance(x, dict) for x in data):
                if level == 0 or len(data) == 1:
                    # if 'neighbors' in key_path:
                    #     print(f'title is {title} level is {level}, key_path is {key_path}, data is {data} len is {len(data)}')
                    '''remove the condition cells cause in cells title has this situation that has list data and it's len is 1 
                       e.g neighbors in HipTD_THOR_56_CAP6_FDD_32x4RX_10MHz_COMP.json '''
                    # if len(data) == 1 and title != "cells" and level != 0:
                    if len(data) == 1 and level != 0:
                        key_path.append(0)
                        # if 'neighbors' in key_path:
                        #     print(f'append 0 and new key_path is {key_path}')
                    else:
                        level += 1
                        key_path.append("[]")
                    
                    for list_index, sub_list in enumerate(data):
                        current_index = index if len(data) == 1 else list_index
                        result, output_data = self.loop_data_in_level(sub_list, current_index, key_path, level, result, output_data, title)
                else:
                    if self._mode == 'comp':
                        result = panda_processing.add_data_to_panda(result, data, index, key_path, title)
                    else:
                        sub_title = title + '_' + str(index)+ '_' + str(key_path[-1])
                        sub_index = 0
                        sub_level = 0
                        link_title = r'=HYPERLINK("#'+sub_title[-30:]+'!A3' + '\", \"' + "link_to_" + sub_title + '")'
                        result = panda_processing.add_data_to_panda(result, link_title, index, key_path, title)
                        key_path = fill_path_index(key_path,index)
                        sub_result = panda_processing.default_panda()
                        sub_result, output_data = self.loop_data_in_level(data, sub_index, key_path, sub_level, sub_result, output_data, sub_title)
                        output_data.update({sub_title:sub_result})
            else:

                result = panda_processing.add_data_to_panda(result, data, index, key_path, title)

            return result, output_data
        else:
            result = panda_processing.add_data_to_panda(result, data, index, key_path, title)
            return result, output_data

    def check_valid_data(self, data):
        if data != None and data != "":
            return True
        else:
            return False

    def accumulate_data_to_one_index(result, v, k):
        return result.update({k:v})


        
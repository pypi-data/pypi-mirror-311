#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
# from base_info import BaseInfo
# from cell_info import CellInfo
# from user_info import UserInfo
from all_case_info import AllCaseInfo
# from basic_define import OptionalWayOfCommpare
from pathlib import Path
from typing import Dict, List, Set, Optional, Union
import json
# from copy import deepcopy
# from case_manage.lib.panda_processing import merge_df

# from compareCase import compare

class CollectCaseInfo:
    __slots__ = (
        '_base_data',
        '_cell_data',
        '_user_data',
        # '_cell_user_data',
        # '_cell_number',
        # '_cell_id',
        # '_channel_info',
        # '_standard',
    )
    _base_data: Dict
    _cell_data: Optional
    _user_data: Optional
    # _cell_user_data: Dict
    # _cell_number: int
    # _cell_id: List
    # _channel_info: Set
    # _standard: List

    def __init__(self, path: Path):
        pass
        # with open(path, 'r') as f:
        #     data = json.load(f)
        #     # need to change to for cell
        #     # cells = data["cells"]
        #     # field_cases, field_cells, field_ues = self.get_field_files(cells)
        #     # source_data = data["sct_configuration"]
        #     source_data = data
        #     current_base_info = BaseInfo(OptionalWayOfCommpare.BaseConfig, source_data, list(field_cases))
        #     self._base_data = current_base_info.get_info()
            # print(f"get result base {self._base_data}")
            
            # source_data = data["cells"]
            # current_cell_info = CellInfo(OptionalWayOfCommpare.BaseConfig, source_data, list(field_cells))
            # self._cell_data = current_cell_info.get_info()
            # self._cell_number = current_cell_info.get_cell_number()
            # self._cell_id = current_cell_info._subcell_id
            # # print(f"get result cell {self._cell_data}")
            # self._standard = source_data[0]["standard"]

            # source_data = data["users"]
            # current_user_info = UserInfo(OptionalWayOfCommpare.BaseConfig, source_data, list(field_ues), current_cell_info._subcell_id)
            # self._user_data, self._channel_info = current_user_info.get_info()
            # print(f"get result user {self._user_data}")

    # def get_field_files(self, source_data: Optional):
    #     field_cases = []
    #     field_cells = []
    #     field_ues = []
    #     for cell in source_data:
    #         standard = cell["standard"]
    #         field_case =  ["field_case_lte.txt"] if standard == "LTE" else ["field_case.txt"]
    #         field_cell =  ["field_cell_lte.txt"] if standard == "LTE" else ["field_cell.txt"]
    #         field_ue = ["field_ue_lte_common.txt","field_ue_lte_prach.txt","field_ue_lte_pucch.txt","field_ue_lte_pusch.txt","field_ue_lte_srs.txt"] \
    #             if standard == "LTE" else ["field_ue_common.txt","field_ue_prach.txt","field_ue_pucch.txt","field_ue_pusch.txt","field_ue_srs.txt"]

    #         if not self.get_data_in_list(field_case, field_cases):
    #             field_cases.append(field_case)
    #         if not self.get_data_in_list(field_cell, field_cells):
    #             field_cells.append(field_cell)
    #         if not self.get_data_in_list(field_ue, field_ues):
    #             field_ues.append(field_ue)
    #         # if not self.get_data_in_list(standard, self._standard):
    #         #     self._standard.append(standard)

    #     return field_cases, field_cells, field_ues

    # def get_data_in_list(self, data: Optional, list: List):
    #     for sub in list:
    #         if data == sub:
    #             return 1
    #     return 0

    def get_base_data(self):
        return self._base_data

    def get_cell_data(self):
        return self._cell_data
    
    def get_user_data(self):
        return self._user_data
    
    # def get_cell_user_data(self):
    #     return self._cell_user_data

    # def get_cell_number(self):
    #     return self._cell_number

    # def get_cell_id(self):
    #     return self._cell_id

    # def get_channel_info(self):
    #     return self._channel_info

    # def get_standard(self):
    #     return self._standard

# class CollectCustomCaseInfo(CollectCaseInfo):
#     def __init__(self, path: Path,  custom_cell_id: int, custom_rnti: int):
#         with open(path, 'r') as f:
#             data = json.load(f)
#             cells = data["cells"]
#             field_cases, field_cells, field_ues = self.get_field_files(cells)
#             source_data = data["sct_configuration"]
#             current_base_info = BaseInfo(OptionalWayOfCommpare.BaseConfig, source_data, field_cases)
#             self._base_data = current_base_info.get_info()
#             # print(f"get result base {self._base_data}")

#             source_data = data["cells"]
#             current_cell_info = CellInfo(OptionalWayOfCommpare.BaseConfig, source_data, field_cells)
#             self._cell_data = current_cell_info.get_info(custom_cell_id)
#             self._cell_number = current_cell_info.get_cell_number()
#             # print(f"get custom result cell {self._cell_data}")
#             self._standard = source_data[0]["standard"]

#             source_data = data["users"]
#             current_user_info = UserInfo(OptionalWayOfCommpare.BaseConfig, source_data, field_ues, current_cell_info._subcell_id)
#             self._user_data, self._channel_info = current_user_info.get_info(custom_rnti)
            # print(f"get custom result user {self._user_data}")
    
# class CollectCaseInfoForExcelModify(CollectCaseInfo):
#     def __init__(self, path: Path):
#         with open(path, 'r') as f:
#             data = json.load(f)
#             # need to change to for cell
#             cells = data["cells"]
#             field_cases, field_cells, field_ues = self.get_field_files(cells)
#             # source_data = data["sct_configuration"]
#             # current_base_info = BaseInfo(OptionalWayOfCommpare.BaseConfig, source_data, list(field_cases))
#             # self._base_data = current_base_info.get_info()
#             # print(f"get result base {self._base_data}")
            
#             source_data = data["cells"]
#             current_cell_info = CellInfo(OptionalWayOfCommpare.BaseConfig, source_data, list(field_cells))
#             self._cell_data = current_cell_info.get_panda_cell_info()
#             self._cell_number = current_cell_info.get_cell_number()
#             self._cell_id = current_cell_info._subcell_id

#             # print(f"get result cell {self._cell_data}")
#             # self._standard = source_data[0]["standard"]

#             source_data = data["users"]
#             current_user_info = UserInfo(OptionalWayOfCommpare.BaseConfig, source_data, list(field_ues), current_cell_info._subcell_id)
#             self._user_data = current_user_info.get_panda_user_info()
#             # print(f"get result user {self._user_data}")

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

# def is_nr_case(cell_infos):
#     for cell_info in cell_infos:
#         if cell_info["standard"] == 'NR':
#             return True
#     return False

# def is_lte_case(cell_infos):
#     for cell_info in cell_infos:
#         if cell_info["standard"] == 'LTE':
#             return True
#     return False

# def is_test_ability(data):
#     if data["sct_configuration"]["snapshot_configuration"]:
#         return True
#     return False
    
class CollectAllCaseInfo(CollectCaseInfo):
    __slots__ = (
        '_mode',
        '_area'
    )
    _mode: str
    _area: str

    def __init__(self, path: Path, mode: str='normal'):
        with open(path, 'r') as f:
            data = json.load(f)
            
            source_data = data["cells"]
            current_cell_info = AllCaseInfo(source_data, "cells", mode)
            self._cell_data = current_cell_info.sort_iterate_data()

            source_data = data["users"]
            current_user_info = AllCaseInfo(source_data, "users", mode)
            self._user_data = current_user_info.sort_iterate_data()
            
            # # if mode == 'comp':
            # #     df_cell = deepcopy(self._cell_data["cells"])
            # #     df_user = deepcopy(self._user_data["users"])
            # #     self._cell_user_data = {"cell_user":merge_df(df_cell, df_user)}
            # #     is_ul = is_ul_case(data["cells"])
            # #     is_dl = is_dl_case(data["cells"])
            # #     if is_test_ability(data):
            # #         self._area = 'test_ability'
            # #     elif is_ul and is_dl:
            # #         self._area = 'common'
            # #     elif is_dl:
            # #         self._area = 'dl'
            # #     elif is_ul:
            # #         self._area = 'ul'
            # #     else:
            # #         print(f"this case has an undefined area, please check the config {path}")

            # #     if self._area == 'dl' or self._area == 'ul':
            # #         is_lte = is_lte_case(data["cells"])
            # #         is_nr = is_nr_case(data["cells"])
            # #         if is_lte and is_nr:
            # #             self._area = 'common'
            # #         elif is_lte:
            # #             self._area += '_lte'
            # #         elif is_nr:
            # #             self._area += '_nr'
            # #         else:
            # #             print(f"this case has an error standard, please check the config {path}")
            # # else:
            # #     self._area = 'unknown'
            
            data["cells"] = None
            data["users"] = None
            source_data = data
            current_cell_info = AllCaseInfo(source_data, "basic_info", mode)
            self._base_data = current_cell_info.sort_iterate_data()

    # def get_case_area(self):
    #     return self._area

# class ReferenceCustomCaseInfo(CollectCaseInfo):
#     def __init__(self, path: Path,  field_cells: List, field_ues: List, custom_cell_id: int, custom_rnti: int, necessary_paths: List):
#         with open(path, 'r') as f:
#             data = json.load(f)

#             source_data = data["cells"]
#             current_cell_info = CellInfo(OptionalWayOfCommpare.BaseConfig, source_data, field_cells)
#             self._cell_data = current_cell_info.get_exclude_info(custom_cell_id, field_cells, necessary_paths)

#             source_data = data["users"]
#             current_user_info = UserInfo(OptionalWayOfCommpare.BaseConfig, source_data, field_ues, custom_cell_id)
#             self._user_data = current_user_info.get_exclude_info(custom_cell_id, custom_rnti, field_ues, necessary_paths)

# class ReferenceAddCustomCaseInfo(CollectCaseInfo):
#     def __init__(self, path: Path, custom_cell_id: int, custom_rnti: int):
#         with open(path, 'r') as f:
#             data = json.load(f)

#             source_data = data["cells"]
#             current_cell_info = CellInfo(OptionalWayOfCommpare.BaseConfig, source_data, [])
#             self._cell_data = current_cell_info.get_total_info(custom_cell_id)

#             source_data = data["users"]
#             current_user_info = UserInfo(OptionalWayOfCommpare.BaseConfig, source_data, [], None)
#             self._user_data = current_user_info.get_total_info(custom_rnti)
#             # if self._cell_data == None or self._user_data == None:
#             #     print(f"check your cell id or rnti can't get this cell info or user info")

# class ReplaceCustomCaseInfo(CollectCaseInfo):

#     def __init__(self, path: Path,  field_cells: List, field_ues: List, custom_cell_ids: Union[List, None], custom_rntis: List, replace_value:Dict, necessary_paths: List):
#         with open(path, 'r') as f:
#             data = json.load(f)

#             source_data = data["cells"]
#             current_cell_info = CellInfo(OptionalWayOfCommpare.BaseConfig, source_data, field_cells)
#             data["cells"] = current_cell_info.set_exclude_info(custom_cell_ids, field_cells, replace_value, necessary_paths)

#             source_data = data["users"]
#             current_user_info = UserInfo(OptionalWayOfCommpare.BaseConfig, source_data, field_ues, custom_cell_ids)
#             data["users"] = current_user_info.set_exclude_info(custom_cell_ids, custom_rntis, field_ues, replace_value, necessary_paths)
#         with open(path, 'w') as f:
#             json.dump(data, f, indent=4)
        

# class AddCustomCaseInfo(CollectCaseInfo):

#     def __init__(self, path: Path,  cell_number: int, user_number: int, cell_step_fields: List, user_step_fields: List,
#                  cell_section_fields: List, user_section_fields: List, cell_loop_fields: List, user_loop_fields: List,
#                  add_cell_value: List, add_user_value: List):
#         with open(path, 'r') as f:
#             data = json.load(f)

#             for id in range(cell_number):
#                 field_list, current_value = self.get_variable_field_data(id, cell_step_fields, cell_section_fields, cell_loop_fields)

#                 current_cell_info = CellInfo(OptionalWayOfCommpare.BaseConfig, add_cell_value, field_list)
#                 current_cell_data = current_cell_info.set_exclude_info(None, field_list, current_value, [])
#                 # print(f"current_cell_data is {current_cell_data}")
#                 data["cells"] += deepcopy(current_cell_data)

#             # source_data = data["users"]
#             for id in range(user_number):
#                 field_list, current_value = self.get_variable_field_data(id, user_step_fields, user_section_fields, user_loop_fields)
#                 current_user_info = UserInfo(OptionalWayOfCommpare.BaseConfig, add_user_value, field_list, None)
#                 current_user_data = current_user_info.set_exclude_info(None, [], field_list, current_value, [])
#                 data["users"] += deepcopy(current_user_data)
#         with open(path, 'w') as f:
#             json.dump(data, f, indent=4)

#     def get_variable_field_data(self, id, step_fields, section_fields, loop_fields):
#         field_list = []
#         current_value = {}
#         for step_field in step_fields:
#             field_list.append(step_field[0])  # input format [field,stard,end,step]
#             value = int(step_field[3]) * id + int(step_field[1])
#             current_value.update({step_field[0] : value})
#         for section_field in section_fields:
#             field_list.append(section_field[0])
#             value = self.find_section_value(id,section_field)
#             current_value.update({section_field[0] : value})
#         for loop_field in loop_fields:
#             field_list.append(loop_field[0])
#             value = self.find_loop_value(id,loop_field)
#             current_value.update({loop_field[0] : value})
        
#         return field_list, current_value

#     def find_section_value(self, id :int, section_field: List):
#         # input format [field,stard-id1,end-id1,type1,value1,stard-id2,end-id2,type2,value2...]
#         field_len = len(section_field) - 1
#         section_number = int(field_len / 4)
#         value = None
#         for section_id in range(section_number):
#             start_id = int(section_field[section_id * 4 + 1])
#             end_id = int(section_field[section_id * 4 + 2])
#             if (id + 1) >= start_id and (id + 1) <= end_id:
#                 value = section_field[section_id * 4 + 4]
#                 field_type = section_field[section_id * 4 + 3]
#                 if field_type == 'int':
#                     value = int(value)
#                 if field_type == 'listfloat':
#                     value = float(value)
#                     value = [value]
#                 return value
#         return value

#     def find_loop_value(self, id :int, loop_field: List):
#         # input format [field,type,value1,value2,value3...]
#         field_len = len(loop_field) - 2
#         loop_id = int(id % field_len)
#         value = loop_field[loop_id + 2]
#         field_type = loop_field[1]
#         if field_type == 'int':
#             value = int(value)
#         if field_type == 'listfloat':
#             value = float(value)
#             value = [value]
#         return value
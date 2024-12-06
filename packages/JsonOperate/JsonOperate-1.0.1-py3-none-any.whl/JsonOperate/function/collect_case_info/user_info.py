
# from base_info import BaseInfo
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
from cell_info import CellInfo
from basic_define import OptionalWayOfCommpare, SupportChannel
from typing import Dict, List, Tuple, Set, Optional, Union
from case_manage.lib import panda_processing

channels_str = ['common','prach','pucch','pusch','srs']
channels_header = ['common_','prach_','pucch_','pusch_','srs_']

class UserInfo(CellInfo):
    __slots__ = (
        '_subcell_id',
        '_channel_info',
    )
    _subcell_id: List[int]
    _channel_info: List

    def __init__(self, way_of_compare: Set[OptionalWayOfCommpare], source_data: Optional, field_file_name: List[str], subcell_id: List[int]):
        super().__init__(way_of_compare, source_data, field_file_name)
        self._subcell_id = subcell_id
        self._channel_info = []

    def get_info(self, rnti: int = 0) -> Dict:
        if OptionalWayOfCommpare.BaseConfig == self._way_of_compare:
            # print(f"user use {self._way_of_compare} now")
            
            for channel in SupportChannel:
                self._filter_data.update(self._get_channel_info(channel, rnti))
            
            return self._filter_data, set(self._channel_info)

    def get_panda_user_info(self) -> Dict:
        field_list = []
        necessary_paths = []
        total_user_info = []
        # users = self._source_data
        # print(f"self._field_file_name is {self._field_file_name}")
        for channel in SupportChannel:
            for sub_field_file in self._field_file_name:
                current_field_list = self._get_field_from_file(channel, sub_field_file)
                field_list += current_field_list
            # print(f"current_field_list is {current_field_list}")
            if channel == SupportChannel['Common']:
                necessary_paths = current_field_list
            else:
                necessary_paths += [channels_str[channel.value] for i in range(len(current_field_list))]

        for cell_id in self._subcell_id:
            sorted_users = self._filter_data_by_cellid(self._source_data, cell_id)
            df_list = []
            
            for user in sorted_users:
                temp_dict = {}

                for field, necessary_path in zip(field_list, necessary_paths):
                    path = []
                    value, path = self.find_key_path_value(field, user, path, [necessary_path])
                    temp_dict.update({str(path) : value})
                
                index_name = "user_" + str(user["rnti"])
                df = panda_processing.convert_dict_to_panda(temp_dict, index_name)
                df_list.append(df)
            user_data_in_one_cell = panda_processing.panda_concat(df_list, 0)
            total_user_info.append(user_data_in_one_cell) 
        return total_user_info

    def _get_channel_info(self, channel:SupportChannel, rnti: int = 0):
        channel_data = {}
        field_list = []
        for sub_field_file in self._field_file_name:
            field_list += self._get_field_from_file(channel, sub_field_file)
            
        # field_list = self._get_field_from_file(channel)
        set_field_list = set(field_list)
        sorted_users = self._filter_data_by_cellid(self._source_data, None)
        cell_number = len(self._subcell_id)
        for field in set_field_list:
            same_cell_value = [[]for i in range(cell_number)]
            
            for user in sorted_users:
                user_rnti = self.find_key_value('rnti', user)
                tar = self.find_key_value(channel.name, user)
                if user["standard"] == "LTE":
                    cell_id = self.find_key_value("ln_cell_id", user)
                else:
                    cell_id = self.find_key_value("subcell_id", user)
                if (tar or channel == SupportChannel['Common']) and (user_rnti == rnti or rnti == 0):
                    search_data = user if channel == SupportChannel['Common'] else user['uplink'][channel.name]
                    value = self.find_key_value(field, search_data)
                    cell_index = self._get_list_index(self._subcell_id, int(cell_id))
                    # print(f" list subcell_id {self._subcell_id} curr cellid {cell_id} result {cell_index}")
                    if cell_index < cell_number:
                        same_cell_value[cell_index].append(value)
                    # channelType means have lte coresponse ue, need add relative cell info compare
                    # alloc_slot means have NR srs and pucch ue, prb_occasion_index means have nr prach ue, mcs_index indicate nr pusch
                    if field == 'channelType' or field == 'alloc_slot' or field == 'prb_occasion_index' or field == 'mcs_index':
                        self._channel_info.append(channels_header[channel.value])
            new_field = channels_header[channel.value] + field
            channel_data.update({new_field : same_cell_value})

        return channel_data

    def get_total_info(self, rnti:int) -> Union[Dict,None]:
        
        users = self._source_data

        for user in users:
            if user["rnti"] == rnti:
                return user

        return None

    def get_exclude_info(self, cell_id:int, rnti:int, fields:List, necessary_paths:List) -> Dict:
        
        users = self._source_data

        for user in users:
            if user["rnti"] != rnti:
                continue
            for field in fields:
                necessary_path = self.get_necessary_path(field, necessary_paths)
                path = []
                value, path = self.find_key_path_value(field, user, path, necessary_path)
                field_path = field + '_path'
                self._filter_data.update({field : value})
                self._filter_data.update({field_path : path})
            break

        return self._filter_data

    def set_exclude_info(self, cell_ids, rntis:List, fields:List, values:dict, necessary_paths:List) -> Dict:
        
        users = self._source_data

        for user in users:
            # if user["standard"] == "LTE":
            #     my_cell_id = user["uplink"]["ln_cell_id"]
            # else:
            #     my_cell_id = user["uplink"]["subcell_id"]

            # print(f"my_cell_id is {my_cell_id}, cell_ids is {cell_ids}")

            # if my_cell_id not in cell_ids and cell_ids != []:
            #     continue

            if user["rnti"] not in rntis and rntis != []:
                continue

            for field in fields:
                necessary_path = self.get_necessary_path(field, necessary_paths)
                path = []
                # print(f"field is {field}, value is {values[field]}, nessary_path is {necessary_path}")
                self.set_key_value(field, user, values[field], path, necessary_path)

        return self._source_data

    def _get_list_index(self, list_data:List[int], match_data:int):
        index = 0
        for data in list_data:
            if match_data == data:
                break
            else:
                index += 1
        return index

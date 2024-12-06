import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
from base_info import BaseInfo
from basic_define import OptionalWayOfCommpare, SupportChannel
from typing import Dict, List, Tuple, Set, Optional, Union
import pandas as pd
from case_manage.lib import panda_processing

class CellInfo(BaseInfo):
    __slots__ = (
        '_subcell_id',
    )
    _subcell_id: List

    def __init__(self, way_of_compare: Set[OptionalWayOfCommpare], source_data: Optional, field_file_name: List[str]):
        super().__init__(way_of_compare, source_data, field_file_name)
        # print(f"field_file_name is {field_file_name}")
        self._subcell_id = []

    def get_info(self, cell_id = None) -> Dict:
        if OptionalWayOfCommpare.BaseConfig == self._way_of_compare:
            # print(f"cell use {self._way_of_compare} now")
            field_list = []
            for sub_field_file in self._field_file_name:
                field_list += self._get_field_from_file(SupportChannel['Common'], sub_field_file)

            set_field_list = set(field_list)

            sorted_cells = self._filter_data_by_cellid(self._source_data, cell_id)
            self._subcell_id = self._collect_cellid(self._source_data, cell_id)

            for field in set_field_list:
                values = []
                for cell in sorted_cells:
                    value = self.find_key_value(field, cell)
                    values.append(value)
                    self._filter_data.update({field : values})

            return self._filter_data

    def get_total_info(self, cell_id:int) -> Union[Dict,None]:
        
        cells = self._source_data

        for cell in cells:
            if cell["uplink"] and ('ln_cell_id' in cell["uplink"].keys() or 'subcell_id' in cell["uplink"].keys()):
                if cell["standard"] == "LTE":
                    loop_cell_id = cell["uplink"]["ln_cell_id"]
                else:
                    loop_cell_id = cell["uplink"]["subcell_id"]
            if loop_cell_id == cell_id:
                return cell

        return None

    def get_panda_cell_info(self) -> Dict:
        field_list = []
        for sub_field_file in self._field_file_name:
            field_list += self._get_field_from_file(SupportChannel['Common'], sub_field_file)

        set_field_list = set(field_list)

        sorted_cells = self._filter_data_by_cellid(self._source_data, None)
        self._subcell_id = self._collect_cellid(self._source_data, None)
        df_list = []
        for cell_id, cell in enumerate(sorted_cells):

            for field in set_field_list:
                path = []
                value, path = self.find_key_path_value(field, cell, path, [field])

                self._filter_data.update({str(path) : value})

            index_name = "cell_" + str(self._subcell_id[cell_id])
            df = panda_processing.convert_dict_to_panda(self._filter_data, index_name)
            df_list.append(df)
        df_result = panda_processing.panda_concat(df_list, 0)
        return df_result

    def get_exclude_info(self, cell_id:int, fields:List, necessary_paths:List) -> Dict:
        
        cells = self._source_data

        for cell in cells:
            if cell["uplink"] and ('ln_cell_id' in cell["uplink"].keys() or 'subcell_id' in cell["uplink"].keys()):
                if cell["standard"] == "LTE":
                    loop_cell_id = cell["uplink"]["ln_cell_id"]
                else:
                    loop_cell_id = cell["uplink"]["subcell_id"]

            if loop_cell_id != cell_id:
                continue
            for field in fields:
                necessary_path = self.get_necessary_path(field, necessary_paths)

                path = []
                value, path = self.find_key_path_value(field, cell, path, necessary_path)
                field_path = field + '_path'
                self._filter_data.update({field : value})
                self._filter_data.update({field_path : path})
            break

        return self._filter_data

    def set_exclude_info(self, cell_ids, fields:List, values:dict, necessary_paths:List) -> Dict:

        cells = self._source_data
        # print(f"cells is {cells}")
        for cell in cells:
            
            if cell["uplink"] and ('ln_cell_id' in cell["uplink"].keys() or 'subcell_id' in cell["uplink"].keys()):
                if cell["standard"] == "LTE":
                    loop_cell_id = cell["uplink"]["ln_cell_id"]
                else:
                    loop_cell_id = cell["uplink"]["subcell_id"]
        
            if cell_ids != None:
                if loop_cell_id not in cell_ids:
                    continue

            for field in fields:
                necessary_path = self.get_necessary_path(field, necessary_paths)
                path = []
                value = self.set_key_value(field, cell, values[field], path, necessary_path)

        return self._source_data

    def get_cell_number(self) -> int:
        return len(self._subcell_id)

    def get_cell_id(self) -> List:
        return self._subcell_id

    def _filter_data_by_cellid(self, source_data: Optional, cell_id) -> Optional:
        filter_data_lte = []
        filter_data_nr = []
        sorted_data_lte = []
        sorted_data_nr = []

        for data in source_data:
            if data["uplink"] and ('ln_cell_id' in data["uplink"].keys() or 'subcell_id' in data["uplink"].keys()):
                if data["standard"] == "LTE":

                    if cell_id == None or data["uplink"]["ln_cell_id"] == cell_id:
                        filter_data_lte.append(data)
                else:
                    if cell_id == None or data["uplink"]["subcell_id"] == cell_id:
                        filter_data_nr.append(data)


        if filter_data_nr:
            sorted_data_nr = sorted(filter_data_nr, key=lambda k: (k["uplink"]["subcell_id"]), reverse=False)
        if filter_data_lte:
            sorted_data_lte = sorted(filter_data_lte, key=lambda k: (k["uplink"]["ln_cell_id"]), reverse=False)

        return sorted_data_lte + sorted_data_nr

    def _collect_cellid(self, cells: Optional, cell_id) -> List:
        filter_cellid_lte = []
        filter_cellid_nr = []
        sorted_cellid_lte = []
        sorted_cellid_nr = []

        for cell in cells:
            if cell["uplink"] and ('ln_cell_id' in cell["uplink"].keys() or 'subcell_id' in cell["uplink"].keys()):
                if cell["standard"] == "LTE":
                    if (cell_id == None or cell["uplink"]["ln_cell_id"] == cell_id):
                        filter_cellid_lte.append(int(cell["uplink"]["ln_cell_id"]))
                else:
                    if cell_id == None or cell["uplink"]["subcell_id"] == cell_id:
                        filter_cellid_nr.append(int(cell["uplink"]["subcell_id"]))

        if filter_cellid_nr:
            sorted_cellid_nr = sorted(filter_cellid_nr)
        if filter_cellid_lte:
            sorted_cellid_lte = sorted(filter_cellid_lte)

        return sorted_cellid_lte + sorted_cellid_nr
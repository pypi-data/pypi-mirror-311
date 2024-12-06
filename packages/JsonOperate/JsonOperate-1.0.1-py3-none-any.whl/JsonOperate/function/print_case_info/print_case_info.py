#!/usr/bin/env python3

from typing import Dict, List, NamedTuple
from pathlib import Path
import re
import os
from JsonOperate.function.collect_case_info.collect_case_info import CollectAllCaseInfo
from JsonOperate.lib.panda_processing import add_lable
from JsonOperate.lib.output import PrintCaseInfoOutputByPanda

class PrintPath:
    json_path: Path
    excel_path: Path
    def __init__(self, json_path, excel_path):
        self.json_path = json_path
        self.excel_path = excel_path

def get_name_path(base_path: Path, file:str):
    target_name = re.sub(r'.json| |\n', "", file)
    json_path = os.path.join(base_path, file)
    excel_name = re.sub(r'.json| |\n', ".xlsx", file)
    excel_path = os.path.join(base_path, excel_name)
    path = PrintPath(json_path, excel_path)
    return target_name, path

def get_target_info_from_file(base_path: Path, file:str, arguments):

    target_name, path = get_name_path(base_path, file)

    return {
        "name": target_name,
        "path": path
    }

def output_to_excel(output: Path, data: Dict):
    excel_output = PrintCaseInfoOutputByPanda(output, 1)
    with excel_output as excel:
        sort_data_to_excel(excel, data)

def sort_data_to_excel(excel, data: Dict):
    for k, v in data.items():
        excel_sheet_name = k[-30:]
        excel.add_new_sheet(excel_sheet_name)
        excel.data_output(v, 0)

class PrintCaseInfo():
    __slots__ = (
        '_target_info',
        '_area',
    )

    def __init__(self, target_info) -> None:
        self._target_info = target_info
        self._area = 'unknown'

    def sort_data(self) -> Dict:
        path = self._target_info["path"].json_path
        
        tar_collect = CollectAllCaseInfo(path)
        basic_info = tar_collect.get_base_data()
        # print(f"basic_info is {basic_info}")
        detail_cell_info = tar_collect.get_cell_data()
        detail_user_info = tar_collect.get_user_data()
        basic_info.update(detail_cell_info)
        basic_info.update(detail_user_info)
        return basic_info

    def get_output_path(self) -> Path:
        return self._target_info["path"].excel_path
    
    def get_case_area(self) -> str:
        return self._area
    

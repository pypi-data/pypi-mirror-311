#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Dict, List, Union, Mapping, Optional
from pkg_resources import resource_filename

_CPRI_RELATIVE_PATH = 'fronthaul/cpri'
_ECPRI_RELATIVE_PATH = 'fronthaul/ecpri'

def _is_list_name_in_file(file_name:str, file_path: str) -> int:
    with open(file_path, "r") as f:
        for line in f:
            line = re.sub(r' - | |\n|\r', "", line)
            if line == file_name:
                return 1
            # elif file_name in line:
            #     print(f"line is {line} file_name is {file_name}")
            # else:
            #     pass
    return 0

class TargetElement:
    __slots__ = (
        '_py_path_list',
        '_x86_path_list',
        '_hw_path_list',
        '_function_name',
        '_target_name',
        '_team_info',
    )
    _py_path_list: List[Path]
    _x86_path_list: List[Path]
    _hw_path_list: List[Path]
    _function_name: List[str]
    _team_info: List[str]
    _target_name: str

    def __init__(self, target: str) -> None:
        self._py_path_list = []
        self._x86_path_list = []
        self._hw_path_list = []
        self._function_name = []
        self._target_name = target
        self._team_info = []

class FindList:
    __slots__ = (
        '_path',
        '_ci_list_path',
        '_board',
        '_source',
        '_target_element',
        '_sct_job_path',
    )
    _path: Path
    _ci_list_path: Path
    _board: str
    _source: str
    _target_element: List[TargetElement]
    _sct_job_path: Path

    def __init__(self, path: Path, ci_list_path: Path, board: str, source: str, sct_job_path: Path = '') -> None:
        self._path = path
        self._board = board
        self._ci_list_path = ci_list_path
        self._source = source
        self._target_element = []
        self._sct_job_path = sct_job_path
        print(f"sct_job_path is {sct_job_path}")

    def create_target(self, target_name: str) -> TargetElement:
        return TargetElement(target_name)

    def find_case_name_in_py(self, target_element: TargetElement, sub_path: Path = "") -> None:
        find_case_files = os.listdir(self._path)
        py_path_fh_ecpri = os.path.join(self._path, _ECPRI_RELATIVE_PATH)
        py_path_fh_cpri = os.path.join(self._path, _CPRI_RELATIVE_PATH)
        py_path_fh_ecpri_files = os.listdir(py_path_fh_ecpri)
        py_path_fh_cpri_files = os.listdir(py_path_fh_cpri)
        # case_list_path = os.path.join(self._path, find_case_file)
        # case_list_path_ec =  os.path.join(py_path_fh_ecpri, find_case_file)
        # case_list_path_c =  os.path.join(py_path_fh_cpri, find_case_file)
        base_paths = [self._path] * len(find_case_files) + [py_path_fh_ecpri] * len(py_path_fh_ecpri_files) + [py_path_fh_cpri] * len(py_path_fh_cpri_files)
        # print(f"base_path is {base_paths}")

        find_case_files += py_path_fh_ecpri_files
        find_case_files += py_path_fh_cpri_files
        
        target_name = re.sub(r'.json', "", target_element._target_name)
        function_name_counter = -1
        for find_case_file, base_path in zip(find_case_files, base_paths):
            # print(f"file name is {find_case_file}, target_name is {target_name} base_path is {base_path}")
            if '.py' not in find_case_file:
                continue
            # print(f"file name is {find_case_file}, target_name is {target_name}")

            case_list_path = os.path.join(base_path, find_case_file)
            search_board = re.search(self._board, find_case_file, re.M|re.I)
            search_fh = re.search('fh', find_case_file, re.M|re.I)
            if (not (search_board or search_fh)) and self._board == "thor":
                continue
            function_name = ""
            team_info = ''
            pre_line = ''
            find_target_name = 0
            with open(case_list_path, "r") as f:
                for line in f:
                    # if '/lte/' in self._path:
                    #     target_name1 = re.sub(r'HipTD_TRX_', "", target_name)
                    #     target_name2 = re.sub(r'HipTD_', "", target_name)
                    #     line = re.sub('        vector = "', "", line)
                    #     line = re.sub(r'"\s', "", line)

                    #     if line == target_name1 or target_name2 == line:
                    #         function_name = re.sub(r'    def |\(.*\):| |\n', "", pre_line)
                    #         target_element._function_name.append(function_name)
                    #         target_element._team_info = team_info
                    #         function_name_counter += 1
                    #         target_element._py_path_list.append(find_case_file)
                    #         # print("function_name",function_name)
                    #         break
                    #     if '    def ' in line:
                    #         pre_line = line
                    # else:
                    matchObj = re.findall(r'\'([^\']*).json\'', line, re.M|re.I)
                    if matchObj:
                        if matchObj[0] == target_name:
                            # print(f" line is {line}")
                            find_target_name = 1
                            function_name_counter += 1

                    if 'def ' in line and find_target_name:
                        function_name = re.sub(r'def |\(.*| |\n', "", line)
                        target_element._function_name.append(function_name)
                        target_element._team_info.append(team_info)
                        find_target_name = 0
                        target_element._py_path_list.append(find_case_file)
                    if 'mark.team(' in line:
                        team_info = re.sub(r'@pytest.mark.team\(|\)| |#.*', "", line)
                        # team_info = re.sub(r'\)', "", line)                

    def find_function_name_list(self, target_element: TargetElement) -> None:
        if not target_element._function_name:
            return
        x86_list = [[] for i in range(len(target_element._function_name))]
        hw_list = [[] for i in range(len(target_element._function_name))]
        find_case_files = os.listdir(self._ci_list_path)
        for find_case_file in find_case_files:
            case_list_path = os.path.join(self._ci_list_path, find_case_file)
            search_x86 = re.search("clang", find_case_file , re.M|re.I)
            search_hw = re.search("hw|abio|abip|abin|asoe|asof|asog", find_case_file , re.M|re.I)
            search_board = re.search(self._board, find_case_file, re.M|re.I)
            search_fh = re.search("fh", find_case_file, re.M|re.I)

            if not ((search_board or search_fh) and (search_x86 or search_hw)):
                continue
            
            with open(case_list_path, "r") as f:
                for line in f:
                    key_value = re.sub(r'.*::.*::| |\n', "", line)
                    for function_name in enumerate(target_element._function_name,  start=0):
                        # print(f"function_name is {function_name}")
                        if function_name[1] == key_value and "#" not in line:
                            if search_x86 and (self._check_gate_file_vaildation(find_case_file)):
                            # if search_x86:
                                x86_list[function_name[0]].append(find_case_file)
                            if search_hw and (self._check_gate_file_vaildation(find_case_file)):
                            # if search_hw:
                                hw_list[function_name[0]].append(find_case_file)
                            break

        target_element._x86_path_list = x86_list
        target_element._hw_path_list = hw_list

    
    def _check_gate_file_vaildation(self, find_case_file: str) -> int:
        check_gate_list_file = self._sct_job_path if self._sct_job_path else Path(resource_filename('case_manage', 'function/find_case_list/gate_hw_list.txt'))
        
        file_name = re.sub(r'.txt', "", find_case_file)
        if _is_list_name_in_file(file_name, check_gate_list_file):
            return 1
    
        if 'check.yaml' in check_gate_list_file:
            check_gate_list_file = re.sub(r'check', 'gate', check_gate_list_file)
            if _is_list_name_in_file(file_name, check_gate_list_file):
                return 1
        
            check_gate_list_file = re.sub(r'gate', 'post', check_gate_list_file)
            if _is_list_name_in_file(file_name, check_gate_list_file):
                return 1

        return 0

    def _get_list_max_len(self, data: Optional) -> int:
        max_len = 0
        if isinstance(data, list):
            for subvalue in data:
                length = self._get_list_max_len(subvalue)
                max_len = length if length > max_len else max_len
        else:
            max_len = len(data) if len(data) > max_len else max_len
        return max_len

    def check_case_vaildation(self, target_element: TargetElement) -> int:
        result = 1

        self.find_case_name_in_py(target_element)
        # if not target_element._function_name:
        #     if 'ecpri' in target_element._target_name:
        #         self.find_case_name_in_py(target_element, py_path_fh_ecpri)
        #     else:
        #         self.find_case_name_in_py(target_element, py_path_fh_cpri)

        self.find_function_name_list(target_element)

        if self._source == 'py' and self._get_list_max_len(target_element._py_path_list) == 0:
            # print(f"target is {target_element._target_name} function_name is {target_element._function_name} didn't find py")
            result = 0
            return None
        elif self._source == 'x86' and self._get_list_max_len(target_element._x86_path_list) == 0 and self._get_list_max_len(target_element._hw_path_list) == 0:
            # print(f"target is {target_element._target_name} function_name is {target_element._function_name} didn't find py")
            result = 0
            return None
        elif self._source == 'hw' and self._get_list_max_len(target_element._hw_path_list) == 0:
            result = 0
            return None
        else:
            self._target_element.append(target_element)
        return target_element

    @property
    def  get_elements(self) -> List[TargetElement]:
        return self._target_element
         



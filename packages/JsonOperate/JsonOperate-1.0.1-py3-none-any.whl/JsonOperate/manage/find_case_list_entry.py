#!/usr/bin/env python3
from JsonOperate.function.find_case_list.find_list import FindList
from JsonOperate.lib.output import SimilarOutput, FindListOutput
from typing import Dict, List, Union, Mapping, Set, Iterator
from pathlib import Path
import os
import re
import sys
import multiprocessing

def generate_targets(path: Path) -> Iterator[str]:
    # print(f"path is {path}")
    vector_files = os.listdir(path)
    for file in vector_files:
        if re.search('.json$',file):
            yield file

def get_required_targets(model: str, path: Path) -> List[str]:
    if model == 'list-info-all':
        vector_paths = os.listdir(path)

        def iterate_files(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    yield file_path
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    yield from iterate_files(dir_path)

        return {
            os.path.basename(target) for target in iterate_files(path)
        }
    elif model == 'list-info':
        return {
            target for target in generate_targets(path) 
        }
    else:
        pass

def multi_process_get_target(target_find_list, target):
    element = target_find_list.create_target(target)
    return target_find_list.check_case_vaildation(element)

def find_case_list(arguments):
    case_path = arguments.case_path[0]
    if '/lte/' in case_path:
        root_dir = re.search('.*(?=test/sct/lte/)',case_path)
        py_path = os.path.join(root_dir.group(), "test/sct/lte/tests")
    else:
        root_dir = re.search('.*(?=test/sct/py3/)',case_path)
        py_path = os.path.join(root_dir.group(), "test/sct/py3/tests")

    ci_list_path = os.path.join(root_dir.group(), "ci/testlist")
    target_find_list = FindList(py_path, ci_list_path, arguments.board, arguments.source, arguments.sct_job_path)

    excel_path = os.path.join(case_path, arguments.source)
    if not os.path.exists(excel_path):
        os.mkdir(excel_path)

    excel_path = os.path.join(excel_path, arguments.function + '_' + arguments.board + '.xlsx')
    excel_summary = FindListOutput(excel_path, arguments.display_equal_value)
    # excel_summary = FindListPandasOutput(excel_path, arguments.display_equal_value)

    with excel_summary as excel:
        excel.add_new_sheet(arguments.function + '_' + arguments.board)
        # for target in get_required_targets(arguments.model, case_path):
        #     # if 'NR_THOR_PUSCH_TDD_2RX_3CELLS_MULTILAYER' not in target:
        #         # print(f"target is {target}")
        #         # continue

        #     element = target_find_list.create_target(target)
        #     target_find_list.check_case_vaildation(element)

        num_processes = os.cpu_count()
        # print(f"The system has {num_processes} CPUs/cores in write excel.")

        with multiprocessing.Pool(processes=num_processes) as pool:
            args = [(target_find_list, target) for target in get_required_targets(arguments.model, case_path)]
            results = pool.starmap(multi_process_get_target, args)

        # elements = target_find_list.get_elements
        # elements = target_find_list.get_data_frame
        results = [result for result in results if result != None]
        excel.data_output(results)
        # excel.data_output(elements)

#!/usr/bin/env python3
import re
import os
from pathlib import Path
import multiprocessing

def multi_process_get_target(file, vector_path, arguments, get_target_info_from_file):
    if re.search('.json$',file):
        if tar := get_target_info_from_file(vector_path, file, arguments):
            return tar
    return {}

def get_target_name_and_path(vector_path: Path, get_target_info_from_file, arguments):
    
    def iterate_files(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                yield file_path
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                yield from iterate_files(dir_path)

    # vector_files = iterate_files(vector_path)
    # for file in vector_files:
    #     print(f"vector_files is {file}")

    num_processes = os.cpu_count()
    # print(f"The system has {num_processes} CPUs/cores in write excel.")

    with multiprocessing.Pool(processes=num_processes) as pool:
        args = [(file, vector_path, arguments, get_target_info_from_file) for file in iterate_files(vector_path)]
        results = pool.starmap(multi_process_get_target, args)

    # for file in vector_files:
    #     if re.search('.json$',file):
    #         if tar := get_target_info_from_file(vector_path, file, arguments):
    #             target_info.append(tar)
    return [result for result in results if result]

def get_target_reference_info(arguments, get_target_info_from_file):
    target_info = []
    vector_paths = arguments.case_path

    if '.json' in vector_paths[0]:
        file = os.path.basename(vector_paths[0])
        dir_name = os.path.dirname(vector_paths[0])
        target_info.append(get_target_info_from_file(dir_name, file, arguments))
    else:
        for vector_path in vector_paths:
            target_info += get_target_name_and_path(vector_path, get_target_info_from_file, arguments)
        
        unique_list = []

        for d in target_info:
            if d not in unique_list and d['name'] not in [x['name'] for x in unique_list]:
                unique_list.append(d)
        return unique_list
    
    return target_info

def get_output_path(arguments):
    root_dir = re.search('.*(?=test/sct/py3/)',arguments.case_path[0])
    if '/vectors_lte_ul/' in arguments.case_path[0]:
        output_path = os.path.join(root_dir.group(), "test/sct/py3/vectors_lte_ul/")
    else:
        output_path = os.path.join(root_dir.group(), "test/sct/py3/vectors/")
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    excel_name = "short_summary.xlsx" if 'short' == arguments.output_mode else "summary.xlsx"
    output_path = os.path.join(output_path, excel_name)
    return output_path
    # print(f"output_path is {output_path}")
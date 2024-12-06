#!/usr/bin/env python3
from JsonOperate.lib.output import FindListPandasOutput
from JsonOperate.function.find_case_list.find_list_by_panda import FindList
from JsonOperate.function.print_case_info.print_case_info import get_name_path, output_to_excel
# from JsonOperate.manage.print_case_repeat_info_entry import find_case_list_by_target
from JsonOperate.manage.sort_argument import get_target_reference_info
from JsonOperate.function.split_json_structure.split_json_structure import SplitJsonStructure
import multiprocessing
# from multiprocessing import Lock
import os
import pandas as pd
from typing import Dict, List, Union, Mapping, Set, Iterator
from copy import deepcopy
import re
import subprocess

def find_case_list_by_target(arguments, target):
    root_dir = re.search('.*(?=test/sct/py3/)',arguments.case_path[0])
    py_path = os.path.join(root_dir.group(), "test/sct/py3/tests")
        
    ci_list_path = os.path.join(root_dir.group(), "ci/testlist")

    target_find_list = FindList(py_path, ci_list_path, arguments.board, arguments.source, arguments.sct_job_path)

    element = target_find_list.create_target(target)
    result = target_find_list.check_case_vaildation(element)
    info = target_find_list.get_data_frame if result else 0

    return result, info

def get_important_path(base_path, file:str):
    path = os.path.join(base_path, file)
    _, *dirs = os.path.splitdrive(path)
    dirs = os.path.join(*dirs).split(os.sep)
    print(dirs)
    try:
        index = dirs.index("vectors")
    except ValueError:
        print("No vectors directory found")
        return []
    else:
        print(dirs[index+1:-1])
    
    return dirs[index+1:-1]

def get_target_info_from_file(base_path, file_path, arguments):
    file = os.path.basename(file_path)
    if file == file_path:
        dir = base_path
    else:
        dir = os.path.dirname(file_path)
    print(f"dir is {dir}")

    target_name, path = get_name_path(dir, file)
    improtant_path = get_important_path(dir, file)

    if arguments.source == "schema":
        return {
            "name": target_name,
            "path": path,
            "improtant_path": improtant_path
        }

    result, info = find_case_list_by_target(arguments, file)
    if result:
        return {
            "name": target_name,
            "path": path,
            "improtant_path": improtant_path
        }
    else:
        return None

def find_sub_value(search_value, match_value):
    for sub_v in search_value:
        if sub_v == match_value:
            return 1
        
    return 0

def generate_sorted_data(target_infos):
    num_processes = os.cpu_count()
    print(f"The system has {num_processes} CPUs/cores in read {len(target_infos)} json file.")
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(split_json, target_infos)
        for keys_structure in results:
            yield keys_structure

def json_structure_combine(total_json_structure, new_json_structure):
    # Find common keys
    # common_keys = set(total_json_structure.keys()) & set(new_json_structure.keys())
    for key, _ in new_json_structure.items():
        total_json_structure[key] = total_json_structure[key] + new_json_structure[key]

def copy_folder_to_server(local_folder, remote_path, username, host, source):
    try:
        # 删除远程文件夹
        delete_command = f"ssh {username}@{host} 'rm -rf {remote_path}/{source}'"
        subprocess.run(delete_command, shell=True, check=True)
        print(f"Removed existing folder at {remote_path} on {host}.")

        # 传输新的文件夹
        scp_command = [
            "scp",
            "-r",  # 递归传输文件夹
            local_folder,
            f"{username}@{host}:{remote_path}"
        ]
        subprocess.run(scp_command, check=True)
        print(f"Folder '{local_folder}' successfully copied to {remote_path} on {host}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy folder: {e}")

areas = ["common", "dl", "ul"]
def collect_json_structure(arguments):
    target_infos = get_target_reference_info(arguments, get_target_info_from_file)
    excel_path = target_infos[0]['path'].excel_path
    for target_info in target_infos:
        target_name = target_info["name"]
        if arguments.debug:
            if not (('HipTD_thor_valid_srs_tdd_bwv_CB008322_G_frCfg1208_td_jumping_trigger_snapshot' in target_info["name"]) or 
                    ('HipTD_Thor_CAP3B_Thor15_FDD_18Cell_20MHz_4RX_128UE_PUSCH_11000RRC_COMP_CATM' in target_info["name"])):
                continue
            print(f"print tar is {target_name}")
        else:
            print(f"print tar is {target_info['path'].json_path}")

        # total_collect_info.append(split_json(target_info))
    total_json_structure = {"common": None, "ul": None, "dl": None}
    # total_json_structure = None
    if not arguments.send_directly:
        for (json_structure, area) in generate_sorted_data(target_infos):
        # for json_structure in total_collect_info:
            if total_json_structure[area] is None:
                total_json_structure[area] = json_structure
            else:
                # total_json_structure = total_json_structure + json_structure
                json_structure_combine(total_json_structure[area], json_structure)

    dir_path, _ = os.path.split(excel_path)

    path_list = []
    data_list = []
    for c_area in areas:
        if not arguments.send_directly:
            if total_json_structure[c_area] == None:
                continue

            output_data = pd.DataFrame(total_json_structure[c_area])

            # unique_count = output_data['key'].nunique()
            # print(f'unique_count in key is {unique_count}')
            # output_data['length'] = output_data['value'].apply(lambda x: (str(x).count(' ') + str(x).count('_') + str(x).count('-')))
            # output_data['value_index'] = output_data.groupby('key')['value'].transform(lambda x: pd.factorize(x)[0])

            # chunk_size = 700000  # Set the desired chunk size
            chunk_size = 100000
            tail = len(output_data) % chunk_size

            print(f'output len is {len(output_data)}')

            # Calculate the number of chunks needed
            num_chunks = int(len(output_data) / chunk_size) if tail == 0 else int(len(output_data) / chunk_size) + 1

            # Split the DataFrame into chunks
            df_chunks = [output_data[i * chunk_size:(i + 1) * chunk_size] if (i+1) < num_chunks else output_data[i * chunk_size:i * chunk_size+tail] for i in range(num_chunks)]

        if 'schema' == arguments.source:
            dataset_path = os.path.join(dir_path, 'schema')
        else:
            dataset_path = os.path.join(dir_path, 'sct')

        if not os.path.exists(dataset_path):  # 判断路径是否存在
            os.makedirs(dataset_path)        # 创建路径
            print(f"Path '{dataset_path}' created.")
        else:
            print(f"Path '{dataset_path}' already exists.")

        if not arguments.send_directly:
            for id, df_chunk in enumerate(df_chunks):
                excel_path = os.path.join(dataset_path, f"{c_area}_{id}.xlsx")
                print(f'excel path is {excel_path}')
                # path_list.append(excel_path)
                append_data = deepcopy(df_chunk)
                data_list.append(append_data)
                output_to_excel(excel_path, df_chunk)

    if arguments.user_account != '':
        copy_folder_to_server(dataset_path, arguments.target_path, arguments.user_account, arguments.server, arguments.source)

    # for excel_path, df_chunk in zip(path_list, data_list):
    #     output_to_excel(excel_path, df_chunk)
    # multi_write_excel(path_list, data_list)
    # total_vocab_path = os.path.join(dir_path, f"total_vocab.txt")
    # with open(total_vocab_path, 'w', newline='', encoding='utf-8') as f:
    #     for chunk_data in data_list:
    #         for text in chunk_data['value']:
    #             f.write(text + '\n')
    #         for text in chunk_data['key']:
    #             f.write(text + '\n')
            # output_to_excel(excel_path, df_chunk)

# excel_lock = Lock()

# def write_data_to_excel(excel_path, df_chunk):
#     with excel_lock:
#         print(f"file is {excel_path}")
#         print(f"df_chunk is {df_chunk}")
#         output_to_excel(excel_path, df_chunk)


# def multi_write_excel(path_list, data_list):
#     num_processes = os.cpu_count()
#     print(f"The system has {num_processes} CPUs/cores in write {len(data_list)} train file.")
#     with multiprocessing.Pool(processes=num_processes) as pool:
#         args = [(path, data) for path, data in zip(path_list, data_list)]
#         pool.starmap(write_data_to_excel, args)

def split_json(target_info):
    # prepare data
    tar_data = SplitJsonStructure(target_info['path'].json_path, target_info["name"], target_info["improtant_path"])
    return tar_data.keys_structure


def output_to_excel(excel_path, data):
    excel_output = FindListPandasOutput(excel_path, 1)
    with excel_output as excel:
        excel.add_new_sheet('json_structure')
        # df = pd.DataFrame(data)
        excel.data_output(data, 0)

    # source_vocab_path = excel_path.replace('.xlsx', '.txt')

    # with open(source_vocab_path, 'w', newline='', encoding='utf-8') as f:
    #     for text in data['value']:
    #         f.write(text + '\n')
    #     for text in data['key']:
    #         f.write(text + '\n')
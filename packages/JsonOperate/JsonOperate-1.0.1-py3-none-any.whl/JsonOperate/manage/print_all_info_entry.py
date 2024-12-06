#!/usr/bin/env python3
from JsonOperate.function.print_case_info.print_case_info import PrintCaseInfo, get_target_info_from_file, output_to_excel
from JsonOperate.manage.sort_argument import get_target_reference_info

def print_all_info(arguments):
    target_infos = get_target_reference_info(arguments, get_target_info_from_file)
    for target_info in target_infos:

        target_name = target_info["name"]
        if arguments.debug:
            if not (('HipTD_TRX_FD_PUSCH_10MHz_HST_InvalidNS_ValidHS_2RX_2CELL' in target_info["name"]) or 
                    ('HipTD_Thor_CAP3B_Thor15_FDD_18Cell_20MHz_4RX_128UE_PUSCH_11000RRC_COMP_CATM' in target_info["name"])):
                continue
            print(f"print tar is {target_name}")
        else:
            print(f"print tar is {target_name}")

        print_case(target_info)


def print_case(target_info):
    # prepare data
    tar_data = PrintCaseInfo(target_info)
    sorted_data = tar_data.sort_data()
    # ouput data
    output_to_excel(tar_data.get_output_path(), sorted_data)

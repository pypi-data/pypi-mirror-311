#!/usr/bin/env python3
from argparse import ArgumentParser
# from JsonOperate.manage.find_case_list_entry import find_case_list
from JsonOperate.manage.print_all_info_entry import print_all_info
from JsonOperate.manage.collect_json_structure_entry import collect_json_structure
from JsonOperate.function.collect_case_info.collect_case_info import CollectAllCaseInfo
import json

# from compareCase.compare import output
# from compareCase.compare.adapt_compare_method import FieldCompare
from typing import Dict, List, Union, Mapping, Set, Iterator, overload
from pathlib import Path
import os
import re
import sys
# import pandas as pd

def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '--case-path', '-p',
        action='store',
        nargs='+',
        default='',
        help='case vectors path usually under l1sw/test/sct/py3/vectors',
        required='--parser.target' in sys.argv,
    )
    parser.add_argument(
        '--sct-job-path',
        action='store',
        default='',
        help='use config sct-job-list instead of default hw list',
    )
    parser.add_argument(
        '--model', '-m',
        action='store',
        choices=['every', 'target-every', 'target-reference', 'fixed-reference', 'list-info', 'list-info-all'],
        default='every',
        help='every means every file compare other files,'
             'target-every means target file compare other files,'
             'target-reference means target file compare reference files,'
             'list-info means print relative info on py/x86/hw list',
    )
    parser.add_argument(
        '--source', '-s',
        action='store',
        choices=['py', 'x86', 'hw', 'vector', 'schema'],
        default='x86',
        help='py means case can be found in tests/.py will be comapre,'
             'x86 means case can be found in ci/clang_list will be comapre,'
             'hw means case can be found in ci/hw_list will be comapre,'
             'vector all case is vaild', 
    )
    parser.add_argument(
        '--board', '-b',
        action='store',
        choices=['loki', 'thor', 'lte', 'all'],
        default='thor',
        help='choise board',
    )
    parser.add_argument(
        '--target', '-t',
        action='store',
        nargs='+',
        default='',
        help='case name add case file path can get the path of target',
    )
    parser.add_argument(
        '--reference', '-r',
        action='store',
        default='',
        help='case name add case file path can get the path of reference',
    )
    parser.add_argument(
        '--additional-reference', '-a',
        action='store',
        nargs='+',
        default='',
        help='case name add case file path can get the path of additional reference',
    )
    parser.add_argument(
        '--server',
        action='store',
        default='10.70.86.30',
        help='target server id of we want to copy vector to ',
    )
    parser.add_argument(
        '--user-account',
        action='store',
        default='',
        help='target server account of we want to copy vector to ',
    )
    parser.add_argument(
        '--target-path',
        action='store',
        default='/home/ute/app',
        help='target path account of we want to copy vector to ',
    )
    parser.add_argument(
        '--function', '-f',
        action='store',
        choices=['find-case-list', 'function-test', 'print-case-info', 'collect-json-structure'],
        default='',
        help='confirm a function you need',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='start debug',
    )
    parser.add_argument(
        '--send-directly',
        action='store_true',
        default=False,
        help='direct send data to server',
    )
    parser.add_argument(
        '--output-case-name',
        action='store',
        nargs='+',
        default='',
        help='provide combine or split case name',
    )
    parser.add_argument(
        '--excel-path',
        action='store',
        default='',
        help='set trainning data path for ML training',
    )
    return parser

def function_test(arguments):
    print("this function test add your small code here!")

_FUNCTION = Union[
    # find_case_list,
    function_test,
    print_all_info,
    collect_json_structure,
]

_RULE_FILE_MAP: Mapping[str, _FUNCTION] = {
    # 'find-case-list': find_case_list,
    'function-test' : function_test,
    'print-case-info' : print_all_info,
    'collect-json-structure': collect_json_structure,
}

def main():
    arguments = get_argument_parser().parse_args()
    _RULE_FILE_MAP[arguments.function](arguments)

if __name__ == '__main__':
    main()

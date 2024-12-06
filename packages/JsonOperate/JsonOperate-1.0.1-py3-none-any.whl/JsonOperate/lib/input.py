#!/usr/bin/env python3
from typing import Dict, List, Optional
from pathlib import Path
import os
import re
import pandas as pd
import openpyxl
import ast

class NormalInput:
    __slots__ = (
        '_path',
        '_sheet_name_list',
    )
    _path: Path
    _sheet_name_list: List

    def __init__(self, path: Path):
        # Load the Excel workbook
        self._path = path
        workbook = openpyxl.load_workbook(path)
        # Get a list of sheet names
        self._sheet_name_list = workbook.get_sheet_names()

    def read_excel_info(self, sheet):
        df = pd.read_excel(self._path, index_col=0, sheet_name=sheet, dtype=object)
        df.index = df.index.str.lower()
        return df
    
    def read_excel_info_int_index(self, sheet):
        df = pd.read_excel(self._path, index_col=0, sheet_name=sheet, dtype=object)
        return df

    def eval_panda_data(self,ori_data):
        for rowIndex, row in ori_data.iterrows():
            for columnIndex, value in row.items():
                if isinstance(value, str):
                    if '[' in value and ']' in value:
                        # print(f"value is {value} type is {type(value)}")
                        ori_data.loc[rowIndex, columnIndex] = ast.literal_eval(value)
                        # print(f"after eval value is {value} type is {type(value)}")
        return ori_data

    def get_sheet_name_list(self):
        return self._sheet_name_list
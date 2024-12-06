from typing import Dict, List, Optional
import xlsxwriter
from pathlib import Path

class Excel:
    __slots__ = (
        '_xlrawu',
        '_sheet',
        '_last_sheet_id',
        '_bg_colour_r',
        '_bg_colour_g',
        '_bg_colour_y',
        '_bg_colour_b',
        '_bg_colour_a',
        '_text_wrap',
        '_column_width',
        '_last_name',
    )
    _xlrawu: Optional
    _sheet: List
    _last_sheet_id: int
    _bg_colour_r: Optional
    _bg_colour_g: Optional
    _bg_colour_y: Optional
    _bg_colour_b: Optional
    _bg_colour_a: Optional
    _text_wrap: Optional
    _column_width: int
    _last_name:str

    def __init__(self, xlpath: Path, mode: bool):
        self._xlrawu = xlsxwriter.Workbook(xlpath)
        self._sheet = []
        self._last_sheet_id = -1
        self._last_name = 'sheet1'
        # self._sheet.set_column('A:AL',40)

        # self.colour = self._xl.add_format({'color':'red'})
        self._bg_colour_r = self._xlrawu.add_format({'bg_color':'red', 'text_wrap':mode, 'align': 'right'})
        self._bg_colour_g = self._xlrawu.add_format({'bg_color':'green', 'text_wrap':mode, 'align': 'right'})
        self._bg_colour_y = self._xlrawu.add_format({'bg_color':'yellow', 'text_wrap':mode, 'align': 'right'})
        self._bg_colour_b = self._xlrawu.add_format({'bg_color':'blue', 'text_wrap':mode, 'align': 'right'})
        self._bg_colour_a = self._xlrawu.add_format({'bg_color':'cyan', 'text_wrap':mode, 'align': 'right'})
        # self.bg_colour_p = self._xl.add_format({'bg_color':'purple'})
        self._text_wrap = self._xlrawu.add_format({'text_wrap':mode, 'align': 'right'})

    def add_sheet(self, name: str):
        self._last_sheet_id += 1
        sheet = self._xlrawu.add_worksheet(name)
        # sheet.protect(options={'Contents': False, 'UserInterfaceOnly' : False, 'AllowUsingPivotTables': True, 'AllowInsertingHyperlinks': True})
        self._sheet.append(sheet)
        self._last_name = name
        # print(f"sheet name is {self._sheet[self._last_sheet_id]} ,sheet id is {self._last_sheet_id} sheetname 0 {self._sheet[0]}")

    def _check_sheet_id(self):
        if self._last_sheet_id == -1:
            print(f"you have to create one sheet before you use it")

    def _check_sheet_by_given_id(self, given_id: int):
        if self._last_sheet_id == -1 or given_id > self._last_sheet_id:
            print(f"you have to create one sheet before you use it, given id is {given_id}")

    def writetoxl(self, row: int, col: int, content: int, option: int = 0):
        self._check_sheet_id()

        if(option == 0):
            self._sheet[self._last_sheet_id].write_string(row,col,content,self._text_wrap)
        elif(option == 1):
            self._sheet[self._last_sheet_id].write_string(row,col,content,self._bg_colour_g)
        elif(option == 2):
            self._sheet[self._last_sheet_id].write_string(row,col,content,self._bg_colour_r)
        elif(option == 3):
            self._sheet[self._last_sheet_id].write_string(row,col,content,self._bg_colour_y)
        elif(option == 4):
            self._sheet[self._last_sheet_id].write_string(row,col,content,self._text_wrap)
            self._sheet[self._last_sheet_id].set_column(col,col,0)
        elif(option == 5):
            self._sheet[self._last_sheet_id].write_string(row,col,content,self._bg_colour_b)
        elif(option == 6):
            self._sheet[self._last_sheet_id].write_string(row,col,content,self._bg_colour_a)
        else:
            pass

    def paint_chart(self, chart_name:str, x_name:str, y_name:str, data:dict, pisition:str, start_col:int):

        # Configure the chart data
        categories = list(data.keys())
        # values = list(data.values())

        length = len(categories) if len(categories) < 20 else 20

        row = 1
        for category, value in data.items():
            self._sheet[self._last_sheet_id].write(row, start_col, category)
            self._sheet[self._last_sheet_id].write(row, start_col+1, value)
            row += 1

        # Create a chart object
        chart = self._xlrawu.add_chart({'type': 'column'})
        chart.add_series({
            'name': chart_name,
            'categories': [self._last_name, 1, start_col, length , start_col],
            'values': [self._last_name, 1, start_col+1, length, start_col+1],
        })
        # Add x-axis label
        chart.set_x_axis({'name': x_name})
        
        # Add y-axis label
        chart.set_y_axis({'name': y_name})
        if len(categories) > 10:
            chart.set_size({'width': 800})
        # elif len(categories) > 30:
        #     chart.set_size({'width': 1200})
        # elif len(categories) > 10:
        #     chart.set_size({'width': 800})
        # else:
        #     pass
        # Insert the chart into the worksheet
        self._sheet[self._last_sheet_id].insert_chart(pisition, chart)


    def set_column(self, pos: int, weight: int):
        self._check_sheet_id()
        self._sheet[self._last_sheet_id].set_column(pos,pos,weight)

    def writetoxl_by_given_id(self, row: int, col: int, content: int, given_id: int, option=0):

        self._check_sheet_by_given_id(given_id)

        if(option == 0):
            # self._sheet[given_id].write_string(row,col,content,self._text_wrap)
            self._sheet[given_id].write_formula(row,col,content,self._bg_colour_y)
        elif(option == 1):
            self._sheet[given_id].write_formula(row,col,content,self._bg_colour_a)
        elif(option == 2):
            self._sheet[given_id].write_string(row,col,content,self._bg_colour_y)
        elif(option == 3):
            self._sheet[given_id].write_string(row,col,content,self._bg_colour_a)
        else:
            pass

    def set_column_by_given_id(self, pos: int, weight: int, given_id: int):
        self._check_sheet_by_given_id(given_id)
        self._sheet[given_id].set_column(pos,pos,weight)

    def close(self):
        self._xlrawu.close()

#!/usr/bin/env python3

import pandas as pd
import numpy as np
import re

dictA = {'A': [[1, 2, 3], [2, 3, 4], [4, 5, 6]],
    'B': [[4, 5, 7], [7, 4, 4],],
    'C': [[4, 6, 0]]
}
def test_panda():

    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dictA.items()]))
    print(f"test_df is {df}")

def convert_dict_to_panda(dict_data, basic_index):
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dict_data.items()]), dtype=object)
    df.index = [basic_index + "_" + str(i) for i in df.index]
    return df

def convert_dict_to_panda_one_index(dict_data, id):
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dict_data.items()]), dtype=object)
    df.index = [id]
    return df

def convert_dict_to_panda_max_index(dict_data, basic_index):
    x=[len(v) if isinstance(v, list) else 0 for _,v in dict_data.items()]
    x = [basic_index + "_" + str(i) for i in range(max(x))]
    df = pd.DataFrame(data=dict_data, index=x)
    return df

def panda_concat(df_list, axis):
    df = pd.concat(df_list, axis=axis, sort=True)
    return df

def default_panda():
    df = pd.DataFrame()
    return df

def check_if_converted_str(data):
    if re.match(r'^[0-9\[\], .+-]+(?:e[\-0-9]+)?$|(?i)true|(?i)false|\[', data):
        return True
    else:
        return False

def add_data_to_panda(df, v, index, key_path, title):    
    title_index = str(title) + '_' + str(index)

    if str(key_path) in df.columns:
        if title_index in df.index:
            df.loc[title_index, str(key_path)] = "'" + v + "'" if isinstance(v, str) and check_if_converted_str(v) else str(v)
        else:
            df_v = convert_dict_to_panda_one_index({str(key_path): "'" + v + "'" if isinstance(v, str) and check_if_converted_str(v) else str(v)}, title_index)
            df = panda_concat([df, df_v], 0)
    else:
        df_v = convert_dict_to_panda_one_index({str(key_path): "'" + v + "'" if isinstance(v, str) and check_if_converted_str(v) else str(v)}, title_index)
        df = panda_concat([df, df_v], 1)
    return df

def compare_two_dataframe(df1, df2):

    # df1.index = df1.index.str.lower()
    # df2.index = df2.index.str.lower()

    df1a, df2a = df1.align(df2, join='outer', axis=None)

    df1a.fillna("fill_na", inplace=True)
    df2a.fillna("fill_na", inplace=True)
    # compare the two dataframes
    df_diff_o = df1a.compare(df2a)
    print(f'df_diff_o is {df_diff_o}')
    # df_diff_o = compare_float_data(df_diff_o, df1a, df2a)

    # select the cells that are different
    df_diff = df_diff_o[df_diff_o.ne(0).any(1)]

    df_diff.fillna("invaild_diff", inplace=True)

    return df_diff

def compare_float_data(df_diff, df1, df2):
    for col in df_diff:
        data1 = df1.loc[df_diff.index,col[0]][0]
        data2 = df2.loc[df_diff.index,col[0]][0]
        print(f"data1 is {data1} , data 2 is {data2}")
        print(f"data1 type is {type(df2.loc[df_diff.index,col[0]][0])} , data 2 type is {type(df1.loc[df_diff.index,col[0]][0])}")
        if isinstance(data1, str) or isinstance(data2, str):
            continue

        result = np.isclose(df2.loc[df_diff.index,col[0]], df1.loc[df_diff.index,col[0]], rtol=1e-05, atol=1e-08)
        if all(result):
            df_diff = df_diff.drop(col, axis=1)
    return df_diff

def head_cell_id(df):
    if df["['[]', 'standard']"].iloc[0] == "LTE":
        cell_id = "['[]', 'uplink', 'ln_cell_id']"
    else:
        cell_id = "['[]', 'uplink', 'subcell_id']"
    new_order = [cell_id] + [col for col in df.columns if col != cell_id]
    df = df.reindex(columns=new_order)
    df = df.sort_values(by=cell_id, na_position='first')
    return df

def add_lable(data, label, df_info):
    for key, v in data.items():
        title = "item_id_in_case"
        total_title = "total_items_number_in_case"

        v_len = v.shape[0]
        case_name_value = pd.DataFrame({'case_name': [label] * v_len, title: range(v_len), total_title: [v_len] * v_len}, index=v.index)
        df_info_repeat = pd.concat([df_info]*v_len, ignore_index=True)
        df_info_repeat.index = pd.Index(v.index)
        data[key] = panda_concat([v, case_name_value, df_info_repeat], 1)

    return data

def merge_repeat_data(df, sort_group, channel = '', sclar_channel_group = []):
    df.fillna(" ", inplace=True)
    # print(f"channel is {channel}, sclar_channel_group is {sclar_channel_group}")
    counts = df.groupby(sort_group).size().rename(f'{channel}repeat_number').to_frame()#.replace(1, 0)
    merged_df = pd.merge(df, counts.copy(), on=sort_group, how='left')
    if channel:
        df_subset = merged_df[sclar_channel_group]

        empty_mask = (df_subset == ' ').all(axis=1)
        # print(f"empty_mask is {empty_mask}")

        merged_df.loc[empty_mask, f'{channel}repeat_number'] = 0

    repeat_ids = merged_df.groupby(sort_group).ngroup().rename(f'{channel}item_id_in_ci').to_frame()
    merged_df = pd.concat([merged_df, repeat_ids], axis=1)
    
    return merged_df.sort_values(by=[f'{channel}repeat_number',f'{channel}item_id_in_ci'], na_position='first' ,ascending=[False, True])

def map_level(percent):
    if percent >= 90:
        return "repeat over 90"
    elif percent >= 80:
        return "repeat from 80 to 90"
    elif percent >= 60:
        return "repeat from 60 to 80"
    elif percent >= 30:
        return "repeat from 30 to 60"
    else:
        return "repeat below 30"

def add_percentage(df, channels):
    columns = []
    for channel in channels:
        columns.append(f'{channel}repeat_number')

    mask = (((df[columns] != 1).all(axis=1)) & ((df[columns] != 0).any(axis=1)))
    case_repeat_percentage = mask.groupby(df['case_name']).mean() * 100
    case_repeat_percentage = df['case_name'].map(case_repeat_percentage).rename(f'case_repeat_percentage').to_frame()
    repeat_level = case_repeat_percentage['case_repeat_percentage'].apply(map_level).rename(f'repeat_level').to_frame()
    merge_df = pd.concat([df, case_repeat_percentage, repeat_level], axis=1)

    df_unique = merge_df.drop_duplicates(subset='case_name', keep='first')
    
    repeat_level_counts = df_unique['repeat_level'].value_counts().to_dict()
    
    # Calculate percentage of total for each unique name
    repeat_level_counts = merge_df['repeat_level'].apply(lambda x: repeat_level_counts[x]).rename(f'repeat_level_counts').to_frame()
    merge_df = pd.concat([merge_df, repeat_level_counts], axis=1)
    return merge_df

def merge_df(df1, df2):
    common_cols = list(set(df1.columns).intersection(set(df2.columns)))
    if not common_cols:
        return df1
    columns_with_nan = [col for col in common_cols if df2[col].isna().any()]
    if columns_with_nan:
        columns_without_nan = [col for col in common_cols if df2[col].notna().all()]
        df2_drop = df2.drop(columns=columns_with_nan)
        merged_df = pd.merge(df1, df2_drop, on=columns_without_nan, how='outer')

    else:
        merged_df = pd.merge(df1, df2, on=common_cols, how='outer')

    return merged_df

def get_group(df):
    return [column for column in df.columns if is_repeat_item(column)]

def is_repeat_item(key):
    if "repeat_number" in key:
        return 1
    else:
        return 0



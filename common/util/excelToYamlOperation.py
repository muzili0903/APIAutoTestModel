# -*- coding: utf-8 -*-
"""
@Author  :muzili
@time    :2023/6/30 16:23
@file    :excelToYamlOperation.py
"""
from common.util.excelOperation import ReadExcel
from common.util.fileOperation import get_file_path
from common.util.filePath import ensure_path_sep
from common.util.yamlOperation import write_yaml


def single_excel_to_yaml(sheetname: str, interface: str = '',
                         path: str = r"..\..\testData\pro\APIAutoTestDataModel.xlsx") -> None:
    """
    单表单或单接口转为yaml文件
    :param path: 路径
    :param sheetname: 表table名
    :param interface: 接口名
    """
    datas = ReadExcel(filename=path, sheet_name=sheetname).read_to_dict()
    yamlPath = get_file_path(path) + '\\' + sheetname + '\\'
    if interface.__eq__(''):
        for filename, data in datas.items():
            yamlPath += filename + '.yaml'
            write_yaml(ensure_path_sep(yamlPath), data)
    else:
        for filename, data in datas.items():
            if interface.__eq__(filename):
                yamlPath += filename + '.yaml'
                write_yaml(ensure_path_sep(yamlPath), data)
                break
        else:
            print("接口不存在")


if __name__ == '__main__':
    ...

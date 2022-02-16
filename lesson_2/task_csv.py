import csv
import re
import os

from utils import detect_encoding

"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов 
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. 
"""


def get_data(filenames_list: list):
    titles = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = []
    main_data.append(titles)
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for f in filenames_list:
        encoding = detect_encoding(f)
        print(f'Обнаружена кодировка {encoding} в файле {f}')
        with open(f, 'r', encoding=encoding) as text_file:
            text = text_file.readlines()
            for line in text:
                os_developer = re.match(r'Изготовитель системы:(.*)', line)
                os_name = re.match(r'Название ОС:(.*) Microsoft (.*)', line)
                product_code = re.match(r'Код продукта:(.*)', line)
                system_type = re.match(r'Тип системы:(.*)', line)
                if os_developer:
                    os_developer = os_developer.group(1).strip()
                    os_prod_list.append(os_developer)
                elif os_name:
                    os_name = os_name.group(2).strip()
                    os_name_list.append(os_name)
                elif product_code:
                    product_code = product_code.group(1).strip()
                    os_code_list.append(product_code)
                elif system_type:
                    system_type = system_type.group(1).strip()
                    os_type_list.append(system_type)

    params = [os_prod_list, os_name_list, os_code_list, os_type_list]
    main_data.extend(zip(*params))  # transposition
    print(main_data)
    return main_data


def write_to_csv(filenames_list: list, csv_filename: str):
    with open(csv_filename, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in get_data(filenames_list):
            writer.writerow(row)


if __name__ == '__main__':
    filenames_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    tmp_dir = '../tmp'
    files = [os.path.join(tmp_dir, f) for f in filenames_list]
    csvfilename = os.path.join(tmp_dir, 'task_2_1.csv')
    write_to_csv(files, csvfilename)

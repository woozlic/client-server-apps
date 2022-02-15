import csv
import datetime
import os.path
import re
import json

import chardet
import yaml


def detect_encoding(filename: str) -> str:
    DETECTOR = chardet.UniversalDetector()
    with open(filename, 'rb') as f:
        for i in f:
            DETECTOR.feed(i)
            if DETECTOR.done:
                break
        DETECTOR.close()
    return DETECTOR.result['encoding']


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
                os_developer = re.match(r'Изготовитель ОС:(.*)', line)
                os_name = re.match(r'Название ОС:(.*)', line)
                product_code = re.match(r'Код продукта:(.*)', line)
                system_type = re.match(r'Тип системы:(.*)', line)
                if os_developer:
                    os_developer = os_developer.group(1).strip()
                    os_prod_list.append(os_developer)
                elif os_name:
                    os_name = os_name.group(1).strip()
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


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date: datetime.datetime):
    json_file = 'tmp/orders.json'
    params = [item, quantity, price, buyer, date]

    with open(json_file, 'r', encoding='utf-8') as f:
        orders_obj = json.loads(f.read())

    order = {}
    if all(params):
        order['item'] = item
        order['quantity'] = quantity
        order['price'] = price
        order['buyer'] = buyer
        order['date'] = date.strftime('%d.%m.%Y')

    orders_obj['orders'].append(order)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(orders_obj, f, indent=4)


def save_obj_to_yaml(obj_dict: dict, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        data = yaml.dump(obj_dict, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return data


def load_obj_from_yaml(filepath: str) -> dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


if __name__ == '__main__':
    filenames_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    tmp_dir = 'tmp'
    files = [os.path.join(tmp_dir, f) for f in filenames_list]
    csvfilename = 'output.csv'
    write_to_csv(files, csvfilename)

    orders = [
        ['Milk', 4, 43.7, 'Dmitry D.', datetime.datetime.now()],
        ['Bread', 1, 28.5, 'Dmitry D.', datetime.datetime.now()],
    ]
    for order in orders:
        write_order_to_json(*order)

    yaml_obj = {
        'list': [1, 2, 3],
        4: 4,
        'euros': {
            '1€': '1 €',
            '2€': '2 €',
            '3€': '3 €',
        }
    }

    yaml_file = 'tmp/file.yaml'
    save_obj_to_yaml(yaml_obj, yaml_file)

    res_yaml = load_obj_from_yaml(yaml_file)
    print(yaml_obj)
    print(res_yaml)
    assert res_yaml == yaml_obj

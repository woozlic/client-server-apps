import datetime
import json


"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. 
Написать скрипт, автоматизирующий его заполнение данными. 
"""


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date: datetime.datetime):
    json_file = '../tmp/orders.json'
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


if __name__ == '__main__':

    orders = [
        ['Milk', 4, 43.7, 'Dmitry D.', datetime.datetime.now()],
        ['Bread', 1, 28.5, 'Dmitry D.', datetime.datetime.now()],
    ]
    for order in orders:
        write_order_to_json(*order)

"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом
формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление
в формат Unicode и также проверить тип и содержимое переменных.
"""


def print_value_and_type(items: list) -> None:
    """
    The function prints the values and type of each item in
    the list (the list is an argument to the function).
    :param items:
    :return: None
    """
    for item in items:
        print(item)
        print(type(item))
    print('-' * 80)


VAR_1 = 'разработка'
VAR_2 = 'сокет'
VAR_3 = 'декоратор'
STR_LIST = [VAR_1, VAR_2, VAR_3]

print_value_and_type(STR_LIST)

VAR_UNICODE_1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
VAR_UNICODE_2 = '\u0441\u043e\u043a\u0435\u0442'
VAR_UNICODE_3 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
UNICODE_LIST = [VAR_UNICODE_1, VAR_UNICODE_2, VAR_UNICODE_3]

print_value_and_type(UNICODE_LIST)

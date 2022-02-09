"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).
"""

VAR_1_STR = 'разработка'
VAR_2_STR = 'администрирование'
VAR_3_STR = 'protocol'
VAR_4_STR = 'standard'

STR_LIST = [VAR_1_STR, VAR_2_STR, VAR_3_STR, VAR_4_STR]

result_bytes = []
for el in STR_LIST:
    el_b = el.encode('utf-8')
    print(el_b)
    result_bytes.append(el_b)

print()

result_str = []
for el in result_bytes:
    el_str = el.decode('utf-8')
    result_str.append(el_str)

print(result_str)

"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку
созданного файла (исходить из того, что вам априори неизвестна кодировка этого файла!).
Затем открыть этот файл и вывести его содержимое на печать.
ВАЖНО: файл должен быть открыт без ошибок вне зависимости от того,
в какой кодировке он был создан!
"""
from chardet import detect

LINES_LST = ['сетевое программирование', 'сокет', 'декоратор']
with open('test.txt', 'w') as file:
    for line in LINES_LST:
        file.write(f'{line}\n')
file.close()

# узнаем кодировку файла
with open('test.txt', 'rb') as file:
    CONTENT = file.read()
ENCODING = detect(CONTENT)['encoding']
print(ENCODING)

# открываем файл в правильной кодировке
with open('test.txt', 'r', encoding=ENCODING) as file:
    CONTENT = file.read()
print(CONTENT)

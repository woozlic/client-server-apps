"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл в неизвестной
кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
"""
import chardet

text_filepath = '../tmp/task_1_6.txt'

LINES_LST = ['сетевое программирование', 'сокет', 'декоратор']
with open(text_filepath, 'w') as file:
    for line in LINES_LST:
        file.write(f'{line}\n')

DETECTOR = chardet.UniversalDetector()
with open(text_filepath, 'rb') as test_file:
    for i in test_file:
        DETECTOR.feed(i)
        if DETECTOR.done:
            break
    DETECTOR.close()
print(DETECTOR.result['encoding'])

with open(text_filepath, 'r', encoding=DETECTOR.result['encoding']) as file:
    CONTENT = file.read()
print(CONTENT)

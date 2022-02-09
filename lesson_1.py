import subprocess

import chardet


print('1.')

words = ['разработка', 'сокет', 'декоратор']
for word in words:
    print(word, type(word))

print()
uniwords = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430', '\u0441\u043e\u043a\u0435\u0442',
            '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

for word in uniwords:
    print(word, type(word))


print('2.')
words = [b'class', b'function', b'method']
for word in words:
    print(type(word), word, len(word))

print()

# words = [b'attribute', b'класс', b'функция', b'type']

print('3. Нельзя слова на кириллице представлять в байтовом типе, SyntaxError')

print('4.')

words = ['разработка', 'администрирование', 'protocol', 'standard']
for word in words:
    word = word.encode('utf-8')
    print(word)
    word = word.decode('utf-8')

print('5.')


def ping(service):
    args = ['ping', service]
    ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    count = 0
    for line in ping.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding'])
        print(line)
        if count == 4:
            break
        count += 1


services = ['yandex.ru', 'youtube.com']
for service in services:
    ping(service)


print('6.')

LINES_LST = ['сетевое программирование', 'сокет', 'декоратор']
with open('test.txt', 'w') as file:
    for line in LINES_LST:
        file.write(f'{line}\n')

DETECTOR = chardet.UniversalDetector()
with open('test.txt', 'rb') as test_file:
    for i in test_file:
        DETECTOR.feed(i)
        if DETECTOR.done:
            break
    DETECTOR.close()
print(DETECTOR.result['encoding'])

with open('test.txt', 'r', encoding=DETECTOR.result['encoding']) as file:
    CONTENT = file.read()
print(CONTENT)

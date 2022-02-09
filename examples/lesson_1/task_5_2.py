"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты
из байтового в строковый (предварительно определив кодировку выводимых сообщений).
"""

import subprocess
import chardet

URLS = ['yandex.ru', 'youtube.com']
for url in URLS:
    ping_ya = subprocess.Popen(('ping', url), stdout=subprocess.PIPE)

    for i, line in enumerate(ping_ya.stdout):
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8')) if i < 5 else ping_ya.kill()

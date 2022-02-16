"""
5.Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на
кириллице.
"""
import subprocess

import chardet


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

"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""

words = ['class', 'function', 'method']
for word in words:
    new_word = eval(f"b'{word}'")
    print(type(new_word), new_word, len(new_word))

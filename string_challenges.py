from utils import delimiter

delimiter()
# Вывести последнюю букву в слове
word = 'Архангельск'
print(word[-1])


delimiter()
# Вывести количество букв "а" в слове
word = 'Архангельск'
print(word.count('а'))


delimiter()
# Вывести количество гласных букв в слове
word = 'Архангельск'
print(len([x for x in word if x in 'АЕЁИОУЫЭЮЯаеёиоуыэюя']))


delimiter()
# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
print(len([w for w in sentence.split(' ') if w]))


delimiter()
# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
print(*[w for w in sentence.split(' ') if w], sep='\n')


delimiter()
# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
print(sum([len(w) for w in sentence.split(' ') if w])/len([len(w) for w in sentence.split(' ') if w]))

import random
a = "Стратегии"
b = "Шутеры"
c = "Головоломки"
d = "Аркады"
e = "Хорроры"
f = "Симуляторы"
g = "ММО"
h = "Приключения"
i = "Выживалки"
j = "Гонки"
k = "Песочницы"

games = [a,b,c,d,e,f,g,h,i,j,k]
students = ["Аркадий","Богдан","Вилен","Назар","Никита Ч","Никита М","Даниил","София","Дарья","Артём","Степан",]
random.shuffle(games)
random.shuffle(students)

for i in range(11):
    print(students[i],"-",games[i])



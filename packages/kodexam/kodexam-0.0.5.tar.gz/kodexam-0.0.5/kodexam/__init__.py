
class izi:
    def pract(number=''):
        #1
        sklad = {
#1-17-19
            'Написать программу с':'Написать программу с интерактивным консольным меню (т.е. вывод списка действий по цифрам) по вычислению площади круга (родительский класс), длины окружности (подкласс) и объема шара (подкласс) по задаваемому с клавиатуры радиусу. Содержание меню: 1. Вычислить площадь круга. 2. Вычислить длину окружности. 3. Вычислить объем шара.\n\
\n\
from math import pi\n\
class RoundOne():\n\
def __init__(self, radius):\n\
self.radius = radius\n\
def square_calculate(self):\n\
return pi * self.radius ** 2\n\
class RoundTwo(RoundOne):\n\
def __init__(self, radius):\n\
super().__init__(radius)\n\
def lenght_calculate(self):\n\
return 2 * pi * self.radius\n\
class RoundThree(RoundTwo):\n\
def __init__(self, radius):\n\
super().__init__(radius)\n\
def value_calculate(self):\n\
return pi * self.radius ** 3 * 4 / 3\n\
def choice(x):\n\
print("Input radius: ")\n\
radius = int(input())\n\
circle = RoundThree(radius)\n\
if x == 1:\n\
return circle.square_calculate()\n\
if x == 2:\n\
return circle.lenght_calculate()\n\
if x == 3:\n\
return circle.value_calculate()\n\
def mainloop():\n\
while True:\n\
print("Input your activity:")\n\
print("0: EXIT")\n\
print("1: SQUARE")\n\
print("2: LENGHT")\n\
print("3: VALUE")\n\
i = int(input())\n\
if i == 0:\n\
return\n\
else:\n\
print(choice(i))\n\
print("______________________________")\n\
mainloop()\n\
\n\
\n\
\n\
\n\
\n\
Написать программу с интерактивным консольным меню (т.е. вывод списка действий по цифрам) по удалению из списка (задаем с клавиатуры) элемента с задаваемым с клавиатуры индексом (например, m). При решении задачи необходимо использовать функцию map. Содержание меню: 1. Удалить элемент из списка и вывести итоговый список. 2. Удалить элемент из списка и вывести его номер(а).  (20 баллов)\n\
def f(x, m):\n\
    global z\n\
    if x == m:\n\
        for i in range(len(z)):\n\
            if z[i] == x:\n\
                z[i] = None\n\
                return z[i]\n\
    else:\n\
        return x\n\
\n\
\n\
def choice(x, m):\n\
    global z\n\
    if x == 1:\n\
        z = list(map(lambda x: f(x, m), z))\n\
        z = list(filter(lambda x: x != None, z))\n\
        return z\n\
\n\
    if x == 2:\n\
        ind = []\n\
        z = list(map(lambda x: f(x, m), z))\n\
        for i in range(len(z)):\n\
            if z[i] == None:\n\
                ind.append(i + 1)\n\
        return ind\n\
\n\
\n\
z = []\n\
\n\
\n\
def mainloop():\n\
    global z\n\
    while True:\n\
        print("Input your list and index:")\n\
        z, m = list(map(int, input().split())), int(input())\n\
        print("Input your activity:")\n\
        print("0: EXIT")\n\
        print("1: DELETE OUTPUT LIST")\n\
        print("2: DELETE OUTPUT INDEX")\n\
        i = int(input())\n\
        if i == 0:\n\
            return\n\
        else:\n\
            print(choice(i, m))\n\
            print("______________________________")\n\
\n\
\n\
mainloop()\n\
\n\
\n\
\n\
\n\
\n\
Написать программу с интерактивным консольным меню (т.е. вывод списка действий по цифрам) по вычислению площади прямоугольника (родительский класс), и периметра прямоугольника (дочерний класс) по задаваемой с клавиатуры длине сторон прямоугольника.\n\
Содержание меню: 1. Вычислить площадь прямоугольника. 2. Вычислить периметр прямоугольника. (20 баллов)\n\
class Rectangle1():\n\
    def __init__(self, a, b):\n\
        self.a = a\n\
        self.b = b\n\
\n\
    def square(self):\n\
        return self.a * self.b\n\
\n\
\n\
class Rectangle2(Rectangle1):\n\
    def __init__(self, a, b):\n\
        super().__init__(a, b)\n\
\n\
    def perimetr(self):\n\
        return self.a * 2 + self.b * 2\n\
\n\
\n\
def choice(x):\n\
    print("Input a and b: ")\n\
    a, b = map(int,input().split())\n\
    rect = Rectangle2(a, b)\n\
    if x == 1:\n\
        return rect.square()\n\
    if x == 2:\n\
        return rect.perimetr()\n\
\n\
\n\
def mainloop():\n\
    while True:\n\
        print("Выберите задание:")\n\
        print("0: СТОП")\n\
        print("1: ПЛОЩАДЬ")\n\
        print("2: ПЕРИМЕТР")\n\
        i = int(input())\n\
        if i == 0:\n\
            return\n\
        else:\n\
            print(choice(i))\n\
            print("______________________________")\n\
mainloop()'
            ,
#2-4-6-8-14-26
            'Создать класс стек':'Создать класс стек. Использовать способ реализации стека через list. Поменять местами первый и последний элементы стека.\n\
class stack:\n\
def init(self):\n\
self.items = []\n\
def push(self, item):\n\
self.items.append(item)\n\
def pop(self):\n\
self.items[0], self.items[-1] = self.items[-1], self.items[0]\n\
return self.items\n\
s = stack()\n\
list1 = []\n\
n = input()\n\
n = n.split()\n\
for i in range(len(n)):\n\
list1.append(n[i])\n\
for i in list1:\n\
s.push(i)\n\
print(*s.pop())\n\
\n\
\n\
\n\
\n\
\n\
Создать класс стек. Использовать способ реализации стека через list. Удалить элемент, который находится в середине стека, если нечетное число элементов, а если четное, то два средних.\n\
class stack:\n\
def init(self):\n\
self.items = []\n\
def push(self, item):\n\
self.items.append(item)\n\
def pop(self):\n\
a = len(self.items)\n\
if len(self.items)%2!=0:\n\
self.items.pop(a//2)\n\
return self.items\n\
else:\n\
self.items.pop(a//2)\n\
b = len(self.items)\n\
self.items.pop(b//2)\n\
return self.items\n\
s = stack()\n\
list1 = []\n\
n = input()\n\
n = n.split()\n\
for i in range(len(n)):\n\
list1.append(n[i])\n\
for i in list1:\n\
s.push(i)\n\
print(*s.pop()) \n\
\n\
\n\
\n\
\n\
\n\
Создать класс стек. Использовать способ реализации стека через list. Удалить каждый второй элемент стека.\n\
class stack:\n\
def init(self):\n\
self.items = []\n\
def push(self, item):\n\
self.items.append(item)\n\
def pop(self):\n\
return self.items[0::2]\n\
s = stack()\n\
list1 = []\n\
n = input()\n\
n = n.split()\n\
for i in range(len(n)):\n\
list1.append(n[i])\n\
for i in list1:\n\
s.push(i)\n\
print(*s.pop())\n\
\n\
\n\
\n\
\n\
\n\
Создать класс стек. Использовать способ реализации стека через list. Найти минимальный элемент стека и вставить после него «0».\n\
class stack:\n\
def init(self):\n\
self.items = []\n\
def push(self, item):\n\
self.items.append(item)\n\
def pop(self):\n\
s = ''\n\
a = min(self.items)\n\
for i in range(len(self.items)):\n\
if self.items[i]!=a:\n\
s+=self.items[i]\n\
s+=" "\n\
else:\n\
s+=self.items[i]\n\
s+=" 0 "\n\
return s\n\
s = stack()\n\
list1 = []\n\
n = input()\n\
n = n.split()\n\
for i in range(len(n)):\n\
list1.append(n[i])\n\
for i in list1:\n\
s.push(i)\n\
print(s.pop())\n\
\n\
\n\
\n\
\n\
\n\
Создать класс стек. Использовать способ реализации стека через list. Удалить минимальный элемент стека.\n\
class Stack:\n\
    def __init__(self):\n\
        self.stack = []\n\
\n\
    def is_empty(self):\n\
        return len(self.stack) == 0\n\
\n\
    def push(self, item):\n\
        self.stack.append(item)\n\
\n\
    def pop(self):\n\
        if self.is_empty():\n\
            return "Стек пуст"\n\
        return self.stack.pop()\n\
\n\
    def peek(self):\n\
        if self.is_empty():\n\
            return "Стек пуст"\n\
        return self.stack[-1]\n\
\n\
    def remove_min(self):\n\
        if self.is_empty():\n\
            return "Стек пуст"\n\
        min_element = min(self.stack)\n\
        self.stack.remove(min_element)\n\
        return min_element\n\
stack = Stack()\n\
stack.push(5)\n\
stack.push(3)\n\
stack.push(9)\n\
stack.push(1)\n\
\n\
print(stack.stack)  # Выводит: [5, 3, 9, 1]\n\
\n\
min_element = stack.remove_min()\n\
print(min_element)  # Выводит: 1\n\
\n\
print(stack.stack)  # Выводит: [5, 3, 9]\n\
\n\
\n\
\n\
\n\
\n\
Создать класс стек. Использовать способ реализации стека через list. Сформировать стек с элементами - строками. Прочитать три нижних элемента стека и поменять местами верхний и нижний элементы. (20 баллов)\n\
class Stack(list):\n\
    \n\
    def __init__(self):\n\
        self.stack = []\n\
    def push(self, item):\n\
        self.stack.append(item)\n\
    def pop(self):\n\
        if len(self.stack) == 0:\n\
            return None\n\
        return self.stack.pop()\n\
    def change(self):\n\
        if len(self.stack) == 0:\n\
            raise IndexError("Больше нет элементов!")\n\
        else:\n\
            a = self.stack[-1]\n\
            b = self.stack[0]\n\
            del self.stack[-1]\n\
            del self.stack[0]\n\
            self.stack.append(b)\n\
            self.stack.insert(0, a)\n\
\n\
    def __str__ (self):\n\
        return str(self.stack)\n\
\n\
#Пример\n\
    \n\
example = Stack()\n\
example.push("a")\n\
example.push("b")\n\
example.push("c")\n\
example.push("d")\n\
example.change()\n\
print(example)\n\
example.change()\n\
example.pop()\n\
print(example.pop())\n\
print(example.pop())'
            ,
#3-27
            'Дан список А3':'Дан список А3, состоящий из четного количества элементов. Используя функцию (функции) высшего порядка разбейте его на списки В, С так, чтобы в одном были положительные элементы, а в другом отрицательные.\n\
a = [1, 2, 3, 4, -5, -6]\n\
b = list(filter(lambda x: x >= 0, a))\n\
c = list(filter(lambda x: x < 0, a))\n\
print(b)\n\
print(c)\n\
\n\
\n\
\n\
\n\
\n\
Дан список А3, состоящий из четного количества элементов. Используя функцию(функции) высшего порядка разбейте его на списки В, С так, чтобы в одном были положительные элементы, а в другом отрицательные. (20 баллов)\n\
a = [1, 2, 3, 4, -5, -6]\n\
b = list(filter(lambda x: x >= 0, a))\n\
c = list(filter(lambda x: x < 0, a))\n\
print(b)\n\
print(c)'
            ,
#5
            'Создать класс Plane':'5.	Создать класс Plane (самолетов), имеющий атрибуты: название самолета, количество пассажиров на борту, курс движения (откуда и куда). Методы: - определить загрузку самолета, если максимальная вместимость =200 пассажиров; – определить все имена самолетов, летящих по одному маршруту; - определить среднюю загрузку всех самолетов.\n\
class Plane:\n\
    def __init__(self, name, passengers, route):\n\
        self.name = name\n\
        self.passengers = passengers\n\
        self.route = route\n\
\n\
    def calculate_load(self):\n\
        max_capacity = 200\n\
        load_percentage = (self.passengers / max_capacity) * 100\n\
        return load_percentage\n\
\n\
    @staticmethod\n\
    def find_planes_by_route(planes, route):\n\
        matching_planes = [plane.name for plane in planes if plane.route == route]\n\
        return matching_planes\n\
\n\
    @staticmethod\n\
    def calculate_average_load(planes):\n\
        total_passengers = sum(plane.passengers for plane in planes)\n\
        total_planes = len(planes)\n\
        average_load = total_passengers / total_planes\n\
        return average_load\n\
# Создание экземпляров самолетов\n\
plane1 = Plane("Boeing 747", 150, "New York - London")\n\
plane2 = Plane("Airbus A320", 180, "Paris - Rome")\n\
plane3 = Plane("Boeing 777", 200, "Tokyo - Sydney")\n\
plane4 = Plane("Embraer E190", 120, "New York - London")\n\
plane5 = Plane("Boeing 787", 220, "Paris - Rome")\n\
\n\
# Определение загрузки каждого самолета\n\
load1 = plane1.calculate_load()\n\
load2 = plane2.calculate_load()\n\
load3 = plane3.calculate_load()\n\
load4 = plane4.calculate_load()\n\
load5 = plane5.calculate_load()\n\
\n\
print(f"Загрузка самолета {plane1.name}: {load1}%")\n\
print(f"Загрузка самолета {plane2.name}: {load2}%")\n\
print(f"Загрузка самолета {plane3.name}: {load3}%")\n\
print(f"Загрузка самолета {plane4.name}: {load4}%")\n\
print(f"Загрузка самолета {plane5.name}: {load5}%")\n\
\n\
# Определение всех имен самолетов, летящих по одному маршруту\n\
planes = [plane1, plane2, plane3, plane4, plane5]\n\
matching_planes = Plane.find_planes_by_route(planes, "New York - London")\n\
print(f"Самолеты, летящие по маршруту New York - London: {matching_planes}")\n\
\n\
# Определение средней загрузки всех самолетов\n\
average_load = Plane.calculate_average_load(planes)\n\
print(f"Средняя загрузка всех самолетов: {average_load}")'
            ,
#7-54
            'Дано предложение без':'7.	Дано предложение без знаков препинания. Превратить предложение в список слов. При помощи механизма map/filter/reduce отбросить у каждого слова последнюю букву и склеить в одну строку те обрезанные слова, длина которых больше 5. \n\
from functools import reduce\n\
s = "ABC dfg hhhh klklklk g jfhgidjfhguid dfdf"\n\
print(reduce(lambda x, y: x + y, list(filter(lambda x: len(x) > 5, list(map(lambda x: x[:-1],\n\
s.split())))))) \n\
\n\
\n\
\n\
\n\
\n\
Дано предложение без знаков препинания. Превратить предложение в список слов. При помощи механизма map/filter/reduce найти количество слов, длина которых больше 4 и склеить их в одну строку (20 баллов)\n\
lst = "eeny meeny money moe do they love u no they dont"\n\
lst = lst.split(" ")\n\
a = list(filter(lambda x: len(x)>4, lst)) # отбирает только слова больше 4 сим-в\n\
print("".join(a))'
            ,
#9-29
            'Дан список S':'9.	Дан список S состоящий из N различных элементов. Вывести индексы четных элементов списка. Использовать встроенные функции высшего порядка.\n\
s = [1, 2, 3, 4]\n\
print(list(map(lambda x: print(s.index(x)) if x % 2 == 0 else x, s)))\n\
\n\
\n\
\n\
\n\
\n\
Дан список S состоящий из N различных элементов. Вывести индексы четных элементов списка. Использовать функции высшего порядка. (20 баллов)\n\
s = [1, 2, 3, 4, 5, 6]\n\
list(map(lambda x: print(s.index(x)) if x % 2 == 0 else x, s))'
            ,
#10-18-52
            'Построить базовый класс':'КОМПЬЮТЕРЫ Задание: построить базовый класс с указанными в таблице полями и методами:\n\
- конструктор; - функция, которая определяет «качество» объекта – Q по заданной формуле; - метод вывода информации об объекте.\n\
Построить дочерний класс (класс-потомок), который содержит:\n\
- дополнительное поле P;\n\
- функция, которая определяет «качество» объекта дочернего класса – Qp и перегружает функцию качества родительского класса (Q), выполняя вычисление по новой формуле.\n\
Создать проект для демонстрации работы: ввод и вывод информации об объектах классов\n\
Поля и методы базового класса	Поля и методы дочернего класса\n\
Компьютер:\n\
- наименование процессора;\n\
- тактовая частота процессора (МГц);\n\
- объем оперативной памяти (Мб);\n\
- Q = (0,1·частота) + память	P: объем накопителя SSD (Гб)\n\
- Qp = Q +0,5P\n\
\n\
class Computer:\n\
    def __init__(self, processor_name, processor_speed, memory):\n\
        self.processor_name = processor_name\n\
        self.processor_speed = processor_speed\n\
        self.memory = memory\n\
\n\
    def calculate_quality(self):\n\
        quality = 0.1 * self.processor_speed + self.memory\n\
        return quality\n\
\n\
    def display_info(self):\n\
        print("Computer Information:")\n\
        print(f"Processor: {self.processor_name}")\n\
        print(f"Processor Speed: {self.processor_speed} MHz")\n\
        print(f"Memory: {self.memory} MB")\n\
\n\
\n\
class ComputerPlus(Computer):\n\
    def __init__(self, processor_name, processor_speed, memory, ssd_capacity):\n\
        super().__init__(processor_name, processor_speed, memory)\n\
        self.ssd_capacity = ssd_capacity\n\
\n\
    def calculate_quality(self):\n\
        quality = super().calculate_quality() + 0.5 * self.ssd_capacity\n\
        return quality\n\
\n\
computer1 = Computer("Intel Core i5", 2500, 8192)\n\
computer2 = ComputerPlus("AMD Ryzen 7", 3800, 16384, 500)\n\
\n\
computer1.display_info()\n\
quality1 = computer1.calculate_quality()\n\
print(f"Quality: {quality1}")\n\
\n\
print()\n\
\n\
computer2.display_info()\n\
quality2 = computer2.calculate_quality()\n\
print(f"Quality: {quality2}")\n\
\n\
\n\
\n\
\n\
\n\
Задание: построить базовый класс с указанными в таблице полями и методами:\n\
- конструктор; - функция, которая определяет «качество» объекта – Q по заданной формуле; - метод вывода информации об объекте.\n\
Построить дочерний класс (класс-потомок), который содержит:\n\
- дополнительное поле P;\n\
- функция, которая определяет «качество» объекта дочернего класса – Qp и перегружает функцию качества родительского класса (Q), выполняя вычисление по новой формуле.\n\
Создать проект для демонстрации работы: ввод и вывод информации об объектах классов. (20 баллов)\n\
Поля и методы базового класса Поля и методы дочернего класса\n\
Автомобиль:\n\
- марка автомобиля;\n\
- мощность двигателя (кВт);\n\
- число мест;\n\
- Q = 0,1·мощность ·число мест P: год выпуска\n\
- Qp = Q - 1,5·(T-P),\n\
где T – текущий год\n\
\n\
import datetime\n\
\n\
class Car:\n\
    def init(self, marka, moshnost, chislo_mest):\n\
        self.marka = marka\n\
        self.moshnost = moshnost\n\
        self.chislo_mest = chislo_mest\n\
    \n\
    def kachestvo(self):\n\
        return 0.1 * self.moshnost * self.chislo_mest\n\
    \n\
    def info(self):\n\
        print("Марка:", self.marka)\n\
        print("Мощность двигателя (кВт):", self.moshnost)\n\
        print("Число мест:", self.chislo_mest)\n\
        print("Качество:", self.kachestvo())\n\
\n\
class ChildCar(Car):\n\
    def init(self, marka, moshnost, chislo_mest, date):\n\
        super().init(marka, moshnost, chislo_mest)\n\
        self.P = date\n\
    \n\
    def kachestvo(self):\n\
        year1 = datetime.datetime.now().year\n\
        T = year1\n\
        return super().kachestvo() - 1.5 * (T - self.P)\n\
    \n\
#Пример\n\
car1 = Car("БМВ", 100, 5)\n\
car2 = ChildCar("МЕРСЕДЕС", 150, 4, 2015)\n\
\n\
car1.info()\n\
print()  \n\
car2.info()\n\
\n\
\n\
\n\
\n\
\n\
КОМПЬЮТЕРЫ Задание: построить базовый класс с указанными в таблице полями и методами:\n\
- конструктор; - функция, которая определяет «качество» объекта – Q по заданной формуле; - метод вывода информации об объекте.\n\
Построить дочерний класс (класс-потомок), который содержит:\n\
- дополнительное поле P;\n\
- функция, которая определяет «качество» объекта дочернего класса – Qp и перегружает функцию качества родительского класса (Q), выполняя вычисление по новой формуле.\n\
Создать проект для демонстрации работы: ввод и вывод информации об объектах классов. (20 баллов)\n\
Поля и методы базового класса	Поля и методы дочернего класса\n\
Компьютер:\n\
- наименование процессора;\n\
- тактовая частота процессора (МГц);\n\
- объем оперативной памяти (Мб);\n\
- Q = (0,1·частота) + память	P: объем накопителя SSD (Гб)\n\
- Qp = Q +0,5P\n\
\n\
class Computer:\n\
    def __init__(self, processor_name, processor_speed, memory):\n\
        self.processor_name = processor_name\n\
        self.processor_speed = processor_speed\n\
        self.memory = memory\n\
\n\
    def quality(self):\n\
        return 0.1 * self.processor_speed + self.memory\n\
\n\
    def display_info(self):\n\
        print("Computer Information:")\n\
        print("Processor Name:", self.processor_name)\n\
        print("Processor Speed (MHz):", self.processor_speed)\n\
        print("Memory (MB):", self.memory)\n\
        print("Quality (Q):", self.quality())\n\
\n\
\n\
class ImprovedComputer(Computer):\n\
    def __init__(self, processor_name, processor_speed, memory, ssd_capacity):\n\
        super().__init__(processor_name, processor_speed, memory)\n\
        self.ssd_capacity = ssd_capacity\n\
\n\
    def quality(self):\n\
        return super().quality() + 0.5 * self.ssd_capacity\n\
\n\
    def display_info(self):\n\
        print("Improved Computer Information:")\n\
        print("Processor Name:", self.processor_name)\n\
        print("Processor Speed (MHz):", self.processor_speed)\n\
        print("Memory (MB):", self.memory)\n\
        print("SSD Capacity (GB):", self.ssd_capacity)\n\
        print("Quality (Qp):", self.quality())\n\
\n\
\n\
# Пример использования классов\n\
\n\
# Создание объекта базового класса\n\
computer = Computer("Intel Core i5", 2500, 8192)\n\
computer.display_info()\n\
\n\
# Создание объекта дочернего класса\n\
improved_computer = ImprovedComputer("AMD Ryzen 7", 3500, 16384, 512)\n\
improved_computer.display_info()'
            ,
#11-13-45
            'Реализовать декоратор с':'Реализовать декоратор с именем not_none, который генерирует исключительную ситуацию если декорируемая функция вернула значения None.\n\
def not_none(func):\n\
def inner(x):\n\
if func(x) == None:\n\
return "!!!ERROR!!!"\n\
else:\n\
return func(x)\n\
return inner\n\
def f(x):\n\
if x == 0:\n\
return None\n\
return 1\n\
f = not_none(f)\n\
print(f(1)) \n\
\n\
\n\
\n\
\n\
\n\
Реализовать декоратор с именем print_type, выводящий на печать тип значения, возвращаемого декорируемой функцией. (20 баллов)\n\
def print_type(func):\n\
    def inner(x):\n\
        print(type(func(x)))\n\
        return func(x)\n\
\n\
    return inner\n\
\n\
\n\
def f(x):\n\
    return x\n\
\n\
f = print_type(f)\n\
print(f(1))\n\
\n\
\n\
\n\
\n\
\n\
Реализовать декоратор с именем not_sum, который генерирует исключительную ситуацию, если декорируемая функция вернула отрицательное значение суммы трех чисел. (20 баллов)\n\
def not_sum(funct):\n\
    def wrapper(a,b,c):\n\
        funct(a,b,c)\n\
        assert funct(a,b,c) > 0, «Отрицательное значение»\n\
    return wrapper\n\
\n\
@not_sum\n\
def func(a,b,c):\n\
    return a+b+c\n\
func(10,-1,-1)\n\
\n\
\n\
\n\
\n\
\n\
\n\
# Пример данных\n\
a = 5\n\
b = -10\n\
c = 15\n\
\n\
try:\n\
    sum_result = calculate_sum(a, b, c)\n\
    print("Сумма трех чисел:", sum_result)\n\
except Exception as e:\n\
    print("Исключительная ситуация:", str(e))\n\
'
            ,
#12
            'Создайте класс Speed':'Создайте класс Speed (Скорость), имеющий атрибуты: value (значение), unit (единица измерения). При изменении единицы измерения значение должно соответственно меняться. Например, при переходе от км/ч к м/с и наоборот. Например, 20 км/ч = 5.56 м/с. Допустимые значения свойства unit: ‘м/с’, ‘км/ч’. Организуйте эту проверку. Продемонстрируйте работу с классом. (20 баллов)\n\
class Speed:\n\
    def init(self):\n\
        self.items = []\n\
\n\
    def value(self, item):\n\
        self.items.append(item)\n\
\n\
    def unit(self, item1):\n\
        self.items.append(item1)\n\
\n\
    def chet(self):\n\
        if self.items[1] == "км/ч":\n\
            return round(int(self.items[0]) / 3.6, 2), "м/c"\n\
        else:\n\
            return int(self.items[0]) * 3.6, "км/ч"\n\
\n\
\n\
#Пример\n\
speed = Speed()\n\
speed.value(100)  # Значение скорости: 100\n\
speed.unit("км/ч")  # Единица измерения: "км/ч"\n\
result, unit = speed.chet()\n\
print(f"Результат: {result} {unit}")'
            ,
#15
            'Задано положительное и':'Задано положительное и отрицательное число в двоичной системе. Составить программу вычисления суммы этих чисел, используя функцию сложения чисел в двоичной системе счисления. Использовать рекурсию. (20 баллов)\n\
def func(n1):\n\
    result1 = ""\n\
    if "-" in n1:\n\
        n1 = n1.replace("-", "")\n\
        result1+="-"\n\
        result1+=str(int(n1, 2))\n\
    else:\n\
        result1+=str(int(n1,2))\n\
    return result1\n\
\n\
\n\
n1, n2 = input(), input() #например: 101100 и -1000\n\
result = func(n1)\n\
result2 = func(n2)\n\
total = result + "+" + result2\n\
print(str(bin(eval(total))).replace("0b", ""))'
            ,
#16-34
            'Вывести по убыванию':'Вывести по убыванию количество всех предыдущих ремонтов машин "Жигули". Реализовать с помощью алгоритма сортировки слиянием.\n\
from random import randint\n\
numbers = [randint(1, 20) for _ in range (30)]\n\
numbers = [38, 27, 43, 3, 9, 82, 10] # пример\n\
def merge_sort(array: list):\n\
    if len(array) > 1: \n\
        mid = len(array) // 2\n\
        left = array[:mid] \n\
        right = array[mid:] \n\
        merge_sort(left)\n\
        merge_sort(right)\n\
\n\
        i, j, k= 0, 0, 0\n\
        while i < len(left) and j < len(right):\n\
            if left[i] < right[j]:\n\
                array[k] = left[i]\n\
                i += 1\n\
            else:\n\
                array[k] = right[j]\n\
                j += 1\n\
            k += 1\n\
            print(1, array)\n\
        while i < len(left): \n\
            array[k] = left[i]\n\
            i += 1\n\
            k += 1\n\
            print(2, array)\n\
        while j < len(right): \n\
            array[k] = right[j]\n\
            j += 1\n\
            k += 1\n\
            print(3, array)\n\
\n\
print (numbers)\n\
merge_sort(numbers)\n\
print ("result:", numbers)\n\
\n\
\n\
\n\
\n\
\n\
Вывести по убыванию количество всех предыдущих ремонтов машин "Жигули". Реализовать с помощью алгоритма сортировки слиянием.\n\
from random import randint\n\
numbers = [randint(1, 20) for _ in range (30)]\n\
numbers = [38, 27, 43, 3, 9, 82, 10] # пример\n\
def merge_sort(array: list):\n\
    if len(array) > 1: \n\
        mid = len(array) // 2\n\
        left = array[:mid] \n\
        right = array[mid:] \n\
        merge_sort(left)\n\
        merge_sort(right)\n\
\n\
        i, j, k= 0, 0, 0\n\
        while i < len(left) and j < len(right):\n\
            if left[i] < right[j]:\n\
                array[k] = left[i]\n\
                i += 1\n\
            else:\n\
                array[k] = right[j]\n\
                j += 1\n\
            k += 1\n\
            print(1, array)\n\
        while i < len(left): \n\
            array[k] = left[i]\n\
            i += 1\n\
            k += 1\n\
            print(2, array)\n\
        while j < len(right): \n\
            array[k] = right[j]\n\
            j += 1\n\
            k += 1\n\
            print(3, array)\n\
\n\
print (numbers)\n\
merge_sort(numbers)\n\
print ("result:", numbers)'
            ,
#20-24
            'Дан кольцевой список':'Дан кольцевой список с перечнем товаров. Выбрать все товары, изготовленные фирмой Bosh и создать из них новый список. (20 баллов)\n\
class CircleList:\n\
    def __init__ (self):\n\
        self.circle = []\n\
        self.__index = -1\n\
    def append(self, elem):\n\
        if len(self.circle) != 0:\n\
            self.circle.append([elem, 0])\n\
            self.circle[-2][1] = len(self.circle) - 1\n\
        else:\n\
            self.circle.append([elem, 0])\n\
    def sappend(self, elem):\n\
        if len(self.circle) != 0:\n\
            for i in range(len(self.circle) - 1):\n\
                self.circle[i][1] += 1\n\
            self.circle.insert(0, [elem, 1])\n\
        else:\n\
            self.circle.append([elem, 0])\n\
    def pop(self):\n\
        if len(self.circle) > 1:\n\
            result = self.circle[-1][0]\n\
            self.circle[-2][1] = 0\n\
            del self.circle[-1]\n\
        elif len(self.circle) == 1:\n\
            result = self.circle[-1][0]\n\
            del self.circle[-1]\n\
        else:\n\
            return None\n\
        return result\n\
    def get(self): \n\
        self.__index = self.circle[self.__index] [1]\n\
        return self.circle[self.__index] [0]\n\
    def __str_(self):\n\
        return str(self.circle)\n\
\n\
#Пример\n\
a = CircleList()\n\
a.append("Bosh")\n\
a.append("Sony")\n\
a.sappend("Dyson")\n\
a.sappend("Haier")\n\
result_list = []\n\
while True:\n\
    element = a.pop()\n\
    if element != None:\n\
        if "Bosh" in element:\n\
            result_list.append (element)\n\
    else:\n\
        break\n\
print(*result_list)\n\
\n\
\n\
\n\
\n\
\n\
Дан кольцевой список из 20 фамилий студентов. Разбить студентов на 2 группы по 10 человек. Во вторую группу попадает каждый 12-й человек. (20 баллов)\n\
students = []\n\
for i in range(20):\n\
    students.append(f"st{i+1}")\n\
second_group = []\n\
while len(second_group) < 10:\n\
    try:\n\
        choice = students[11]\n\
        second_group. append (choice)\n\
        del students[11]\n\
        students = students[11:] + students[:11]\n\
    except IndexError:\n\
        students_copy = students[:] + students[:]\n\
        choice = students_copy[11]\n\
        second_group. append (choice)\n\
first_group = set(students) - set (second_group)\n\
print ("Первая группа:", *first_group)\n\
print ("Вторая группа:", *second_group)'
            ,
#21
            'С помощью функции':'С помощью функции reduce() вычислить двойной факториал заданного натурального числа n (для четного или нечетного n). (20 баллов)\n\
from functools import reduce\n\
n = 5\n\
print(reduce(lambda x, y: x * y if y % 2 == n % 2 else x, [i for i in range(1, n + 1)]))\n\
'
            ,
#22
            'Создайте класс Заказ':'Создайте класс Заказ(Order), у которого есть свойства код_товара(code), цена(price), количество(count) и методы __init__ и __str__. Создайте 2 класса-потомка: Опт(Opt) и Розница(Retail). В этих классах создайте методы __init__, __str__ и сумма_заказа (summa), позволяющий узнать стоимость заказа. Для опта стоимость единицы товара составляет 95% от цены, а при покупке более 500 штук – 90% цены. В розницу стоимость единицы товара составляет 100% цены. Стоимость заказа равна произведению цены на количество. Создайте список, содержащий по 2 объекта каждого класса (Order, Opt, Retail). Для этого списка:\n\
•	выведите информацию о каждом объекте с помощью метода __str__;\n\
•	найдите общую стоимость заказов для объектов Opt и Retail. (20 баллов)\n\
class Order:\n\
    def __init__(self, code, price, count):\n\
        self.code = code\n\
        self.price = price\n\
        self.count = count\n\
    \n\
    def __str__(self):\n\
        return f"Товар {self.code} стоимостью {self.price} за шт.\nв количестве {self.count} шт."\n\
\n\
\n\
class Opt(Order):\n\
    def __init__(self, code, price, count):\n\
        super().__init__(code, price, count)\n\
        if count <= 500:\n\
            self.summa = price * count * 0.95\n\
        else:\n\
            self.summa = price * count * 0.9\n\
    \n\
    def __str__(self):\n\
        return f"Товар {self.code} стоимостью {self.price} за шт.\nв количестве {self.count} шт. Итоговая цена: {self.summa}"\n\
    \n\
    def summa_zakaza(self):\n\
        return self.summa\n\
\n\
\n\
class Retail(Order):\n\
    def __init__(self, code, price, count):\n\
        super().__init__(code, price, count)\n\
        self.summa = price * count\n\
    \n\
    def __str__(self):\n\
        return f"Товар {self.code} стоимостью {self.price} за шт.\nв количестве {self.count} шт. Итоговая цена: {self.summa}"\n\
    \n\
    def summa_zakaza(self):\n\
        return self.summa\n\
\n\
\n\
# Пример\n\
a = Order("молоко_1", 80, 40)\n\
b = Order("молоко_2", 98, 10)\n\
c = Opt("шоколад_1", 119, 700)\n\
d = Opt("шоколад_2", 39, 300)\n\
e = Retail("хлеб", 48, 2)\n\
f = Retail("мороженое", 99, 1)\n\
\n\
orders = [a, b, c, d, e, f]\n\
for elem in orders:\n\
    print(elem)\n\
\n\
opt_retail_orders = [c, d, e, f]\n\
total_opt_retail_sum = sum(order.summa_zakaza() for order in opt_retail_orders)\n\
print(f"Общая стоимость заказов для объектов Opt и Retail: {total_opt_retail_sum}")\n\
'
            ,
#23
            'Создать класс Деньги':'Создать класс Деньги для работы с денежными суммами. Число должно быть представлено списком, состоящим из рублей и копеек. Реализовать сложение, вычитание, деление сумм, деление денежных сумм. (20 баллов)\n\
class M():\n\
    summa = [0, 0]\n\
\n\
    def __init__(self, money, digit):\n\
        self.summa[0] = money\n\
        self.summa[1] = digit\n\
\n\
    def plus(self, item1, item2):\n\
        self.summa[0] += item1 + (self.summa[1] + item2) // 100\n\
        self.summa[1] = (self.summa[1] + item2) % 100\n\
\n\
    def minus(self, item1, item2):\n\
        self.summa[0] -= item1 - (self.summa[1] - item2) // 100\n\
        self.summa[1] = (self.summa[1] - item2) % 100\n\
\n\
    def delen(self, mn):\n\
        self.summa[0] /= mn\n\
        self.summa[1] /= mn\n\
\n\
    def delends(self, item1, item2):\n\
        return (self.summa[0] + self.summa[1]/100) / (item1 + item2/100)\n\
\n\
#Пример\n\
    \n\
den = M(100, 15)\n\
print(den.delends(2, 7))\n\
print(den.summa)\n\
'
            ,
#25
            'Составить программу для':'Составить программу для нахождения числа, которое образуется из данного натурального числа при записи его цифр в обратном порядке. Например, для числа 1234 получаем результат 4321. Использовать рекурсию. (20 баллов)\n\
def func(n):\n\
    global string\n\
    while n:\n\
        string += str(n % 10)\n\
        n //= 10\n\
        return func(n)\n\
\n\
\n\
string = ""\n\
func(int(input()))\n\
print(string)'
            ,
#28
            'Создайте класс Студент':'Создайте класс Студент, имеющий: \n\
•	закрытый атрибут Имя – строка, содержащая фамилию; \n\
•	метод __init__. При создании объекта указывается имя, список Дисциплины пустой; \n\
•	закрытый атрибут Дисциплины – словарь сданных дисциплин. Ключом является название дисциплины, значением – оценка. \n\
•	метод put добавляет новую дисциплину в атрибут Дисциплины. Параметрами метода являются название дисциплины и оценка; \n\
•	свойство Сдано возвращает список названий сданных дисциплин; Создайте экземпляр класса, продемонстрируйте работу с атрибутами, методами и свойствами. (20 баллов)\n\
class Student:\n\
\n\
    def __init__(self, name: str):\n\
        self. name = name\n\
        self.__subjects = dict()\n\
\n\
    def put(self, subject: str, mark: int):\n\
        self.__subjects.setdefault (subject, mark)\n\
\n\
    @property\n\
    def passed(self):\n\
        return list(self.__subjects.items())\n\
\n\
me = Student("Kondrashov")\n\
me.put("Math", 5)\n\
me.put("Programming", 5)\n\
me.put("History", 4)\n\
print(me.passed)'
            ,
#30-36
            'Дан однонаправленный связный':'Дан однонаправленный связный список. Вставить элемент после n-го элемента списка. (20 баллов)\n\
class Node:\n\
    def __init__(self, data=None):\n\
        self.data = data\n\
        self.next = None\n\
\n\
\n\
class LinkedList:\n\
    def __init__(self):\n\
        self.head = None\n\
\n\
    def insert_after(self, n, data):\n\
        if n < 0:\n\
            raise ValueError("Индекс должен быть неотрицательным числом!")\n\
\n\
        new_node = Node(data)\n\
\n\
        if n == 0:\n\
            new_node.next = self.head\n\
            self.head = new_node\n\
        else:\n\
            current = self.head\n\
            count = 0\n\
\n\
            while current and count < n:\n\
                current = current.next\n\
                count += 1\n\
\n\
            if not current:\n\
                raise IndexError("Индекс превышает длину списка!")\n\
\n\
            new_node.next = current.next\n\
            current.next = new_node\n\
\n\
    def insert_at_head(self, data):\n\
        new_node = Node(data)\n\
        new_node.next = self.head\n\
        self.head = new_node\n\
\n\
    def display(self):\n\
        current = self.head\n\
\n\
        while current:\n\
            print(current.data)\n\
            current = current.next\n\
\n\
\n\
\n\
linked_list = LinkedList()\n\
\n\
linked_list.insert_at_head("Элемент 1")\n\
linked_list.insert_at_head("Элемент 2")\n\
linked_list.insert_at_head("Элемент 3")\n\
linked_list.insert_at_head("Элемент 4")\n\
\n\
print("Список до вставки:")\n\
linked_list.display()\n\
\n\
linked_list.insert_after(1, "Вставленный элемент")\n\
\n\
print("Список после вставки:")\n\
linked_list.display()\n\
\n\
\n\
\n\
\n\
\n\
Дан однонаправленный связный список. Удалить каждый второй элемент списка.\n\
class Node:\n\
    def __init__(self, data):\n\
        self.data = data\n\
        self.next = None\n\
def delete_every_second_node(head):\n\
    if not head:\n\
        return head\n\
    current = head\n\
    while current and current.next:\n\
        next_node = current.next\n\
        current.next = next_node.next\n\
        next_node = None\n\
        current = current.next\n\
    return head\n\
head = Node(1)\n\
node2 = Node(2)\n\
node3 = Node(3)\n\
node4 = Node(4)\n\
node5 = Node(5)\n\
\n\
head.next = node2\n\
node2.next = node3\n\
node3.next = node4\n\
node4.next = node5\n\
\n\
print("Исходный список:")\n\
current = head\n\
while current:\n\
    print(current.data, end=" -> ")\n\
    current = current.next\n\
print("None")\n\
\n\
\n\
head = delete_every_second_node(head)\n\
\n\
print("Список после удаления каждого второго узла:")\n\
current = head\n\
while current:\n\
    print(current.data, end=" -> ")\n\
    current = current.next\n\
print("None")\n\
'
            ,
#31
            'Создать декоратор tol':'Создать декоратор tol(len, fill) с параметрами len и fill. Декоратор превращает результат декорируемой функции в список состоящий из len элементов. Если исходная функция возвращает меньше заданного количества элементов, то оставшиеся места заполняются значениями fill, в случае, если количество возвращаемых элементов больше len, то хвост последовательности отбрасывается.\n\
\n\
def tol(length, fill):\n\
    def decorator(func):\n\
        def wrapper(*args, **kwargs):\n\
            result = func(*args, **kwargs)\n\
            # Обрезаем результат, если он длиннее length\n\
            result = result[:length]\n\
            # Заполняем результат, если он короче length\n\
            result += [fill] * (length - len(result))\n\
            return result\n\
        return wrapper\n\
    return decorator\n\
#ПРИМЕР ИСПОЛЬЗОВАНИЯ\n\
@tol(5, 0)  # Декоратор с параметрами len=5 и fill=0\n\
def generate_sequence():\n\
    return [1, 2, 3]\n\
result = generate_sequence()\n\
print(result)'
            ,
#32
                        'Реализовать однонаправленный связанный':'Реализовать однонаправленный связанный список (реализовать класс для элементов списка). Преобразовать строку «Eeny, meeny, miney, moe; Catch a tiger by his toe.» в связный список символов строки и удалить из него все элементы содержащие гласные буквы.\n\
\n\
class Node:\n\
    def __init__(self, data):\n\
        self.data = data\n\
        self.next = None\n\
class LinkedList:\n\
    def __init__(self):\n\
        self.head = None\n\
    def insert(self, data):\n\
        new_node = Node(data)\n\
        if self.head is None:\n\
            self.head = new_node\n\
        else:\n\
            current = self.head\n\
            while current.next:\n\
                current = current.next\n\
            current.next = new_node\n\
    def remove_vowels(self):\n\
        if self.head is None:\n\
            return\n\
        current = self.head\n\
        previous = None\n\
        vowels = set("aeiouyAEIOUY")\n\
        while current:\n\
            if current.data in vowels:\n\
                if previous:\n\
                    previous.next = current.next\n\
                else:\n\
                    self.head = current.next\n\
                current = current.next\n\
            else:\n\
                previous = current\n\
                current = current.next\n\
    def display(self):\n\
        current = self.head\n\
        while current:\n\
            print(current.data, end=" ")\n\
            current = current.next\n\
        print()\n\
# Создание связанного списка из строки\n\
string = «Eeny, meeny, miney, moe; Catch a tiger by his toe.»\n\
linked_list = LinkedList()\n\
for char in string:\n\
    linked_list.insert(char)\n\
# Удаление элементов с гласными буквами\n\
linked_list.remove_vowels()\n\
# Вывод связанного списка\n\
linked_list.display()'
            ,
#33
            'Создать базовый класс':'Создать базовый класс по следующей предметной области. Известны оклад (зарплата) и ставка процента подоходного налога. Определить размер подоходного налога и сумму, получаемую на руки. Исходными данными являются величина оклада (переменная oklad, выражаемая числом) и ставка подоходного налога (переменная procent, выражаемая числом). Размер налога (переменная nalog) определяется как oklad∗procent/100, а сумма, получаемая на руки (переменная summa) — как oklad-nalog. \n\
\n\
class Salary:\n\
    def __init__(self, oklad, procent):\n\
        self.oklad = oklad\n\
        self.procent = procent\n\
    def calculate_tax(self):\n\
        nalog = self.oklad * self.procent / 100\n\
        return nalog\n\
    def calculate_net_salary(self):\n\
        nalog = self.calculate_tax()\n\
        summa = self.oklad - nalog\n\
        return summa\n\
# Пример использования\n\
oklad = 1000000\n\
procent = 13\n\
salary = Salary(oklad, procent)\n\
nalog = salary.calculate_tax()\n\
summa = salary.calculate_net_salary()\n\
print(f"Размер налога: {nalog}")\n\
print(f"Сумма на руки: {summa}")\n\
\n\
'
            ,
#35
            'Описать рекурсивные функции':'Описать рекурсивные функции Fact(N) и Fact2(N) вещественного типа, вычисляющие значения факториала N! и двойного факториала N!! соответственно (N > 0 — параметр целого типа).\n\
def Fact(N):\n\
    if N == 0 or N == 1:\n\
        return 1\n\
    else:\n\
        return N * Fact(N - 1)\n\
def Fact2(N):\n\
    if N <= 0:\n\
        return 1\n\
    elif N == 1:\n\
        return 1\n\
    else:\n\
        return N * Fact2(N - 2)\n\
#пример\n\
N=5\n\
factorial = Fact(N)\n\
double_factorial = Fact2(N)\n\
print(f"Факториал {N}! = {factorial}")\n\
print(f"Двойной факториал {N}!! = {double_factorial}")'
            ,
#37-53
            'Создать иерархию классов':'Создать иерархию классов для фруктов, продающихся в магазине. Иерархия должна содержать не менее 3 классов. Объекты должны содержать не менее 3-х атрибутов. Часть атрибутов должна быть защищена от изменения. Необходимо заполнить список представителями всех классов (всего 5 объектов) и продемонстрировать созданную защиту.\n\
\n\
class Fruit:\n\
    def __init__(self, name, color):\n\
        self._name = name\n\
        self._color = color\n\
\n\
    def get_name(self):\n\
        return self._name\n\
\n\
    def get_color(self):\n\
        return self._color\n\
\n\
class Vegetable:\n\
    def __init__(self, name, color):\n\
        self._name = name\n\
        self._color = color\n\
\n\
    def get_name(self):\n\
        return self._name\n\
\n\
    def get_color(self):\n\
        return self._color\n\
\n\
class Berry:\n\
    def __init__(self, name, color):\n\
        self._name = name\n\
        self._color = color\n\
\n\
    def get_name(self):\n\
        return self._name\n\
\n\
    def get_color(self):\n\
        return self._color\n\
fruit = Fruit("Яблоко", "Красное")\n\
vegetable = Vegetable("Морковь", "Оранжевая")\n\
berry = Berry("Клубника", "Красная")\n\
print(fruit.get_name())  # Вывод: Яблоко\n\
print(vegetable.get_color())  # Вывод: Оранжевая\n\
print(berry.get_name())  # Вывод: Клубника\n\
\n\
\n\
\n\
\n\
\n\
Создать иерархию классов для фруктов, продающихся в магазине. Иерархия должна содержать не менее 3 классов. Объекты должны содержать не менее 2-х атрибутов и 2-х методов. Реализовать механизм автоматического подсчета количества всех созданных фруктов и автоматического присвоения каждому фрукту уникального идентификатора. Необходимо заполнить список представителями всех классов (всего не менее 5 объектов) и продемонстрировать работу созданного механизма. (20 баллов)\n\
class Mango(object):\n\
    next_index = 0\n\
    \n\
    @classmethod # для задания индекса\n\
    def generate_next_index(cls):\n\
        index = cls.next_index\n\
        cls.next_index += 1 \n\
        return index\n\
    \n\
    def __init__(self, sort, country, weight):\n\
        self.index = Mango.generate_next_index()\n\
        self.sort = sort\n\
        self.country = country\n\
        self.weight = weight\n\
        \n\
    def price(self):\n\
        return f»the price is {self.weight * 100}»\n\
    \n\
    def __str__(self):\n\
        return f»Сорт манго - {self.sort}, страна - {self.country}, вес - {self.weight}»\n\
\n\
class Banana(Mango):\n\
    next_index = 0\n\
    \n\
    @classmethod\n\
    def generate_next_index(cls):\n\
        index = cls.next_index\n\
        cls.next_index += 1\n\
        return index\n\
    \n\
    def __init__(self, sort, counrty, weight, size):\n\
        super().__init__(sort, country, weight)\n\
        self.index = Banana.generate_next_index()\n\
        self.size = size\n\
        \n\
    def price(self):\n\
        super().price()\n\
        \n\
class Apple(Mango):\n\
    next_index = 0\n\
    \n\
    @classmethod\n\
    def generate_next_index(cls):\n\
        index = cls.next_index\n\
        cls.next_index += 1\n\
        return index\n\
    \n\
    def __init__(self, sort, country, weight, count):\n\
        super().__init__(sort, country, weight)\n\
        self.index = Apple.generate_next_index()\n\
        self.count = count\n\
        \n\
    def price(self):\n\
        return super().price()\n\
        \n\
a1 = Apple(«red», «USA», 2, 3)\n\
a1.next_index\n\
a2 = Apple(«blue», «Kazakhstan», 1, 4)\n\
a2.next_index\n\
m = Mango(«dope», «Brazil», 0.2)\n\
m1 = Mango(«aloa», «Brazil», 0.5)\n\
m2 = Mango(«waergsedrgearg», «Rushka», 123)\n\
m2.next_index'
            ,
#38
            'Расположить по алфавиту':'Расположить по алфавиту имена владельцев и, соответственно, вывести информацию об их машинах.  Использовать алгоритм сортировки выбором.\n\
\n\
def selection_sort(owners, cars):\n\
    n = len(owners)\n\
    for i in range(n-1):\n\
        min_index = i\n\
        for j in range(i+1, n):\n\
            if owners[j] < owners[min_index]:\n\
                min_index = j\n\
        if min_index != i:\n\
            owners[i], owners[min_index] = owners[min_index], owners[i]\n\
            cars[i], cars[min_index] = cars[min_index], cars[i]\n\
\n\
# Пример данных владельцев и их машин\n\
owners = ["Alice", "Charlie", "Bob", "Eve"]\n\
cars = ["Toyota", "Ford", "Honda", "BMW"]\n\
\n\
# Вызываем сортировку выбором\n\
selection_sort(owners, cars)\n\
\n\
# Выводим информацию об отсортированных владельцах и их машинах\n\
for i in range(len(owners)):\n\
    print(f"Владелец: {owners[i]}, Машина: {cars[i]}")'
            ,
#39
            'Описать рекурсивную функцию':'Описать рекурсивную функцию Root (а, b, ε), которая методом деления отрезка пополам находит с точностью ε корень уравнения f(x) = 0 на отрезке [а, b] (считать, что ε > 0, а < b, f(a) – f(b) < 0 и f(x) — непрерывная и монотонная на отрезке [а, b] функция).\n\
\n\
def Root(a, b, ε):\n\
    c = (a + b) / 2  # Находим середину отрезка\n\
    if abs(f(c)) < ε:\n\
        return c  # Условие остановки: достигнута необходимая точность ε\n\
    elif f(a) * f(c) < 0:\n\
        return Root(a, c, ε)  # Рекурсивный вызов для левого подотрезка\n\
    else:\n\
        return Root(c, b, ε)  # Рекурсивный вызов для правого подотрезка\n\
def f(x):\n\
    return x**2 - 4  # Пример функции f(x) = x^2 - 4\n\
\n\
a = 0  # Левый конец отрезка\n\
b = 3  # Правый конец отрезка\n\
ε = 0.001  # Требуемая точность\n\
\n\
root = Root(a, b, ε)\n\
print("Найденный корень:", root)'
            ,
#40-42-44
            'Дан одномерный массив':'Дан одномерный массив целых чисел размерности n, заданных случайным образом из интервала от -20 до 20. Если сумма отрицательных элементов по модулю превышает сумму положительных, то отсортировать массив по возрастанию, иначе – по убыванию. Реализовать сортировку алгоритмом сортировки выбором.\n\
\n\
def selection_sort(arr):\n\
    n = len(arr)\n\
    for i in range(n - 1):\n\
        min_index = i\n\
        for j in range(i + 1, n):\n\
            if arr[j] < arr[min_index]:\n\
                min_index = j\n\
        arr[i], arr[min_index] = arr[min_index], arr[i]\n\
\n\
def sort_array(arr):\n\
    positive_sum = 0\n\
    negative_sum = 0\n\
\n\
    for num in arr:\n\
        if num < 0:\n\
            negative_sum += abs(num)\n\
        else:\n\
            positive_sum += num\n\
\n\
    if negative_sum > positive_sum:\n\
        selection_sort(arr)\n\
    else:\n\
        selection_sort(arr)\n\
        arr.reverse()\n\
\n\
# Пример данных\n\
import random\n\
\n\
n = 10\n\
array = [random.randint(-20, 20) for _ in range(n)]\n\
print("Исходный массив:", array)\n\
\n\
sort_array(array)\n\
print("Отсортированный массив:", array)\n\
\n\
\n\
\n\
\n\
\n\
Дан одномерный массив целых чисел размерности n, заданных случайным образом из интервала от -20 до 20. Если в массиве есть отрицательные элементы, то отсортировать массив по возрастанию, иначе - по убыванию. Реализовать сортировку алгоритмом сортировки вставками.\n\
\n\
def insertion_sort(arr):\n\
    n = len(arr)\n\
    for i in range(1, n):\n\
        key = arr[i]\n\
        j = i - 1\n\
        while j >= 0 and arr[j] > key:\n\
            arr[j + 1] = arr[j]\n\
            j -= 1\n\
        arr[j + 1] = key\n\
\n\
def sort_array(arr):\n\
    has_negative = any(num < 0 for num in arr)\n\
\n\
    if has_negative:\n\
        insertion_sort(arr)\n\
    else:\n\
        insertion_sort(arr)\n\
        arr.reverse()\n\
\n\
# Пример данных\n\
import random\n\
\n\
n = 10\n\
array = [random.randint(-20, 20) for _ in range(n)]\n\
print("Исходный массив:", array)\n\
\n\
sort_array(array)\n\
print("Отсортированный массив:", array)\n\
\n\
\n\
\n\
\n\
\n\
Дан одномерный массив целых чисел размерности n, заданных случайным образом из интервала от 0 до 100. Если количество четных элементов, стоящих на нечетных местах, превышает количество нечетных элементов, стоящих на четных местах, то отсортировать массив по возрастанию, иначе по убыванию. Реализовать алгоритм сортировки слиянием\n\
\n\
def merge_sort(arr):\n\
    if len(arr) <= 1:\n\
        return arr\n\
\n\
    mid = len(arr) // 2\n\
    odd_arr = merge_sort(arr[1::2])\n\
    even_arr = merge_sort(arr[0::2])\n\
\n\
    count_odd = sum(1 for num in even_arr if num % 2 != 0)\n\
    count_even = sum(1 for num in odd_arr if num % 2 == 0)\n\
\n\
    if count_even > count_odd:\n\
        odd_arr.sort()\n\
        even_arr.sort()\n\
    else:\n\
        odd_arr.sort(reverse=True)\n\
        even_arr.sort(reverse=True)\n\
\n\
    merged = []\n\
    i = j = 0\n\
    while i < len(odd_arr) and j < len(even_arr):\n\
        if odd_arr[i] <= even_arr[j]:\n\
            merged.append(odd_arr[i])\n\
            i += 1\n\
        else:\n\
            merged.append(even_arr[j])\n\
            j += 1\n\
\n\
    merged.extend(odd_arr[i:])\n\
    merged.extend(even_arr[j:])\n\
\n\
    return merged\n\
\n\
# Пример данных\n\
import random\n\
\n\
n = 10\n\
array = [random.randint(0, 100) for _ in range(n)]\n\
print("Исходный массив:", array)\n\
\n\
sorted_array = merge_sort(array)\n\
print("Отсортированный массив:", sorted_array)'
            ,
#41
            'Создать декоратор dec':'Создать декоратор dec(a, b) с параметрами a и b. Декоратор увеличивает результат декорируемой функции, которая вычисляет сумму произвольного количества чисел, на «a» элементов при условии положительного значения суммы. Если исходная функция возвращает отрицательное значение суммы, то декоратор уменьшает результат декорируемой функции на значение «b».\n\
\n\
def dec(a, b):\n\
    def decorator(func):\n\
        def wrapper(*args):\n\
            result = func(*args)\n\
            if result >= 0:\n\
                result += a\n\
            else:\n\
                result -= b\n\
            return result\n\
        return wrapper\n\
    return decorator\n\
\n\
# Пример использования декоратора\n\
\n\
@dec(a=10, b=5)\n\
def sum_numbers(*args):\n\
    return sum(args)\n\
\n\
# Вызываем декорированную функцию\n\
result = sum_numbers(1, 2, 3, 4, 5)\n\
print("Результат:", result)'
            ,
#43-47-49
            'Дан список целых':'Дан список целых чисел. При помощи механизма map/filter/reduce рассчитать остаток от деления на 7 для каждого из чисел списка и получить произведение тех остатков, величина которых больше 4.\n\
\n\
from functools import reduce\n\
\n\
# Исходный список целых чисел\n\
numbers = [12, 15, 21, 8, 9, 6, 11]\n\
\n\
# Рассчитываем остаток от деления на 7 для каждого числа\n\
remainders = list(map(lambda x: x % 7, numbers))\n\
\n\
# Фильтруем остатки, оставляя только те, которые больше 4\n\
filtered_remainders = list(filter(lambda x: x > 4, remainders))\n\
\n\
# Вычисляем произведение отфильтрованных остатков с помощью reduce\n\
result = reduce(lambda x, y: x * y, filtered_remainders)\n\
\n\
print("Результат:", result)\n\
\n\
\n\
\n\
\n\
\n\
Дан список целых чисел.  При помощи механизма map/filter/reduce рассчитать остаток от деления на 17 для каждого из чисел списка и получить произведение тех остатков, величина которых меньше 7. (20 баллов)\n\
ls = [19, 18, 17, 21, 20, 5, 8]\n\
a = list(filter(lambda x: x%17, ls))\n\
prod = 1\n\
for i in a:\n\
    if i%17 < 7:\n\
        prod*=i\n\
print(prod)\n\
\n\
\n\
\n\
\n\
\n\
Дан список целых чисел.  При помощи механизма map/filter/reduce рассчитать разность со значением 10 для каждого из чисел списка и получить сумму тех значений, величина которых меньше 0. (20 баллов)\n\
a = [1, 2, 10, 20, 15, 5, 8, 9]\n\
print(list(filter(lambda x: x-10<0, a)))'
            ,
#46
            'Дано два однонаправленных':'Дано два однонаправленных связных списка. Создать список, содержащий элементы общие для двух списков. (20 баллов)\n\
class Node:\n\
    def __init__(self, value = None, next = None):\n\
        self.value = value\n\
        self.next = next\n\
        \n\
class LinkedList:\n\
    def __init__(self):\n\
        self.first = None\n\
        self.last = None\n\
        self.lenght = 0\n\
\n\
    def __str__(self):\n\
        if self.first != None:\n\
            current = self.first\n\
            out = "LinkedList [" +str(current.value) +" "\n\
            while current.next != None:\n\
                current = current.next\n\
                out += str(current.value) + " "\n\
            return out + "]"\n\
        return "LinkedList []"\n\
    def add(self, x):\n\
        self.lenght+=1\n\
        if self.first == None:\n\
            self.last = self.first = Node(x, None)\n\
        else:\n\
            self.last.next = self.last = Node(x, None)\n\
            \n\
    def delete_second(self):\n\
        current = self.first\n\
        i=1\n\
        while current.next != None:\n\
            if (i+1)%2==0:\n\
                current.next = current.next.next\n\
            else:\n\
                current = current.next\n\
            i+=1\n\
L1 = LinkedList()\n\
L1.add(1)\n\
L1.add(2)\n\
L1.add(3)\n\
L2 = LinkedList()\n\
L2.add(4)\n\
L2.add(2)\n\
L2.add(3)\n\
L3 = LinkedList()\n\
current1 = L1.first\n\
for i in range(L1.lenght):\n\
    current2 = L2.first\n\
    for j in range(L2.lenght):\n\
        if current1.value == current2.value:\n\
            L3.add(current1.value)\n\
        current2 = current2.next\n\
    current1 = current1.next\n\
print(L1)\n\
print(L2)\n\
print(L3)\n\
'
            ,
#48
            'Создать класс Профиль':'Создать класс Профиль местности, который хранит последовательность высот, вычисленных через равные промежутки по горизонтали. Методы: наибольшая высота, наименьшая высота, перепад высот (наибольший, суммарный), крутизна (тангенс угла наклона; наибольшая, средняя), сравнение двух профилей одинаковой длины (по перепаду, по крутизне). (20 баллов)\n\
class Profile:\n\
    def __init__(self, heights):\n\
        self.heights = heights\n\
\n\
    def max_height(self):\n\
        return max(self.heights)\n\
\n\
    def min_height(self):\n\
        return min(self.heights)\n\
\n\
    def height_difference_max(self):\n\
        return max(self.heights) - min(self.heights)\n\
\n\
    def height_difference_sum(self):\n\
        return sum(self.heights) - len(self.heights) * self.min_height()\n\
\n\
    def slope_max(self):\n\
        max_slope = max(abs(y2 - y1) / (x2 - x1) for x1, y1, x2, y2 in zip(range(len(self.heights) - 1), self.heights[:-1], range(1, len(self.heights)), self.heights[1:]))\n\
        return max_slope\n\
\n\
    def slope_avg(self):\n\
        avg_slope = sum(abs(y2 - y1) / (x2 - x1) for x1, y1, x2, y2 in zip(range(len(self.heights) - 1), self.heights[:-1], range(1, len(self.heights)), self.heights[1:])) / (len(self.heights) - 1)\n\
        return avg_slope\n\
\n\
    def compare_height_difference(self, other_profile):\n\
        if len(self.heights) != len(other_profile.heights):\n\
            raise ValueError("Profiles must have the same length")\n\
        self_diff = self.height_difference_max()\n\
        other_diff = other_profile.height_difference_max()\n\
        if self_diff > other_diff:\n\
            return 1\n\
        elif self_diff < other_diff:\n\
            return -1\n\
        else:\n\
            return 0\n\
\n\
    def compare_slope(self, other_profile):\n\
        if len(self.heights) != len(other_profile.heights):\n\
            raise ValueError("Profiles must have the same length")\n\
        self_slope = self.slope_max()\n\
        other_slope = other_profile.slope_max()\n\
        if self_slope > other_slope:\n\
            return 1\n\
        elif self_slope < other_slope:\n\
            return -1\n\
        else:\n\
            return 0\n\
profile1 = Profile([10, 15, 20, 18, 12, 8, 6])\n\
\n\
# Вызов методов для получения информации о профиле\n\
print("Максимальная высота:", profile1.max_height())  \n\
print("Минимальная высота:", profile1.min_height())  \n\
print("Максимальный перепад высот:", profile1.height_difference_max())  \n\
print("Суммарный перепад высот:", profile1.height_difference_sum())  \n\
print("Максимальная крутизна:", profile1.slope_max())  \n\
print("Средняя крутизна:", profile1.slope_avg())  \n\
\n\
\n\
profile2 = Profile([8, 12, 10, 16, 14, 20, 22])\n\
\n\
print("Сравнение по высоте", profile1.compare_height_difference(profile2))  \n\
\n\
print("Сравнение по крутизне", profile1.compare_slope(profile2))'
            ,
#50
            'Реализовать двоичное дерево':'Реализовать двоичное дерево в виде связанных объектов (реализовать класс для элементов двоичного дерева) и реализовать симметричную процедуру обхода двоичного дерева в виде рекурсивной функции. (20 баллов)\n\
class BinaryNode: # двоичное дерево (класс)\n\
    def __init__(self, val, left=None, right=None, parent=None): # инициализация\n\
        self.val = val\n\
        self.left_child = left\n\
        self.right_child = right\n\
        self.parent = parent\n\
\n\
    def get_left_child(self): \n\
        return self.left_child #методы для возвращения левых и правых эл-в\n\
\n\
    def get_right_child(self):\n\
        return self.right_child\n\
    \n\
    def get_val(self):\n\
        return self.val\n\
    \n\
    def set_val(self, val):\n\
        self.val = val\n\
        \n\
    def get_parent(self):\n\
        return self.parent\n\
    \n\
    def set_left_child(self, node): # \n\
        if self.left_child == None: \n\
            self.left_child = BinaryNode(node, None, None, self)\n\
        else:\n\
            t = BinaryNode(node)\n\
            t.left_child = self.left_child\n\
            self.left_child = t\n\
            \n\
    def set_right_child(self, node):\n\
        if self.right_child == None:\n\
            self.right_child = BinaryNode(node, None, None, self)\n\
        else:\n\
            t = BinaryNode(node)\n\
            t.right_child = self.right_child\n\
            self.right_child = t\n\
            \n\
    def set_parent(self, node):\n\
        self.parent = BinaryNode(node)\n\
        \n\
    def __str__(self):\n\
        return "{} ({}, {})".format(str(self.get_val()), str(self.get_left_child()), str(self.get_right_child()))\n\
    \n\
def in_order(node):\n\
    if node:\n\
        in_order(node.left_child)\n\
        print(node.get_val(), end = " ")\n\
        in_order(node.right_child)\n\
        \n\
r = BinaryNode(5)\n\
r.set_left_child(7)\n\
r.set_right_child(6)\n\
r.get_left_child().set_left_child(10)\n\
r.get_left_child().set_right_child(30)\n\
r.set_right_child(20)\n\
r.__str__()\n\
in_order(r)'
            ,
#51-55
            'В одномерном массиве':'В одномерном массиве целых чисел найти количество пар элементов разного знака. (пара — это два рядом стоящих элемента). (20 баллов)\n\
counter = 0 # счетчик для пар \n\
array = [1, -1, 2, 4 ,5, -6, 2, 3]\n\
for i in range(len(array)-1):\n\
    if array[i] < 0 and array[i+1] > 0: # проверка знаков\n\
        counter+=1\n\
    elif array[i] > 0 and array[i+1] < 0:\n\
        counter+=1\n\
        \n\
print(counter)\n\
\n\
\n\
\n\
\n\
\n\
В одномерном массиве (array) целых чисел найти количество пар модуль разности элементов которых, больше 10. (пара — это два рядом стоящих элемента). (20 баллов)\n\
def count_pairs(array):\n\
    count = 0\n\
\n\
    for i in range(len(array) - 1):\n\
        diff = abs(array[i] - array[i + 1])\n\
\n\
        if diff > 10:\n\
            count += 1\n\
\n\
    return count\n\
\n\
\n\
# Пример \n\
arr = [3, 15, 7, 22, 18, 9, 4]\n\
pair_count = count_pairs(arr)\n\
print(pair_count)'
            ,
#56
            'Реализовать функцию st_reverse':'Реализовать функцию st_reverse(a_string), которая при помощи стека инвертирует строку (меняет порядок букв на обратный).  Пример: st_reverse(«abcd») -> «dcba». (20 баллов)\n\
class Stack:\n\
    def __init__(self):\n\
        self.items = []\n\
\n\
    def push(self, item):\n\
        self.items.append(item)\n\
\n\
    def pop(self):\n\
        if not self.is_empty():\n\
            return self.items.pop()\n\
        return None\n\
\n\
    def is_empty(self):\n\
        return len(self.items) == 0\n\
\n\
\n\
def st_reverse(a_string):\n\
    stack = Stack()\n\
\n\
    for char in a_string:\n\
        stack.push(char)\n\
\n\
    reversed_string = ""\n\
\n\
    while not stack.is_empty():\n\
        reversed_string += stack.pop()\n\
\n\
    return reversed_string\n\
\n\
\n\
# Пример \n\
string = "abcd"\n\
reversed_string = st_reverse(string)\n\
print(reversed_string)'
            ,
#57-58
            'Дан двунаправленный связный':'Дан двунаправленный связный список. Вставить элемент после n-го элемента списка. (20 баллов)\n\
class Node:\n\
    def __init__(self, data):\n\
        self.data = data\n\
        self.next = None\n\
        self.prev = None\n\
\n\
class DoublyLinkedList:\n\
    def __init__(self):\n\
        self.head = None\n\
\n\
    def insert_after_nth_node(self, n, data):\n\
        new_node = Node(data)\n\
        if self.head is None:\n\
            self.head = new_node\n\
        else:\n\
            current = self.head\n\
            count = 1\n\
            while current and count < n:\n\
                current = current.next\n\
                count += 1\n\
\n\
            if current is None:\n\
                last_node = self.get_last_node()\n\
                last_node.next = new_node\n\
                new_node.prev = last_node\n\
            else:\n\
                new_node.next = current.next\n\
                new_node.prev = current\n\
                if current.next:\n\
                    current.next.prev = new_node\n\
                current.next = new_node\n\
\n\
    def get_last_node(self):\n\
        current = self.head\n\
        while current.next:\n\
            current = current.next\n\
        return current\n\
\n\
    def display(self):\n\
        current = self.head\n\
        while current:\n\
            print(current.data, end=" ")\n\
            current = current.next\n\
        print()\n\
\n\
# Пример \n\
dll = DoublyLinkedList()\n\
\n\
dll.insert_after_nth_node(2, 10)  \n\
dll.insert_after_nth_node(4, 20)  \n\
dll.insert_after_nth_node(1, 5)   \n\
\n\
dll.display()\n\
\n\
\n\
\n\
\n\
\n\
Дан двунаправленный связный список. Удалить n-ый элемент списка. (20 баллов)\n\
class Node:\n\
    def __init__(self, data):\n\
        self.data = data\n\
        self.prev = None\n\
        self.next = None\n\
\n\
def delete_node(head, n):\n\
    if not head or n == 0:\n\
        return head\n\
\n\
    if n == 1:\n\
        new_head = head.next\n\
        if new_head:\n\
            new_head.prev = None\n\
        return new_head\n\
\n\
    current = head\n\
    prev_node = None\n\
    count = 1\n\
\n\
    while current and count < n:\n\
        prev_node = current\n\
        current = current.next\n\
        count += 1\n\
\n\
    if not current:\n\
        return head\n\
\n\
    prev_node.next = current.next\n\
\n\
    if current.next:\n\
        current.next.prev = prev_node\n\
\n\
    return head\n\
\n\
#Пример\n\
\n\
head = Node(1)\n\
node2 = Node(2)\n\
node3 = Node(3)\n\
node4 = Node(4)\n\
node5 = Node(5)\n\
\n\
head.next = node2\n\
node2.prev = head\n\
node2.next = node3\n\
node3.prev = node2\n\
node3.next = node4\n\
node4.prev = node3\n\
node4.next = node5\n\
node5.prev = node4\n\
\n\
\n\
current = head\n\
while current:\n\
    print(current.data, end=" ")\n\
    current = current.next\n\
\n\
\n\
print()\n\
\n\
\n\
head = delete_node(head, 3)\n\
\n\
\n\
current = head\n\
while current:\n\
    print(current.data, end=" ")\n\
    current = current.next'}

        print(sklad[number])

    def theory(number=''):
        #1
        sklad = {'Концепция класса и': 'Класс — в объектно-ориентированном программировании, представляет собой шаблон для создания объектов, обеспечивающий начальные значения состояний: инициализация полей-переменных и реализация поведения функций или методов.\n\
Объект — некоторая сущность в цифровом пространстве, обладающая определённым состоянием и поведением, имеющая определенные свойства (атрибуты) и операции над ними (методы). Как правило, при рассмотрении объектов выделяется то, что объекты принадлежат одному или нескольким классам, которые определяют поведение (являются моделью) объекта. Термины «экземпляр класса» и «объект» взаимозаменяемы.\n\
Парадигма ООП построена на 3 основных принципах:\n\
Инкапсуляция – сокрытие данных, т. е. классы не имеют прямого доступа к полям друг друга, а взаимодействие между ними осуществляется через публичные методы.\n\
Наследование – название говорит само за себя. Дочерний класс наследует свойства и методы родительского, тем самым реализуя повторное использование. \n\
Полиморфизм – это способность одного и того же объекта вести себя по-разному в зависимости от того, в контексте какого класса он используется. Полиморфизм связан с созданием перегружаемых виртуальных методов.\n\
'
                 ,
#2
                 'Объявление класса конструктор': 'Теория\n\
\n\
2.Объявление класса, конструктор, создание объектов и одиночное наследование в Python. Управление доступом к атрибутам класса в Python. Полиморфизм и утиная типизация и проверка принадлежности объекта к классу в языке Python.\n\
\n\
Объявление класса\n\
Создание класса в Python начинается с инструкции class. Вот так будет выглядеть минимальный класс.\n\
class C: \n\
    pass\n\
\n\
Класс состоит из объявления (инструкция class), имени класса (нашем случае это имя C) и тела класса, которое содержит атрибуты и методы (в нашем минимальном классе есть только одна инструкция pass).\n\
\n\
Конструктор:\n\
•	Конструктор — уникальный  метод класса, который называется __init__.\n\
•	Первый параметр конструктора во всех случаях self (ключевое слово, которое ссылается на сам класс).\n\
•	Конструктор нужен для создания объекта.\n\
•	Конструктор передает значения аргументов свойствам создаваемого объекта.\n\
•	В одном классе всегда только один конструктор.\n\
•	Если класс определяется не конструктором, Python предположит, что он наследует конструктор родительского класса.\n\
\n\
\n\
\n\
\n\
\n\
Создание объектов\n\
Создание объектов в Python довольно простое. Сначала вы указываете имя нового объекта, за которым следует оператор присваивания и имя класса с параметрами (как определено в конструкторе). \n\
Помните, что количество и тип параметров должны быть совместимы с параметрами, полученными в функции-конструкторе. \n\
Когда объект создан, могут быть вызваны методы-члены и доступны атрибуты-члены (при условии, что они доступны).\n\
\n\
Одиночное наследование \n\
Одноуровневое наследование позволяет производному классу наследовать характеристики от одного родительского класса.\n\
\n\
Управления доступом к атрибутам  класса в Python\n\
Управления доступом к атрибутам в Python может осуществляться несколькими способами:\n\
__getattr__  __set__  __getattribute__  __delete__\n\
property\n\
дескриптор\n\
property и дескрипторы применяются к отдельным атрибутам.\n\
Свойства\n\
attribute = property(fget, fset, fdel, doc)\n\
Все аргументы по умолчанию None, при обращение приводят к исключению\n\
Дескрипторы\n\
Протокол дескрипторов позволяет передавать выполнение операций чтения и записи для определенного атрибута методам отдельного обьекта класса.\n\
В отличии от свойств в дескрипторе при отсутствии метода не возникает исключение.\n\
Если не реализован __set__, то атрибут будет просто переопределен\n\
\n\
\n\
__getattr__ и __getattribute__\n\
__getattr__ -вызывается при обращение к несуществующим атрибутам\n\
__set__ -при присваивании значений\n\
__getattribute__ -вызывается при обращение к любым атрибутам\n\
Делегирования - управление доступом ко всем атрибутам встроенного объекта\n\
функция getattr(self, item) эквивалентна self.item\n\
\n\
Полиморфизм и утиная типизация\n\
Полиморфизм - это поддержка нескольких реализаций на основе общего интерфейса.\n\
Другими словами, полиморфизм позволяет перегружать одноименные методы родительского класса в классах-потомках.\n\
утиная типизация\n\
Утиная типизация – это концепция, характерная для языков программирования с динамической типизацией, согласно которой конкретный тип или класс объекта не важен, а важны лишь свойства и методы, которыми этот объект обладает. Другими словами, при работе с объектом его тип не проверяется, вместо этого проверяются свойства и методы этого объекта. Такой подход добавляет гибкости коду, позволяет полиморфно работать с объектами, которые никак не связаны друг с другом и могут быть объектами разных классов. Единственное условие, чтобы все эти объекты поддерживали необходимый набор свойств и методов.\n\
проверка принадлежности объекта к классу в языке Python.\n\
Описание:\n\
Функция isinstance() вернет True, если проверяемый объект object является экземпляром указанного класса (классов) или его подкласса (прямого, косвенного или виртуального).\n\
Если объект object не является экземпляром данного типа, то функция всегда возвращает False.\n\
Функцией isinstance() можно проверить класс, кортеж с классами, либо рекурсивный кортеж кортежей. Другие типы последовательностей аргументом classinfo не поддерживаются.\n\
Синтаксис:\n\
isinstance(object, classinfo)\n\
Параметры:\n\
•	object - объект, требующий проверки,\n\
•	classinfo - класс, кортеж с классами или рекурсивный кортеж кортежей или с версии Python 3.10 может быть объединением нескольких типов (например int | str).\n\
Возвращаемое значение:\n\
•	bool.\n\
'
,



                 
#3
                 'Методы классов и': 'Методы классов и статические переменные и методы в Python. Специальные методы для использования пользовательских классов со стандартными операторами и функциями.\n\
\n\
Методы классов\n\
Методы класса вместо параметра self принимают параметр cls. Этот параметр при вызове метода указывает не на экземпляр объекта, а на класс.\n\
Поскольку метод класса имеет доступ только к аргументу cls, он не может изменять состояние экземпляра объекта. Для этого нужен доступ к self. Но, тем не менее, методы класса могут изменять состояние класса в целом, что затронет и все экземпляры этого класса.\n\
\n\
V2:\n\
\n\
Метод класса получает первым аргументом ссылку на класс, которую принято называть cls. Такие методы относятся к классам, а значит, могут оперировать статическими атрибутами, но не имеют доступа к объектам.  Они объявляются в теле класса при помощи декораторов @staticmethod и @classmethod соответственно\n\
\n\
Статические переменные и методы в Python\n\
Статическая переменная в Python - это переменная, которая объявлена внутри определенного класса, но не в методе. Эту переменную можно вызвать через класс, внутри которого она определена, но не напрямую. Статическая переменная также называется переменной класса. Эти переменные ограничены классом, поэтому они не могут изменить состояние объекта.\n\
Статические методы в python\n\
В Python, статические методы класса отмечаются декоратором @staticmethod, \n\
Этот тип метода не принимает ни параметра self как метод экземпляра класса, ни параметра cls как метод класса. При этом, конечно, статический метод может принимать произвольное количество других параметров.\n\
Поэтому статический метод не может изменять ни состояние объекта, ни состояние класса. Статические методы ограничены в том, к каким данным они могут получить доступ.\n\
\n\
Специальные методы для использования пользовательских классов со стандартными операторами и функциями.\n\
Специальные методы\n\
Методы, имена которых обрамляются __, Python трактует как специальные, например, __init__ (инициализация) или __str__ (строковое представление). Специальные методы, как правило, идут первыми при объявлении класса.\n\
'
,
#4
                 'Основные возможности поддерживаемые': '4.Основные возможности, поддерживаемые функциональными языками программирования. Поддержка элементов функционального программирования в Python\n\
\n\
Основные возможности, поддерживаемые функциональными языками программирования\n\
\n\
•	Чистые функции — функциональное программирование использует чистые функции. Это функции, которые не изменяются, дают надёжные результаты и всегда дают одинаковый результат для одного и того же ввода. Они не вызывают неожиданных результатов или побочных эффектов и абсолютно предсказуемы независимо от внешнего кода.\n\
•	Неизменяемость — это принцип, согласно которому после того, как вы установили значение для чего-либо, это значение не изменится. Это устраняет побочные эффекты или неожиданные результаты, поскольку программа не зависит от состояния. Таким образом, функции всегда работают одинаково при каждом запуске; это чистые функции.\n\
•	Дисциплинированное состояние — новые ценности могут быть созданы, поэтому есть некоторые состояния, которые могут измениться в этом смысле, но это глубоко контролируемый процесс. Функциональное программирование стремится избежать общего состояния и изменчивости. Если состояние жёстко контролируется, его легче масштабировать и отлаживать, и вы получаете менее неожиданные результаты.\n\
•	Ссылочная прозрачность — этот принцип основан на сочетании чистых функций и неизменности. Поскольку наши функции чисты и предсказуемы, мы можем использовать их для замены переменных и, следовательно, уменьшить количество выполняемых назначений. Если результат функции будет равен переменной, поскольку наши результаты предсказуемы, мы можем просто заменить переменную этой функцией.\n\
•	Функции первого класса — этот принцип прост. Функциональное программирование очень высоко ценит определённые функции, функции первого класса. Следовательно, он поддерживает передачу целых функций между собой так же легко, как другие языки с переменными. Эти функции можно рассматривать как значения или данные в функциональном программировании.\n\
•	Системы типов — поскольку функциональное программирование так сосредоточено на точности и предотвращении ошибок. Наличие статически типизированной системы имеет смысл. Это необходимо для того, чтобы убедиться, что каждый тип данных назначен правильно, строки — это строки, а числа с плавающей запятой — это числа с плавающей запятой, и предотвращает использование непредсказуемых переменных.\n\
\n\
Поддержка элементов функционального программирования в Python\n\
Lamda функция\n\
Встроенные функции высших порядков(функции первого класса):\n\
map()\n\
Принимает функцию-аргумент и применяет её ко всем элементам входящей последовательности.\n\
filter()\n\
Как следует из названия, filter() фильтрует последовательность по заданному условию.\n\
apply()\n\
Применяет входящую функцию к позиционным и именованным аргументам. Эти аргументы задаются списком и словарём соответственно.\n\
zip()\n\
Упаковывает итерируемые объекты в один список кортежей. При работе ориентируется на объект меньшей длины:\n\
\n\
Модуль functools\n\
Functools — это библиотека, которая содержит дополнительные функции высших порядков.\n\
reduce()\n\
Принимает функцию и последовательность. Запускает цепь вычислений, применяя функцию ко всем элементам последовательности. Сводит набор к единственному значению.\n\
\n\
\n\
partial()\n\
Функция служит для частичного назначения аргументов. На входе и на выходе — тоже функции.\n\
cmp_to_key()\n\
Возвращает ключевую функцию для компарации объектов.\n\
update_wrapper()\n\
Используется для обновления метаданных функции-обертки, данными из некоторых атрибутов оборачиваемой функции. Обеспечивает лучшую читаемость и возможность повторного использования кода.\n\
@lru_cache\n\
lru_cache — это декоратор. То есть обёртка, которая может изменить поведение функции, не меняя её код. Lru_cache даёт выбранной функции кэширование, чтобы фиксировать результаты тяжеловесных вычислений, запросов или других операций.\n\
'
                 ,
#5
                 'Концепция функции граждане': '5.Концепция «функции – граждане первого класса» в языке программирования, поддержка этой концепции в Python. Специфика лямбда-функций в Python их возможности и ограничения. Типичные сценарии использования лямбда-функций в Python.\n\
\n\
Концепция «функции – граждане первого класса» в языке программирования, поддержка этой концепции в Python\n\
   Концепция «функции – граждане первого класса» в языке программирования\n\
Функции в языке программирования считаются гражданами первого класса, если они демонстрируют следующие характеристики.\n\
•	Их можно хранить в переменных.\n\
•	Их можно хранить в структурах данных.\n\
•	Их можно пропустить как аргумент к функции.\n\
•	Они могут быть возвращены как значения из другой функции.\n\
\n\
поддержка этой концепции в Python\n\
Это означает, что функции можно динамически создвать и уничтожать, передвать их в другие функции, возвращать их как значения и так далее.\n\
Python поддерживает все эти функции, чтобы функции рассматривались как граждане первого класса.\n\
def logger(msg):\n\
    def message():\n\
        print(Log:, msg)\n\
    return message\n\
logWarning = logger(Warning)\n\
logWarning()\n\
Специфика лямбда-функций в Python их возможности и ограничения.\n\
Лямбда-функция — это небольшая анонимная функция, которая принимает любое количество аргументов, но имеет только одно выражение. Лямбда-функции возвращают объект, который назначен переменной или используется как часть других функций.\n\
Лямбда-выражения отличаются от обычных определений функций по нескольким причинам. В частности, лямбда-функции ограничены одним выражением, поэтому они не могут использовать операторы или аннотации.\n\
Когда дело доходит до значений, возвращаемых из лямбда-выражений, всегда есть неявный оператор возврата. Лямбда-функции оценивают выражение и автоматически возвращают результат.\n\
\n\
Типичные сценарии использования лямбда-функций в Python.\n\
\n\
Когда функция имеет только одно выражение. \n\
\n\
Для повторяющихся задач, носящих временный характер.'               
                 ,

#6
                 'Глобальные и локальные': '6.Глобальные и локальные переменные в функциях на примере Python. Побочные эффекты вызова функций и их последствия.\n\
\n\
Глобальные переменные\n\
В Python переменная, объявленная вне функции или в глобальной области видимости, называется глобальной переменной. К глобальной переменной можно получить доступ как внутри, так и вне функции.\n\
x = глобальная переменная\n\
def foo():\n\
    print(x внутри функции:, x)\n\
foo()\n\
print(x вне функции:, x)\n\
Вывод: \n\
x внутри функции: глобальная переменная\n\
x вне функции: глобальная переменная\n\
\n\
Локальные переменные\n\
Переменная, объявленная внутри тела функции или в локальной области видимости, называется локальной переменной.\n\
\n\
def foo():\n\
    y = локальная переменная\n\
    print(y)\n\
foo()\n\
Вывод:\n\
локальная переменная\n\
\n\
Побочные эффекты вызова функций и их последствия\n\
побочные эффекты — это наблюдаемые последствия вызова функции, не относящиеся к возвращаемому результату.\n\
Есть такие функции, которые при вызове меняют файлы и таблицы баз данных, отправляют данные на сервер или модифицируют глобальные переменные. Всё это — побочные эффекты.'
                 ,

#7
                 'Вложенные функции и':'Вложенные функции и замыкания, специфика реализации в Python.\n\
Вложенные (или внутренние, англ. inner, nested) функции – это функции, которые мы определяем внутри других функций. В Python такая функция имеет прямой доступ к переменным и именам, определенным во включающей её функции. Вложенные функции имеют множество применений, в первую очередь для создания замыканий и декораторов.\n\
Замыкание — это комбинация функции и множества ссылок на переменные в области видимости функции. Последнее иногда называют ссылочной средой. Замыкание позволяет выполнять функцию за пределами области видимости. В Python ссылочная среда хранится в виде набора ячеек. Доступ к ним можно получить с помощью атрибутов func_closure или __closure__. В Python 3 используется только __closure__\n\
\n\
в Python вложенные функции имеют прямой доступ к переменным и именам, которые вы определяете во включающей функции. Это предоставляет механизм для инкапсуляции функций, создания вспомогательных решений, реализации замыканий и декораторов.\n\
\n\
'
                 ,
#8                
                 'Функции высшего порядка':'8.Функции высшего порядка и декораторы в Python.\n\
\n\
Функция высшего порядка – это функция, которая может принимать в качестве аргумента другую функцию и/или возвращать функцию как результат работы. Так как в Python функции – это объекты первого класса, то они являются HOF, это свойство активно используется при разработке программного обеспечения. \n\
\n\
К встроенным функциям высшего порядка, которые можно использовать без импорта каких-либо библиотек, относятся map и filter.\n\
Функция map принимает функцию и итератор, возвращает итератор, элементами которого являются результаты применения функции к элементам входного итератора.\n\
Функция filter принимает функцию предикат и итератор, возвращает итератор, элементами которого являются данные из исходного итератора, для которых предикат возвращает True.\n\
\n\
Модуль functools\n\
Модуль functools предоставляет набор декораторов и HOF функций, которые либо принимают другие функции в качестве аргумента, либо возвращают функции как результат работы.\n\
\n\
HOF функции\n\
\n\
Partial\n\
\n\
Функция partial создает частично примененные функции (см. “Функция как возвращаемое значение. Каррирование, замыкание, частичное применение”). Суть идеи в том, что если у функции есть несколько аргументов, то можно создать на базе нее другую, у которой часть аргументов будут иметь заранее заданные значения.\n\
\n\
Прототип:\n\
\n\
partial(func, /, *args, **keywords)\n\
\n\
Параметры:\n\
func\n\
Функция, для которой нужно построить частично примененный вариант.\n\
args\n\
Позиционные аргументы функции.\n\
keywords\n\
Именованные аргументы функции.\n\
\n\
Partialmethod\n\
\n\
Инструмент, аналогичный по своему назначению функции partial(), применяется для методов классов.\n\
\n\
Прототип:\n\
\n\
class partialmethod(func, /, *args, **keywords)\n\
\n\
Параметры:\n\
\n\
func\n\
Метод класса, для которого нужно построить частично примененный вариант.\n\
args\n\
Позиционные аргументы метода.\n\
keywords\n\
Именованные аргументы метода.\n\
\n\
Reduce\n\
\n\
Сворачивает переданную последовательность с помощью заданной функции. Прототип функции:\n\
\n\
reduce(function, iterable[, initializer])\n\
\n\
Параметры:\n\
function\n\
Функция для свертки исходной последовательности, должна принимать два аргумента.\n\
iterable\n\
Последовательность для свертки (итератор).\n\
initializer\n\
Начальное значение, которое будет использоваться для сверки. Если значение не задано, то в качестве начального будет выбран первый элемент из итератора.\n\
\n\
Декоратор — это функция, которая позволяет обернуть другую функцию для расширения её функциональности без непосредственного изменения её кода. \n\
\n\
def param_transfer(fn):\n\
   def wrapper(arg):\n\
       print("Run function: " + str(fn.__name__) + "(), with param: " + str(arg))\n\
       fn(arg)\n\
   return wrapper\n\
@param_transfer\n\
def print_sqrt(num):\n\
   print(num**0.5)'
                 ,
#9                 
                 'Концепция map filter':'9.Концепция map/filter/reduce. Реализация map/filter/reduce в Python и пример их использования.\n\
\n\
В Python функция map принимает два аргумента: функцию и аргумент составного типа данных, например, список. map применяет к каждому элементу списка переданную функцию. Например, вы прочитали из файла список чисел, изначально все эти числа имеют строковый тип данных, чтобы работать с ними - нужно превратить их в целое число:\n\
old_list = [1, 2, 3, 4, 5,6, 7]\n\
new_list = list(map(int, old_list))\n\
print (new_list)\n\
[1, 2, 3, 4, 5, 6, 7]\n\
\n\
Функция filter() в Python:\n\
Функция filter предлагает элегантный вариант фильтрации элементов последовательности. Принимает в качестве аргументов функцию и последовательность, которую необходимо отфильтровать:\n\
\n\
mixed = [мак, просо, мак, мак, просо, мак, просо, просо, просо, мак]\n\
zolushka = list(filter(lambda x: x == мак, mixed))\n\
print (zolushka)\n\
[мак, мак, мак, мак, мак]\n\
\n\
Функция reduce() в Python:\n\
Функция reduce принимает 2 аргумента: функцию и последовательность. reduce() последовательно применяет функцию-аргумент к элементам списка, возвращает единичное значение.  «в Python 2.x функция reduce доступна как встроенная, в то время, как в Python 3 она была перемещена в модуль functools.»\n\
\n\
Вычисление суммы всех элементов списка при помощи reduce:\n\
from functools import reduce\n\
items = [1,2,3,4,5]\n\
sum_all = reduce(lambda x,y: x + y, items)\n\
print (sum_all) \n\
15\n\
\n\
'
                 ,
#10
                 
                 'Итераторы в Python':'10.Итераторы в Python: встроенные итераторы, создание собственных итераторов, типичные способы обхода итераторов и принцип их работы. Встроенные функции для работы с итераторами и возможности модуля itertools. Функции генераторы и выражения генераторы: создание и применение в Python.\n\
Итерируемый тип данных - это такой тип, который может возвращать свои элементы по одному. Любой объект, имеющий метод __iter__() , или любая последовательность (то есть объект, имеющий метод__getitem__() , принимающий целочисленный аргумент со значением от 0 и выше), является итерируемым и может предоставлять итератор.\n\
Итератор - это объект, имеющий метод __next__() , который при каждом вызове возвращает очередной элемент и возбуждает исключение StopIteration после исчерпания всех элементов.\n\
\n\
создания собственных итераторов\n\
Самый простой способ создания собственных итераторов в Python — это создание генератора.\n\
squares = (n**2 for n in favorite_numbers)\n\
\n\
обойти итератор\n\
Самый простой способ обойти итератор – использовать цикл for. Мы можем получить доступ к каждому элементу в итераторе, используя цикл for следующим образом.\n\
myList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\
myIter = iter(myList)\n\
print(list is:, myList)\n\
print(Elements in the iterator are:)\n\
for element in myIter:\n\
    print(element)\n\
\n\
Другой способ получить доступ к элементам итератора – использовать функцию next (). Функция next () принимает итератор в качестве входных данных и возвращает следующий элемент, который еще не был пройден, как и метод __next __ ().\n\
\n\
myList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\
myIter = iter(myList)\n\
print(list is:, myList)\n\
print(Elements in the iterator are:)\n\
try:\n\
    print(next(myIter))\n\
    print(next(myIter))\n\
    print(next(myIter))\n\
    print(next(myIter))\n\
except StopIteration as e:\n\
    print(All elements in the iterator already traversed. Raised exception, e)\n\
\n\
\n\
Встроенные функции для работы с итераторами\n\
Две встроенные функции Python, map() и filter(), дублируют функциональность выражения-генератора:\n\
\n\
Встроенной функцией map(f, iterA, iterB, ...) можно заменить цикл for/in, так как она применяет функцию f() ко всем переданным итераторам (по сути, в цикле, тоже выполняются какие-то действия с каждым элементом), и следовательно возвращает итератор значений f(iterA[0], iterB[0]), f(iterA[1], iterB[1]), f(iterA[2], iterB[2]),\n\
\n\
Встроенная функция filter(predicate, iter) возвращает итератор по всем элементам последовательности, которые удовлетворяют определенному условию, и аналогичным образом дублируется при составлении списков. Аргумент predicate - это функция, которая принимает одно значение итерации iter, что-то с ним делать, и в итоге должна возвращать значение bool. Возвращаемое значение True будет говорить функции filter() пропустить значение, False - отбросить.\n\
\n\
возможности модуля itertools\n\
\n\
Бесконечные итераторы.\n\
Модуль itertools поставляется с тремя итераторами, которые могут повторяться бесконечно. Это означает, что при их использовании необходимо понимать, что в конце концов нужно будет как то выходить из этих итераторов, иначе будет бесконечный цикл..\n\
\n\
Итератор itertools.count() будет возвращать равномерно распределенные значения, начиная с числа, которое передается в качестве начального параметра start; этот итератор также принимает параметр шага step.\n\
\n\
Итератор itertools.cycle() позволяет создать итератор, который будет бесконечно циклически перебирать серию значений.\n\
\n\
Итератор itertools.repeat() будет возвращать переданный объект (например словарь, список и т.д. ) снова и снова (бесконечно), если НЕ установить аргумент times, который отвечает за количество повторений.\n\
\n\
Конечные итераторы.\n\
Итератор itertools.accumulate() возвращает накопленные суммы (по умолчанию) или накопленные результаты функции, которую можно передать в качестве второго аргумента. По умолчанию для накопления используется сложение:\n\
\n\
Итератор itertools.chain() берет серию итераций и, по сути, сглаживает их в одну общую итерацию.\n\
\n\
Комбинаторные итераторы.\n\
Модуль itertools содержит четыре итератора, которые можно использовать для создания комбинаций и перестановок данных.\n\
Функция itertools.combinations() позволяет создать итератор со всеми возможными комбинациями элементов входной последовательности.\n\
Итератор itertools.combinations_with_replacement() похож на itertools.combinations(). Единственное отличие заключается в том, что он фактически будет создавать комбинации, в которых элементы действительно повторяются.\n\
Функция itertools.product() предназначена для создания декартовых произведений из серии входных итераций.\n\
Функция itertools.permutations() будет возвращать последовательные перестановки элементов указанной длины из итерации, которая передается в качестве аргумента. Подобно функции itertools.combinations(), перестановки выдаются в лексикографическом порядке сортировки.\n\
\n\
Функции генераторы и выражения генераторы: создание и применение в Python.\n\
Функции-генераторы\n\
Функции-генераторы отличаются от обычных функций тем, что в них есть один или несколько операторов yield.\n\
Создать генератор на Python довольно просто. Он похож на обычную функцию, определяемую ключевым словом def, и использует ключевое слово yield вместо return. Или мы можем сказать, что если тело любой функции содержит оператор yield, он автоматически становится функцией-генератором. Рассмотрим следующий пример:\n\
def simple(): \n\
for i in range(10): \n\
    if(i%2==0): \n\
         yield i \n\
for i in simple(): \n\
    print(i) \n\
\n\
Генератор выражения\n\
Мы можем легко создать выражение генератора без использования пользовательской функции. Это то же самое, что и лямбда-функция, которая создает анонимную функцию; выражения генератора создают анонимную функцию генератора.\n\
\n\
Представление выражения генератора похоже на понимание списка Python. Единственное отличие состоит в том, что квадратные скобки заменены круглыми скобками. Понимание списка вычисляет весь список, тогда как выражение генератора вычисляет один элемент за раз.\n\
# Generator expression \n\
a =(x**3 for x in list)'
                 ,
#11
                 'Специфика массивов как':'11.Специфика массивов, как структур данных. Динамические массивы – специфика работы, сложность операций. Специфика работа с array в Python.\n\
\n\
В классических языках, требуется указывать размер массива и тип данных. \n\
В Питоне нет структуры данных, полностью соответствующей массиву. Однако, есть списки, которые являются их надмножеством, то есть это те же массивы, но с расширенным функционалом. Эти структуры удобнее в использовании, но цена такого удобства, как всегда, производительность и потребляемые ресурсы. И массив, и список – это упорядоченные коллекции, но разница между ними заключается в том, что классический массив должен содержать элементы только одного типа, а список Python может содержать любые элементы.\n\
\n\
Динамический массив похож на массив, но с той разницей, что его размер можно динамически изменять во время выполнения. Не нужно заранее указывать размер массива. Элементы массива занимают непрерывный блок памяти, и после создания его размер не может быть изменен. После заполнения динамический массив может выделить больший кусок памяти, скопировать содержимое из исходного массива в это новое пространство и продолжить заполнять доступные слоты.\n\
\n\
\n\
Модуль array. Массивы в python\n\
Модуль array определяет массивы в python. Массивы очень похожи на списки, но с ограничением на тип данных и размер каждого элемента.\n\
Размер и тип элемента в массиве определяется при его создании \n\
Класс array.array(TypeCode [, инициализатор]) — новый массив, элементы которого ограничены TypeCode, и инициализатор, который должен быть списком, объектом, который поддерживает интерфейс буфера, или итерируемый объект.\n\
array.typecodes — строка, содержащая все возможные типы в массиве.\n\
Массивы изменяемы. Массивы поддерживают все списковые методы (индексация, срезы, умножения, итерации), и другие методы'
                 ,
#12
                 'Абстрактная структура данных':'12.Абстрактная структура данных стек и очередь: базовые и расширенные операции, их сложность.\n\
Стек в Python – это линейная структура данных, в которой данные расположены объектами друг над другом. Он хранит данные в режиме LIFO (Last in First Out). Данные хранятся в том же порядке, в каком на кухне тарелки располагаются одна над другой. Мы всегда выбираем последнюю тарелку из стопки тарелок. В стеке новый элемент вставляется с одного конца, и элемент может быть удален только с этого конца.\n\
empty() – возвращает истину, если стек пуст. Временная сложность O (1).\n\
size() – возвращает длину. Временная сложность O (1).\n\
top() – этот метод возвращает адрес последнего элемента. Временная сложность O (1).\n\
push(g) – метод добавляет элемент ‘g’ в конец стека – временная сложность составляет O (1).\n\
pop() – удаляет самый верхний элемент. Временная сложность O (1).\n\
\n\
\n\
Очередь в Python – это линейный тип структуры данных, используемый для последовательного хранения данных. Ее концепция основана на FIFO (“First in First Out”), что означает «первым пришел – первым обслужен». Или так: «первым пришел – первый вышел». Очередь имеет два конца – спереди и сзади. Следующий элемент вставляется с заднего конца и снимается с переднего конца.\n\
\n\
Enqueue – постановка в очередь – операция, которая добавляет элементы. Является условием, если очередь заполнена. Временная сложность постановки составляет O (1).\n\
Dequeue – это операция, при которой мы удаляем элемент из очереди. Он удаляется в том же порядке, в котором был вставлен. Если очередь пуста, это является условием потери значимости. Временная сложность составляет O (1).\n\
Front – элемент вставлен в переднюю часть. Временная сложность – O (1).\n\
Rear – элемент удален из задней части. Временная сложность задней части O (1).'
                 ,
#13
                 'Специфика реализации и':'13.Специфика реализации и скорости основных операций в очереди на базе массива и связанного списка\n\
 \n\
 Производительность реальизации очереди на базе динамического массива\n\
 \n\
Реализация deque основана на двунаправленных связных списках массивов фиксированной длины. deque поддерживает итерацию, операции len(d), reversed(d), проверку вхождения с помощью оператора in . Операции получения элемента по индексу (такие как d[0] , d[-1] ) быстрые (имеют сложность O(1) для двух концов очереди, но длительные (сложность O(n)) для элементов в середине списка. Т.е. для быстрого произвольного доступа к элементам списка нужно использовать list вместо deque.\n\
\n\
Массив\n\
Массив array хранит непосредственно объекты (а не ссылки на них), что обеспечивает более быстрый доступ и значительно меньший объем памяти для хранения тех же данных (на типе int экономия памяти может составлять 4-5 раз!). Минус: массивы, так же как и в других языках, могут хранить только объекты одного типа.'
                 ,
#14
                 'Связанные списки однонаправленные':'14.Связанные списки: однонаправленные и двунаправленные – принцип реализации. Сравнение скорости выполнения основных операций в связанных списках и в динамическом массиве.\n\
Однонаправленные связанные списки. \n\
Каждый узел ссылается на объект, который является элементом последовательности и на следующий узел списка (или хранит значение None, если в списке больше нет узлов)\n\
 \n\
Упрощенная илюстрация однонаправленного связного списка (для упрощения объекты, являющиесяэлементами последовательности, представлены встроенными в узлы, а не внешними объектами, на которые ссылаются узлы)\n\
\n\
Двунаправленные связанные списки\n\
 \n\
Двойные списки требуют больше места на узел (если не используется XOR-связывание), а их элементарные операции дороже; но ими часто легче манипулировать, поскольку они обеспечивают быстрый и простой последовательный доступ к списку в обоих направлениях. В двусвязном списке можно вставить или удалить узел за постоянное число операций, учитывая только адрес этого узла. Чтобы сделать то же самое в односвязном списке, необходимо иметь адрес указателя на этот узел, который является либо дескриптором всего списка (в случае первого узла), либо полем ссылки в предыдущем узле. Некоторые алгоритмы требуют доступа в обоих направлениях. С другой стороны, двусвязные списки не допускают совместного использования хвостов и не могут использоваться в качестве постоянных структур данных'
                 ,
#15                 
                 'Алгоритм обменной сортировки':'15.Алгоритм обменной сортировки, сложность сортировки и возможности по ее улучшению.\n\
\n\
Обменные сортировки (Bubble Sort)\n\
Алгоритм прямого обмена основывается на сравнении и смене позиций пары соседних элементов.Процесс продолжается до тех пор, пока не будут упорядочены все элементы.\n\
Пример первого прохода алгоритма сортировки пузырьком:\n\
# Сортировка пузырьком:\n\
def bubble_sort(a_list):\n\
for pass_num in range(len(a_list) - 1, 0, -1):\n\
                for i in range(pass_num):\n\
  if a_list[i] > a_list[i + 1]:\n\
                         temp = a_list[i]\n\
                         a_list[i] = a_list[i + 1]\n\
                         a_list[i + 1] = temp\n\
return a_list\n\
\n\
test_list\n\
[54, 26, 93, 17, 77, 31, 44, 55, 20, 65]\n\
\n\
bubble_sort(list(test_list))\n\
[17, 20, 26, 31, 44, 54, 55, 65, 77, 93]'
                 ,
#16
                 'Алгоритм сортировки выбором':'16.Алгоритм сортировки выбором, сложность сортировки и возможности по ее улучшению\n\
Массив делится на уже отсортированную часть:\n\
 \n\
и неотсортированную:\n\
 \n\
На каждом шаге извлекается максимальный элемент из неотсортированной части и ставится в начало отсортированной части. Оптимизация по сравнению с сортировкой пузырьком происходит за счет выполнения только одного обмена за каждый проход через список. В результате каждого прохода находится наибольшее значение в неотсортированной части и устанавливается в корректное место отсортированного фрагмента массива.\n\
Пример работы алгоритма сортировки выбором:'
                 ,
#17
                 'Алгоритм сортировки вставками':'17.Алгоритм сортировки вставками, его сложность. Алгоритм быстрого поиска в отсортированном массиве. Сложность поиска в отсортированном и не отсортированном массиве.\n\
Алгоритм сортировки вставками (Insertion Sort) состоит в пошаговом включении каждого элемента массива в уже отсортированную часть массива. На каждом шаге выбирается очередной элемент и вставляется на соответствующее место в отсортированной части. Сложность сортировки вставками составляет O(n^2), где n - количество элементов в массиве. В лучшем случае (когда массив уже отсортирован) сложность может быть улучшена до O(n).\n\
\n\
Алгоритм быстрого поиска в отсортированном массиве (Binary Search) работает путем деления массива пополам и сравнения искомого значения с элементом в середине массива. Если искомое значение меньше, чем элемент в середине, поиск продолжается в левой половине массива; если больше, то в правой половине. Процесс повторяется до тех пор, пока искомый элемент не будет найден или пока не останется пустая половина массива. Сложность быстрого поиска в отсортированном массиве составляет O(log n), где n - количество элементов в массиве.\n\
\n\
Сложность поиска в неотсортированном массиве без использования дополнительных структур данных (например, хэш-таблиц) составляет O(n), где n - количество элементов в массиве. Поскольку массив не отсортирован, требуется последовательно проверить каждый элемент на совпадение с искомым значением.\n\
\n\
Итак, сложность поиска:\n\
\n\
Отсортированный массив (быстрый поиск): O(log n)\n\
Отсортированный массив (обычный поиск): O(n)\n\
Неотсортированный массив: O(n)'
                 ,
#18
                 'Алгоритм сортировки Шелла':'18.Алгоритм сортировки Шелла, сложность сортировки и возможности по ее улучшению.\n\
Алгоритм сортировки Шелла (Shell Sort) является модификацией алгоритма сортировки вставками. Вместо сравнения и вставки элементов попарно, сортировка Шелла работает с элементами, находящимися на определенном расстоянии друг от друга. Сначала используется большое расстояние (обычно половина длины массива), а затем это расстояние постепенно уменьшается до одного. При каждой итерации элементы находятся на расстоянии шага, и производится сортировка вставками на этом расстоянии. Такой подход позволяет ускорить сортировку, перемещая элементы ближе к своим конечным позициям.\n\
\n\
Сложность сортировки Шелла зависит от выбранной последовательности расстояний между элементами. В худшем случае, когда используется наиболее плохая последовательность, сложность составляет примерно O(n^2). Однако при использовании определенных последовательностей (например, последовательности Шелла), сложность может быть улучшена до O(n log n) или даже O(n^(4/3)).\n\
\n\
Существует несколько способов улучшения сортировки Шелла:\n\
\n\
Выбор оптимальной последовательности расстояний: выбор разных последовательностей может значительно повлиять на производительность алгоритма.\n\
Комбинирование с другими алгоритмами сортировки: можно применить сортировку Шелла в сочетании с другими алгоритмами для получения еще лучших результатов.\n\
Оптимизация вставки: можно улучшить процесс вставки элементов, например, использовать алгоритм бинарного поиска для нахождения правильной позиции вставки.\n\
Однако следует отметить, что сортировка Шелла не является стабильной сортировкой и не обладает свойством сохранения относительного порядка элементов с одинаковыми значениями.\n\
\n\
\n\
Задание: построить базовый класс с указанными в таблице полями и методами:\n\
- конструктор; - функция, которая определяет «качество» объекта – Q по заданной формуле; - метод вывода информации об объекте.\n\
Построить дочерний класс (класс-потомок), который содержит:\n\
- дополнительное поле P;\n\
- функция, которая определяет «качество» объекта дочернего класса – Qp и перегружает функцию качества родительского класса (Q), выполняя вычисление по новой формуле.\n\
Создать проект для демонстрации работы: ввод и вывод информации об объектах классов. (20 баллов)\n\
Поля и методы базового класса Поля и методы дочернего класса\n\
Автомобиль:\n\
- марка автомобиля;\n\
- мощность двигателя (кВт);\n\
- число мест;\n\
- Q = 0,1·мощность ·число мест P: год выпуска\n\
- Qp = Q - 1,5·(T-P),\n\
где T – текущий год\n\
\n\
import datetime\n\
\n\
class Car:\n\
    def init(self, marka, moshnost, chislo_mest):\n\
        self.marka = marka\n\
        self.moshnost = moshnost\n\
        self.chislo_mest = chislo_mest\n\
    \n\
    def kachestvo(self):\n\
        return 0.1 * self.moshnost * self.chislo_mest\n\
    \n\
    def info(self):\n\
        print("Марка:", self.marka)\n\
        print("Мощность двигателя (кВт):", self.moshnost)\n\
        print("Число мест:", self.chislo_mest)\n\
        print("Качество:", self.kachestvo())\n\
\n\
class ChildCar(Car):\n\
    def init(self, marka, moshnost, chislo_mest, date):\n\
        super().init(marka, moshnost, chislo_mest)\n\
        self.P = date\n\
    \n\
    def kachestvo(self):\n\
        year1 = datetime.datetime.now().year\n\
        T = year1\n\
        return super().kachestvo() - 1.5 * (T - self.P)\n\
    \n\
#Пример\n\
car1 = Car("БМВ", 100, 5)\n\
car2 = ChildCar("МЕРСЕДЕС", 150, 4, 2015)\n\
\n\
car1.info()\n\
print()  \n\
car2.info()'
                 ,
#19
                 'Алгоритм быстрой сортировки':'19.Алгоритм быстрой сортировки, сложность сортировки и возможности по ее улучшению\n\
Быстрая сортировка – это алгоритм сортировки, время работы которого для входного массива из n чисел в наихудшем случае равно 𝑂(𝑛^2). Несмотря на такую медленную работу в наихудшем случае, этот алгоритм на практике зачастую оказывается оптимальным благодаря тому, что в среднем время его работы намного лучше: 𝑂(𝑛ln𝑛). Кроме того, постоянные множители, не учтенные в выражении 𝑂(𝑛ln𝑛), достаточно малы по величине. Алгоритм обладает также тем преимуществом, что сортировка в нем выполняется без использования дополнительной памяти, поэтому он хорошо работает даже в средах с виртуальной памятью.\n\
Алгоритм быстрой сортировки является реализацией парадигмы «разделяй и властвуй». Разделение исходного массива осуществляется по следующему принципу:\n\
Выбрать наугад какой-либо элемент массива – х\n\
Просмотреть массив слева направо, пока не обнаружим элемент 𝐴𝑖 > x\n\
Просмотреть массив справа налево, пока не встретим 𝐴𝑖 < х\n\
Поменять местами эти два элемента\n\
Процесс просмотра и обмена продолжается, пока указатели обоих просмотров не встретятся\n\
\n\
def quick_sort(a_list):\n\
    quick_sort_helper(a_list, 0, len(a_list) - 1)\n\
    return a_list\n\
def quick_sort_helper(a_list, first, last):\n\
    if first < last:\n\
        split_point = partition(a_list, first, last)        \n\
        quick_sort_helper(a_list, first, split_point - 1)\n\
        quick_sort_helper(a_list, split_point + 1, last)\n\
def partition(a_list, first, last):\n\
    pivot_value = a_list[first]\n\
    left_mark = first + 1\n\
    right_mark = last\n\
    done = False\n\
    while not done:\n\
        while left_mark <= right_mark and a_list[left_mark] <= pivot_value:\n\
            left_mark = left_mark + 1\n\
        while a_list[right_mark] >= pivot_value and right_mark >= left_mark:\n\
            right_mark = right_mark - 1\n\
        if right_mark < left_mark:\n\
            done = True\n\
        else:\n\
            temp = a_list[left_mark]\n\
            a_list[left_mark] = a_list[right_mark]\n\
            a_list[right_mark] = temp\n\
    temp = a_list[first]\n\
    a_list[first] = a_list[right_mark]\n\
    a_list[right_mark] = temp\n\
    return right_mark\n\
\n\
'
                 ,
#20
                 'Алгоритм сортировки слиянием':'20.Алгоритм сортировки слиянием, сложность сортировки.\n\
Многие полезные алгоритмы имеют рекурсивную структуру: для решения данной задачи они рекурсивно вызывают сами себя один или несколько раз, чтобы решить вспомогательную задачу, имеющую непосредственное отношение к поставленной задаче. Такие алгоритмы зачастую разрабатываются с помощью метода декомпозиции, или разбиения:\n\
• сложная задача разбивается на несколько более простых, которые подобны исходной задаче, но имеют меньший объем;\n\
• далее эти вспомогательные задачи решаются рекурсивным методом, после чего полученные решения комбинируются с целью получить решение исходной задачи.\n\
Парадигма, лежащая в основе метода декомпозиции «разделяй и властвуй», на каждом уровне рекурсии включает в себя три этапа:\n\
1. Разделение задачи на несколько подзадач.\n\
2. Покорение – рекурсивное решение этих подзадач. Когда объем подзадачи достаточно мал, выделенные подзадачи решаются непосредственно.\n\
3. Комбинирование решения исходной задачи из решений вспомогательных задач.\n\
\n\
Алгоритм сортировки слиянием (merge sort) в большой степени соответствует парадигме метода разбиения. На интуитивном уровне его работу можно описать таким образом.\n\
\n\
Разделение: сортируемая последовательность, состоящая из n элементов, разбивается на две меньшие последовательности, каждая из которых содержит n/2 элементов.\n\
Покорение: сортировка обеих вспомогательных последовательностей методом слияния.\n\
Комбинирование: слияние двух отсортированных последовательностей для получения окончательного результата.\n\
\n\
Рекурсия достигает своего нижнего предела, когда длина сортируемой последовательности становится равной 1. В этом случае вся работа уже сделана, поскольку любую такую последовательность можно считать упорядоченной. Основная операция, которая производится в процессе сортировки по методу слияний, – это объединение двух отсортированных последовательностей в ходе комбинирования (последний этап). Это делается с помощью вспомогательной процедуры слияния. В этой процедуре предполагается, что элементы подмассивов упорядочены. Она сливает эти два подмассива в один отсортированный, элементы которого заменяют текущие элементы. Для выполнения этой процедуры требуется время в 𝑂(𝑛) , где 𝑛 – количество подлежащих слиянию элементов.\n\
'
                 ,
#21
                 'Реализация двоичных деревьев':'21.Реализация двоичных деревьев в виде связанных объектов. Различные реализации рекурсивного обхода двоичных деревьев.\n\\n\
\n\\n\
Двоичное (бинарное) дерево (binary tree) — иерархическая \n\\n\
структура данных, в которой каждый узел имеет не более двух \n\\n\
потомков (детей). Обычно, первый называется родительским \n\\n\
узлом, а дети называются левым и правым наследниками. \n\\n\
Прямой (preorder) порядок обхода дерева:\n\
1. Первым просматривается корневой узел.\n\
2. Затем производится рекурсивный прямой обход левого поддерева.\n\
3. Затем производится рекурсивный прямой обход правого поддерева. \n\
\n\
Обратный (postorder) порядок обхода дерева.\n\
1. Первым производится рекурсивный обратный обход левого поддерева.\n\
2. Затем производится рекурсивный обратный обход правого поддерева.\n\
3. Затем производится корневой узел.\n\
\n\\n\
Симметричный (inorder) порядок обхода дерева:\n\\n\
Первым производится рекурсивный симметричный обход левого поддерева.\n\\n\
Затем просматривается корневой узел\n\\n\
Затем производится рекурсивный симметричный обход правого поддерева'
                 ,
#22
                 'Двоичное дерево поиска':'22.Двоичное дерево поиска – принципы реализации и логика реализации основных операций.\n\
Двоичное дерево поиска (binary search tree, BST) — это двоичное дерево, для которого выполняются следующие дополнительные условия (свойства дерева поиска):\n\
1. Оба поддерева — левое и правое — являются двоичными деревьями поиска.\n\
2. У всех узлов левого поддерева произвольного узла X значения ключей данных меньше, нежели значение ключа данных самого узла X.\n\
3. У всех узлов правого поддерева произвольного узла X значения ключей данных больше либо равно, нежели значение ключа данных самого узла X.\n\
Очевидно, данные в каждом узле должны обладать ключами, на которых определена операция сравнения (например, операция меньше).\n\
\n\
Основные операции в бинарном дереве поиска выполняются за время, пропорциональное его высоте. Для полного бинарного дерева с 𝑛n узлами эти операции выполняются за время 𝑂(ln𝑛) в наихудшем случае. Математическое ожидание высоты построенного случайным образом бинарного дерева равно О(ln𝑛) так что все основные операции динамическим множеством в таком дереве выполняются в среднем за время Θ(ln𝑛).\n\
На практике мы не всегда можем гарантировать случайность построения бинарного дерева поиска, однако имеются версии деревьев, в которых гарантируется хорошее время работы в наихудшем случае.\n\
Речь идет о деревьях сбалансированных по высоте по определенным критериям, это:\n\
• АВЛ –деревья\n\
• 2-3, 3-4 деревья\n\
• красно-черные деревья\n\
высота которых определяется как О(ln𝑛)\n\
\n\
Алгоритм вставки нового узла в двоичное дерево поиска:\n\
1. Начинаем просмотр с корня дерева (первый текущий узел - корень).\n\
2. Сравниваем значение нового узла со значением в текущем узле. Если значение в новом узле меньше, то продолжаем поиск в левом поддереве (текущим узлом становится левый дочерний узел предыдущего текущего узла). Если значение в новом узле больше чем в текущем узле, то продолжаем поиск в правом поддереве.\n\
3. Если левого или правого поддерева не существует, то мы обнаружили место для вставки нового элемента. На это место вставляется новый узел дерева.\n\
Алгоритм вставки в бинарное дерево, который мы только что рассмотрели, дает хорошие результаты при использовании случайных входных данных, но все же существует неприятная возможность того, что при этом будет построено вырожденное дерево. Можно было бы разработать алгоритм, поддерживающий дерево в оптимальном состоянии все время, где под оптимальностью мы в данном случае понимаем сбалансированность дерева.\n\
Идеально сбалансированным называется дерево, у которого для каждой вершины выполняется требование: число вершин в левом и правом поддеревьях различается не более чем на 1.\n\
Поддержка идеальной сбалансированности, к сожалению, очень сложная задача. Другая идея заключается в том, чтобы ввести менее жесткие критерии сбалансированности и на их основе предложить достаточно простые алгоритмы обеспечения этих критериев.'
                 ,
#23
                 'Двоичная куча принципы':'23.Двоичная куча – принципы реализации и логика реализации основных операций.\n\
Двоичная куча (пирамида) (binary heap) — такое двоичное дерево, для которого выполнены три условия:\n\
1. Значение в любой вершине не больше, чем значения её потомков.\n\
2. Уровень всех листьев (расстояние до корня) отличается не более чем на 1.\n\
3. Последний уровень заполняется слева направо без «дырок».\n\
\n\
Для гарантированной логарифмической производительности мы дложны поддержвать двоичную кучу в виде сбалансированного дерева. Для этого мы будем строить двоичную кучу в виде полного бинарного дерева - дерева в котором каждый уровень кроме последнего содержит все возможные узлы, а последний уровень заполняется с лева на право без пропусков.\n\
\n\
Важным свойством полного бинарного дерева является то, что такое дерево может быть представленно в виде одного списка. Левый потомок родителя (имеющего индекс p) является элеменотом списка с индексом 2p. Аналогично, правый потомок является элеменотом списка с индексом 2p + 1. Для того, чтобы найти индекс родительского узла нужно взять целую часть от индекса элемента, разделенного на 2.\n\
Базовые операции для двоичной кучи:\n\
• BinaryHeap() - создает новую пустую бинарную кучу\n\
• insert(k) - добавить элемент в кучу, cложность 𝑂(log𝑛)\n\
• find_min() - возввратить минимальный элемент в куче, сложность 𝑂(1)\n\
• del_min() - возввратить минимальный элемент и исключить его из кучи, cложность 𝑂(log𝑛)\n\
• is_empty() - возвращает True если куча пуста и False в обратном случае\n\
• size() - количество элементов в куче\n\
• build_heap(list) - создает новую кучу на основе произвольного (не упроядоченного) массива, сложность 𝑂(𝑛)\n\
Отсортировать массив путём превращения его в кучу, а кучи в отсортированный массив. Время работы 𝑂(𝑛log𝑛)\n\
Реализация метода del_min:\n\
Свойства кучи требуют, чтобы корень дерева был наименьшим элементом в дереве. Таким образом найти наименьший элемент просто.\n\
Сложной частью операции del_min является восстановление корректной структуры кучи и ее свойств после удаления корневого элемента.\n\
1. Мы восстановим корневой элемент установив на его место элемент, изъятый из последней позиции кучи (последний элемент в представлении кучи в виде списка). Таким образом будет получена корректная структура дерева для кучи, но при этом может быть нарушено правило порядка расположения элементов в куче.\n\
2. Восстановление порядка элементов в куче будет выполнено за счет проталкивания нового корневого элемента на корректную позицию. При проталкивании элемент при необходимости будет опускаться на место своего наименьшего потомка.'
                 ,
#24
                 'Абстрактный тип данных':'24.Абстрактный тип данных - ассоциативный массив и принцип его реализации на основе хэш-таблиц и хэш-функций.\n\
\n\
Словарь (ассоциативного массива (map, dictionary, associative array)) - абстрактная структура данных позволяющая хранить пары вида ключ - значение и поддерживающая операции добавления пары, а также поиска и удаления пары по ключу. Предполагается, что ассоциативный массив не может хранить две пары с одинаковыми ключами. Ассоциативный массив с точки зрения интерфейса удобно рассматривать как обычный массив, в котором в качестве индексов можно использовать не только целые числа из определенного диапазона, но и значения других типов — например, строки.\n\
В Python словарь реализуется при помощи dict() .\n\
\n\
Хеш-таблица представляет собой эффективную структуру данных для реализации словарей. Хотя на поиск элемента в хеш-таблице может в наихудшем случае потребоваться столько же времени, что и в связанном списке, а именно 𝑂(𝑛), на практике хеширование исключительно эффективно. При вполне обоснованных допущениях математическое ожидание времени поиска элемента в хеш-таблице составляет 𝑂(1).\n\
Хеш-таблица (hash table) представляет собой обобщение обычного массива. Если количество реально хранящихся в массиве ключей мало по сравнению с количеством возможных значений ключей, эффективной альтернативой массива с прямой индексацией становится хеш-таблица, которая обычно использует массив с размером, пропорциональным количеству реально хранящихся в нем ключей.\n\
\n\
Вместо непосредственного использования ключа в качестве индекса массива, индекс вычисляется по значению ключа. Идея хеширования состоит в использовании некоторой частичной информации, полученной из ключа, т.е. вычисляется хеш-адрес ℎ(𝑘𝑒𝑦), который используется для индексации в хеш-таблице.\n\
\n\
Когда множество К хранящихся в словаре ключей гораздо меньше пространства возможных ключей 𝑈, хеш-таблица требует существенно меньше места, чем таблица с прямой адресацией. Точнее говоря, требования к памяти могут быть снижены до Θ(|𝐾|), при этом время поиска элемента в хеш-таблице остается равным 𝑂(1).\n\
•	Надо заметить, что это граница среднего времени поиска, в то время как в случае таблицы с прямой адресацией эта граница справедлива для наихудшего случая.\n\
В случае прямой адресации элемент с ключом 𝑘 хранится в ячейке 𝑘. При хешировании этот элемент хранится в ячейке ℎ(𝑘), т.е. мы используем хеш-функцию ℎ для вычисления ячейки для данного ключа 𝑘. Функция ℎ отображает пространство ключей 𝑈 на ячейки хеш-таблицы Т[0..𝑚−1]:\n\
ℎ:𝑈→{0,1,…,𝑚−1}.\n\
Мы говорим, что элемент с ключом 𝑘 хешируется в ячейку ℎ(𝑘), величина ℎ(𝑘) называется хеш-значением ключа 𝑘.\n\
\n\
Пример\n\
𝑇[0,…,10]; ℎ(𝑘)=𝑘mod11\n\
 \n\
При построении хеш-таблиц есть одна проблема: два ключа могут быть хешированы одну и ту же ячейку. Такая ситуация называется коллизией.\n\
\n\
Т.к. ℎh является детерминистической и для одного и того же значения k всегда дает одно и то же хеш-значение ℎ(𝑘)h(k), то поскольку |𝑈|>𝑚|U|>m, должно существовать как минимум два ключа, которые имеют одинаковое хеш-значение. Таким образом, полностью избежать коллизий невозможно в принципе.\n\
Используются два подхода для борьбы с этой проблемой:\n\
•	выбор хеш-функции снижающей вероятность коллизии;\n\
•	использование эффективных алгоритмов разрешения коллизий.\n\
\n\
\n\
Хеш-функция выполняет преобразование массива входных данных произвольной длины (ключа, сообщения) в (выходную) битовую строку установленной длины (хеш, хеш-код, хеш-сумму).\n\
\n\
Хеш-функции применяются в следующих задачах:\n\
•	построение ассоциативных массивов;\n\
•	поиске дубликатов в сериях наборов данных;\n\
•	построение уникальных идентификаторов для наборов данных;\n\
•	вычислении контрольных сумм от данных (сигнала) для последующего обнаружения в них ошибок (возникших случайно или внесённых намеренно), возникающих при хранении и/или передаче данных;\n\
•	сохранении паролей в системах защиты в виде хеш-кода (для восстановления пароля по хеш-коду требуется функция, являющаяся обратной по отношению к использованной хеш-функции);\n\
•	выработке электронной подписи (на практике часто подписывается не само сообщение, а его «хеш-образ»); и многих других.\n\
Для решения различных задач требования к хеш-функциям могут очень существенно отличаться.\n\
\n\
Для обеспечения минимального количества коллизий хеш-функция удовлетворяет (приближенно) предположению простого равномерного хеширования: для каждого ключа равновероятно помещение в любую из 𝑚 ячеек, независимо от хеширования остальных ключей. К сожалению, это условие обычно невозможно проверить, поскольку, как правило, распределение вероятностей, в соответствии с которым поступают вносимые в таблицу ключи, неизвестно; кроме того, вставляемые ключи могут не быть независимыми.\n\
\n\
При построении хеш-функции хорошим подходом является подбор функции таким образом, чтобы она никак не коррелировала с закономерностями, которым могут подчиняться существующие данные.\n\
\n\
Например, можно потребовать:\n\
\n\
чтобы близкие в некотором смысле ключи давали далекие хеш-значения (например, хеш функция для подряд идущих целых чисел давала далекие хеш-значения).\n\
или противоположное, непрерывность: близкие в некотором смысле ключи давали близкие хеш-значения\n\
близкие ключи длолжны порождать близкие хеш-значения'
                 ,                 
#25
                 'Общая схема построения':'25.Общая схема построения хэш-функции и возможная роль в этой схеме хэш-функции multiply-add-and-divide. Принцип работы хэш-функции multiply-add-and-divide.\n\
При построении хеш-функции хорошим подходом является подбор функции таким образом, чтобы она никак не коррелировала с закономерностями, которым могут подчиняться существующие данные.\n\
Например, можно потребовать:\n\
• чтобы близкие в некотором смысле ключи давали далекие хеш-значения (например, хеш функция для подряд идущих целых чисел давала далекие хеш-значения).\n\
• или противоположное, непрерывность: близкие в некотором смысле ключи давали близкие хеш-значения\n\
 близкие ключи длолжны порождать близкие хеш-значения\n\
\n\
Функция MAD может использоваться и в качестве функции построения хеш-кода для целых чисел и в качестве функции компрессии для хеш-кодов, построенных с помощью других функций.\n\
\n\
Хеш-функция multiply-add-and-divide (часто именуемая как MAD) преобразует целое число 𝑘k по следующему алгоритму. У хеш-функци имеются следующие параметры: 𝑝p - большое простое число, 𝑎∈{1,2,…,𝑝−1}a∈{1,2,…,p−1} и 𝑏∈{0,1,…,𝑝−1}b∈{0,1,…,p−1}, 𝑚 - количество значений в диапозоне значений хеш-функции.\n\
h(k) = ((a*k + b) mod(p))*mod(m)\n\
Этот класс хеш-функций удобен тем, что размер 𝑚m выходного диапазона произволен и не обязательно представляет собой простое число. Поскольку число, а можно выбрать р−1способом, и рр способами – число 𝑏b, всего в данном семействе будет содержаться р(р−1) хеш-функций.'
                 ,
#26
                 'Полиномиальная хэш функция':'26.Полиномиальная хэш-функция – принцип работы, специфика эффективной реализации и специфика применения хэш-функции\n\
\n\
 Примером такой хеш-функции является функция, использующая константу 𝑎a (𝑎≠0,𝑎≠) при построении хеш-функции вида:\n\
X0*an-1 + X1*an-2 + … + Xn – 2*a + Xn-1\n\
Т.е. это полином, использующий элементы массива входных данных (𝑥0,𝑥1,…,𝑥𝑛−1) в качестве коэффициентов. Такая функция назвается полиниомиальным хеш-кодом. Для использования ее в качестве хеш-функции к ней необходимо только добавить функцию компресии в соответствующий диапозон значений.\n\
Используя схему Горнера полиномиальный хеш-код можно эффективно вычислить по формуле:\n\
Xn-1 + a(xn-2 + a(xn-3 + … + a(x2 + a(x1 + ax0))…))\n\
Важным правилом реализации функции hash для классов явлется необходимость сохранять консистентность между равенством (x == y) и равенством хеш-функций (hash(x) == hash(y)).\n\
• Для любых двух объектов из равенства x == y должно следовать hash(x) == hash(y)\n\
• Из-за возможности коллизий у хеш-функций следствие в обратную сторону в общем случае не выполняется\n\
Это необходимо для того, чтобы в случае использования объекта в качестве ключа в хеш таблицы для равных объектов (x == y) результат поиска в таблице (который ведется с ипользованием hash(x), hash(y)) был идентичен.'
                 ,
#27
                 'Различные методы разрешения':'27.Различные методы разрешения коллизий в хэш-таблицах.\n\
Разрешение коллизий при помощи цепочек. При использовании данного метода все элементы, хешированные в одну и ту же ячейку, объединяются в связанный список, как показано на рис.\n\
•	Ячейка j или содержит указатель на заголовок списка всех элементов, хеш-значение ключа которых равно j\n\
•	Если таких элементов нет, то ячейка содержит значение None\n\
 \n\
Линейное исследование\n\
Пусть задана обычная хеш-функция ℎʹ:𝑈→{0,1,…,𝑚−1}, которую мы будем в дальнейшем именовать вспомогательной хеш-функцией (auxiliary hash function). Метод линейного исследования для вычисления последовательности исследований использует хеш-функцию\n\
ℎ(𝑘,𝑖)=(ℎʹ(𝑘)+𝑖)mod𝑚\n\
Линейное исследование легко реализуется, однако с ним связана проблема первичной кластеризации, связанной с созданием длинных последовательностей занятых ячеек, что, увеличивает среднее время поиска. Кластеры возникают в связи с тем, что вероятность заполнения пустой ячейки, которой предшествуют 𝑖i заполненных ячеек, равна (𝑖+1)/𝑚. Таким образом, длинные серии заполненных ячеек имеют тенденцию к все большему удлинению, что приводит к увеличению среднего времени поиска.\n\
 \n\
\n\
Квадратичное исследование\n\
Квадратичное исследование использует хеш-функцию вида:\n\
ℎ(𝑘,𝑖)=(ℎʹ(𝑘)+с1𝑖+с2𝑖2)mod𝑚\n\
где ℎʹhʹ – вспомогательная хеш-функция, с1 и с2≠– вспомогательные константы, а 𝑖 принимает значения от 0 до 𝑚−1m−1 включительно.\n\
Начальная исследуемая ячейка - Т[ℎʹ(𝑘)] остальные исследуемые позиции смещены относительно нее на величины, которые описываются квадратичной зависимостью от номера исследования 𝑖.\n\
Этот метод работает существенно лучше линейного исследования, но для того, чтобы исследование охватывало все ячейки, необходим выбор специальных значений, с2с2 и 𝑚 . Кроме того, если два ключа имеют одну и то же начальную позицию исследования, то одинаковы и последовательности исследования в целом.\n\
\n\
Двойное хеширование\n\
Двойное хеширование представляет собой один из наилучших способов использования открытой адресации, поскольку получаемые при этом перестановки обладают многими характеристиками случайно выбираемых перестановок. Двойное хеширование использует хеш-функцию вида\n\
\n\
ℎ(𝑘,𝑖)=(ℎ1(𝑘)+𝑖ℎ2(𝑘))mod𝑚\n\
\n\
где ℎ1 и ℎ2 – вспомогательные хеш-функции. Начальное исследование выполняется в позиции Т[ℎ1(𝑘))], а смещение каждой из последующих исследуемых ячеек относительно предыдущей равно ℎ2(𝑘) по модулю 𝑚.\n\
В отличие от линейного и квадратичного исследования, в данном случае последовательность исследования зависит от ключа 𝑘 по двум параметрам – в плане выбора начальной исследуемой ячейки и расстояния между соседними исследуемыми ячейками, так как оба эти параметра зависят от значения ключа. Производительность двойного хеширования достаточно близка к производительности идеальной схемы равномерного хеширования.\n\
\n\
\n\
'
                 }
        print(sklad[number])

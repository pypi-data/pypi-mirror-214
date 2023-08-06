def choice3(key):
    stack = '''
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    class Stack:
        def __init__(self):
            self.head = None

        def is_empty(self):
            return self.head is None

        def push(self, node):
            node.next = self.head
            self.head = node

        def pop(self):
            if self.is_empty():
                return None
            else:
                popped_item = self.head
                self.head = self.head.next
                return popped_item

        def __str__(self):
            current = self.head
            stack_str = ""
            while current:
                stack_str += str(current.data) + " → "
                current = current.next
            return stack_str.rstrip(" → ") 
    '''
    queue = '''
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    class Queue:
        def __init__(self):
            self.head = None
            self.tail = None

        def is_empty(self):
            return not bool(self.head)

        def enqueue(self, data):
            new_node = Node(data)
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node

        def dequeue(self):
            data = self.head.data
            self.head = self.head.next
            if not self.head:
                self.tail = None
            return data

        def __len__(self):
            count = 0
            current = self.head
            while current:
                count += 1
                current = current.next
            return count

        def __str__(self):
            current = self.head
            queue_str = ""
            while current:
                queue_str += " → " + str(current.data)
                current = current.next
            return queue_str.lstrip(" → ")  
    '''
    dll = '''
    class Node:
        def __init__(self, data):
            self.data = data
            self.prev = None
            self.next = None

    class DoublyLinkedList:
        def __init__(self):
            self.head = None

        def append(self, data):
            new_node = Node(data)
            if self.head is None:
                self.head = new_node
            else:
                current = self.head
                while current.next is not None:
                    current = current.next
                current.next = new_node
                new_node.prev = current

        def remove(self, data):
            if self.head is None:
                return
            elif self.head.data == data:
                if self.head.next is not None:
                    self.head = self.head.next
                    self.head.prev = None
                else:
                    self.head = None
            else:
                current = self.head
                while current.next is not None and current.next.data != data:
                    current = current.next
                if current.next is None:
                    return
                else:
                    current.next = current.next.next
                    if current.next is not None:
                        current.next.prev = current

        def __len__(self):
            count = 0
            current = self.head
            while current:
                count += 1
                current = current.next
            return count

        def __str__(self):
            if self.head == None:
                return f"Двусвязный список пустой"
            current = self.head
            dllist_str = ""
            while current:
                dllist_str += " ⇄ " + str(current.data)
                current = current.next
            return dllist_str.lstrip(" ⇄ ")  
    '''
    ins_s = '''
    def insertion_sort(arr, reverse=False):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and ((not reverse and arr[j] > key) or (reverse and arr[j] < key)):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    '''
    q_s = '''
    def quick_sort(arr, reverse=False):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            left = []
            right = []
            for i in range(1, len(arr)):
                if arr[i] < pivot:
                    left.append(arr[i])
                else:
                    right.append(arr[i])
            if reverse:
                return quick_sort(right, reverse=True) + [pivot] + quick_sort(left, reverse=True)
            else:
                return quick_sort(left) + [pivot] + quick_sort(right)
    '''
    b_s = '''
    def bubble_sort(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if not reverse:
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                else:
                    if arr[j] < arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    '''
    sel_s = '''
    def selection_sort(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if reverse:
                    if arr[j] > arr[min_idx]:
                        min_idx = j
                else:
                    if arr[j] < arr[min_idx]:
                        min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    '''
    uslovia = ['Написать функцию, которая принимает на вход список слов и сортирует его по алфавиту с помощью алгоритма сортировки вставками. Функция должна возвращать отсортированный список.'
               'Написать метод класса «Товар», который сортирует список товаров по цене с помощью алгоритма быстрой сортировки. Метод должен изменять исходный список.'
               'Написать функцию, которая принимает на вход список дат и сортирует его по возрастанию с помощью алгоритма сортировки пузырьком. Функция должна возвращать отсортированный список.'
               'Написать функцию, которая принимает на вход список строк и сортирует его по длине строк с помощью алгоритма сортировки выбором. Функция должна возвращать отсортированный список.'
               'Написать метод класса «Клиент», который сортирует список клиентов по возрасту с помощью алгоритма сортировки пузырьком. Метод должен изменять исходный список.'
               'Написать функцию, которая принимает на вход список чисел и сортирует его по убыванию с помощью алгоритма сортировки вставками. Функция должна возвращать отсортированный список.'
               'Написать метод класса «Заказ», который сортирует список заказов по дате с помощью алгоритма быстрой сортировки. Метод должен изменять исходный список.']
    z15 = '''
    def insertion_sort_words(words, reverse=False):
        for i in range(1, len(words)):
            key = words[i]
            j = i - 1
            while j >= 0 and ((not reverse and words[j] > key) or (reverse and words[j] < key)):
                words[j + 1] = words[j]
                j -= 1
            words[j + 1] = key
        return words
    words = ['xxxx', 'apple', 'banana', 'cherry', 'eeea', 'date', 'elderberry']
    sorted_words = insertion_sort_words(words)
    print(sorted_words)
    
    sorted_words_reverse = insertion_sort_words(words, reverse=True)
    print(sorted_words_reverse)
    '''
    z16 = '''
    class Product:
        def __init__(self, name, price):
            self.name = name
            self.price = price
    
        def __repr__(self):
            return f"{self.name}: {self.price}"
    
        @staticmethod
        def quick_sort_products(products, reverse=False):
            if len(products) <= 1:
                return products
            else:
                pivot = products[0].price
                left = []
                right = []
                for i in range(1, len(products)):
                    if products[i].price < pivot:
                        left.append(products[i])
                    else:
                        right.append(products[i])
                if reverse:
                    return Product.quick_sort_products(right, reverse=True) + [products[0]] + Product.quick_sort_products(left, reverse=True)
                else:
                    return Product.quick_sort_products(left) + [products[0]] + Product.quick_sort_products(right)
    
    products = [Product("Товар 1", 100), Product("Товар 2", 50), Product("Товар 3", 200), Product("Товар 4", 75)]
    print(products)
    products = Product.quick_sort_products(products)
    print(products)
    '''
    z17 = '''
    def bubble_sort_dates(dates, reverse = False):
        n = len(dates)
        for i in range(n):
            for j in range(n - i - 1):
              if not reverse:
                if dates[j] > dates[j + 1]:
                    dates[j], dates[j + 1] = dates[j + 1], dates[j]
              else:
                if dates[j] < dates[j+1]:
                    dates[j], dates[j+1] = dates[j+1], dates[j]
        return dates
    dates = ['2022-01-01', '2021-12-31', '2022-12-31', '2021-01-01']
    print(dates)
    sorted_dates = bubble_sort_dates(dates)
    print(sorted_dates)
    '''
    z18 = '''
    def selection_sort_by_length(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if reverse:
                    if len(arr[j]) > len(arr[min_idx]):
                        min_idx = j
                else:
                    if len(arr[j]) < len(arr[min_idx]):
                        min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    my_list = ['apple', 'banana', 'pear', 'orange', 'kiwi']
    sorted_list = selection_sort_by_length(my_list)
    print(sorted_list)
    '''
    z19 = '''
    class Client:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
        def __repr__(self):
            return f"{self.name}: {self.age}"
    
        @staticmethod
        def bubble_sort(arr, reverse=False):
          n = len(arr)
          for i in range(n):
            for j in range(n - i - 1):
              if not reverse:
                if arr[j].age > arr[j + 1].age:
                  arr[j], arr[j + 1] = arr[j + 1], arr[j]
              else:
                if arr[j].age < arr[j + 1].age:
                  arr[j], arr[j + 1] = arr[j + 1], arr[j]
          return arr
    c1 = Client('Валерий', 18)
    c2 = Client('Кирилл', 19)
    c3 = Client('Руслан', 55)
    c4 = Client('Даша', 12)
    clients = [c1,c2,c3,c4]
    print(clients)
    Client.bubble_sort(clients)
    print(clients)
    '''
    z20 = '''
    lst = [24,1,51,2,45,5,6,1023,10]
    def insertion_sort(arr, reverse=False):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and ((not reverse and arr[j] > key) or (reverse and arr[j] < key)):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    print(lst)
    insertion_sort(lst)
    lst
    '''
    z21 = '''
    class Order:
        def __init__(self, name, date):
            self.name = name
            self.date = date
    
        def __repr__(self):
            return f"{self.name}: {self.date}"
    
        @staticmethod
        def quick_sort(lst, reverse=False):
            if len(lst) <= 1:
                return lst
            else:
                pivot = lst[0].date
                left = []
                right = []
                for i in range(1, len(lst)):
                    if lst[i].date < pivot:
                        left.append(lst[i])
                    else:
                        right.append(lst[i])
                if reverse:
                  lst[:] = Order.quick_sort(right, reverse=True) + [lst[0]] + Order.quick_sort(left, reverse=True)
                  return lst
                else:
                  lst[:] = Order.quick_sort(left) + [lst[0]] + Order.quick_sort(right)
                  return lst
    
    ord1 = Order('Телевизор', '2022-01-01')
    ord2 = Order('Автомобиль', '2021-12-31')
    ord3 = Order('Антенна', '2022-12-31')
    ord4 = Order('Игрушка', '2021-01-01')
    print(ord1.date)
    orders = [ord1,ord2,ord3,ord4]
    print(orders)
    Order.quick_sort(orders)
    print(orders)
    '''
    z22 = '''
    class Node:
        def __init__(self, data):
          self.data = data
          self.left = None
          self.right = None        
    
    class BinaryTree:
        def __init__(self):
            self.root = None
    
        def insert(self, data):
            new_node = Node(data)
            if self.root is None:
                self.root = new_node
            else:
                current = self.root
                while True:
                    if data < current.data:
                        if current.left is None:
                            current.left = new_node
                            break
                        else:
                            current = current.left
                    else:
                        if current.right is None:
                            current.right = new_node
                            break
                        else:
                            current = current.right
    
        def search(self, data):
            current = self.root
            while current is not None:
                if data == current.data:
                    return True
                elif data < current.data:
                    current = current.left
                else:
                    current = current.right
            return False
    
        def delete(self, data):
            if self.root is not None:
                self.root = self._delete(data, self.root)
    
        def _delete(self, data, node):
            if node is None:
                return node
    
            if data < node.data:
                node.left = self._delete(data, node.left)
            elif data > node.data:
                node.right = self._delete(data, node.right)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
    
                temp = self._find_min_node(node.right)
                node.data = temp.data
                node.right = self._delete(temp.data, node.right)
    
            return node
    
        def _find_min_node(self, node):
            while node.left is not None:
                node = node.left
            return node
    
        def _display(self, node, level=0):
          if node is not None:
            self._display(node.right, level+1)
            print("\t" * level, "->", node.data)
            self._display(node.left, level+1)
    
        def display(self):
          self._display(self.root)
    
        def find_largest_smaller_than(self, data):
            current = self.root
            largest_smaller = None
            while current is not None:
              if current.data < data:
                if largest_smaller is None or current.data > largest_smaller:
                    largest_smaller = current.data
                current = current.right
              else:
                  current = current.left
            return largest_smaller
    
    bt = BinaryTree()
    bt.insert(5)
    bt.insert(2)
    bt.insert(8)
    bt.insert(1)
    bt.insert(3)
    bt.insert(1)
    bt.insert(2)
    bt.insert(16)
    bt.insert(7)
    bt.display()
    #bt.find_largest_smaller_than(5)
    '''
    z23 = '''
    class Node:
        def __init__(self, data):
          self.data = data
          self.left = None
          self.right = None        
    
    class BinaryTree:
        def __init__(self):
            self.root = None
    
        def insert(self, data):
            new_node = Node(data)
            if self.root is None:
                self.root = new_node
            else:
                current = self.root
                while True:
                    if data < current.data:
                        if current.left is None:
                            current.left = new_node
                            break
                        else:
                            current = current.left
                    else:
                        if current.right is None:
                            current.right = new_node
                            break
                        else:
                            current = current.right
    
        def search(self, data):
            current = self.root
            while current is not None:
                if data == current.data:
                    return True
                elif data < current.data:
                    current = current.left
                else:
                    current = current.right
            return False
    
        def delete(self, data):
            if self.root is not None:
                self.root = self._delete(data, self.root)
    
        def _delete(self, data, node):
            if node is None:
                return node
    
            if data < node.data:
                node.left = self._delete(data, node.left)
            elif data > node.data:
                node.right = self._delete(data, node.right)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
    
                temp = self._find_min_node(node.right)
                node.data = temp.data
                node.right = self._delete(temp.data, node.right)
    
            return node
    
        def _find_min_node(self, node):
            while node.left is not None:
                node = node.left
            return node
    
        def _display(self, node, level=0):
          if node is not None:
            self._display(node.right, level+1)
            print("\t" * level, "->", node.data)
            self._display(node.left, level+1)
    
        def display(self):
          self._display(self.root)
    
        def height(self, node):
            if node is None:
                return 0
            else:
                left_height = self.height(node.left)
                right_height = self.height(node.right)
                return max(left_height, right_height) + 1
    
        def get_height(self):
            return self.height(self.root)
    
    bt = BinaryTree()
    bt.insert(5)
    bt.insert(2)
    bt.insert(8)
    bt.insert(1)
    bt.insert(3)
    bt.insert(1)
    bt.insert(2)
    bt.insert(16)
    bt.insert(7)
    bt.get_height()
    '''
    z25 = '''
    class Book:
        def __init__(self, title, author, year):
            self.title = title
            self.author = author
            self.year = year
        def __str__(self):
          return f'Название {self.title}, автор: {self.author}, год: {self.year}'
    class HashTable:
        def __init__(self, size):
            self.size = size
            self.table = [[] for _ in range(self.size)]
    
        def hash_function(self, key):
            return hash(key) % self.size
    
        def insert(self, book):
            slot = self.hash_function(book.author)
            for pair in self.table[slot]:
                if pair[0] == book.author:
                    pair[1].append(book)
                    return
            self.table[slot].append((book.author, [book]))
    
        def find(self, author):
            slot = self.hash_function(author)
            for pair in self.table[slot]:
                if pair[0] == author:
                    return pair[1]
            return None
    
    ht = HashTable(10)
    book1 = Book("Преступление и наказание", "Федор Достоевский", 1866)
    book2 = Book("Война и мир", "Лев Толстой", 1869)
    book3 = Book("Идиот", "Федор Достоевский", 1869)
    ht.insert(book1)
    ht.insert(book2)
    ht.insert(book3)
    for book in (ht.find('Федор Достоевский')):
      print(book)

    '''
    d = {'стек': stack,
    'очередь': queue, 
    'двусвязный список': dll, 
    'вставками': ins_s, 
    'пузырьком': b_s,
    'быстрая': q_s, 
    'выбором': sel_s,
    'метод класса заказ': z21,
    'список чисел вставками': z20,
    'метод класса клиент': z19,
    'список строк выбором': z18,
    'список дат пузырьком': z17,
    'метод класса товар': z16,
    'список слов вставками': z15,
    'наибольший дерево': z22,
    'высота дерева': z23,
    'хеш-таблица': z25
         }
    print(d[key])

def info():
    d = {'стек': 1,
         'очередь': 2,
         'двусвязный список': 3,
         'вставками': 4,
         'пузырьком': 5,
         'быстрая': 6,
         'выбором': 7,
         'метод класса заказ': 8,
         'список чисел вставками': 9,
         'метод класса клиент': 10,
         'список строк выбором': 11,
         'список дат пузырьком': 12,
         'метод класса товар': 13,
         'список слов вставками': 14,
        'наибольший дерево': 15,
        'высота дерева': 16,
        'хеш-таблица': 17
         }
    print(d.keys())

def choice2(key):
    anagram = '''
    lst = ['парк', 'карп', 'среда', 'антон', 'андрей', 'адрес', 'топор', 'грот', 'торг', 'ропот', 'повтор']
    a = set()
    f = lambda x, y: all((x.count(i) == y.count(i) and len(x) == len(y)) for i in x)
    for i in range(0, len(lst) - 1):
      for j in range(i+1, len(lst)):
        if f(lst[i],lst[j]):
          a.add(lst[i])
          a.add(lst[j])
    print(a)
    '''
    isprime = '''
    isprime = lambda x: x > 0 and all(x % i for i in range(2, int(x ** 0.5) + 1))
    '''
    kv_sum = '''
    result_list = list(filter(lambda x: any(x == a*a + b*b for a in range(0, x) for b in range(0, x)), range(1, 50+1)))
    '''
    glasnie = '''
    gl = list('ауоыиэяюёе')
    print(sorted(lst, key = lambda x : sum(1 for i in x if i in gl)))
    '''
    capr = '''
    def chisla(element):
      s = str(element ** 2)
      for i in range(0, len(s)):
        a = s[:i+1]
        b = s[i+1:]
        ch = 0
        if a != '': a = int(a)
        if b != '': b = int(b)
        if type(a) == int and type(b) == int:
          if a == 0 or b == 0:
            break
          else:
            ch = a + b
            if ch == element:
              return True
    print(list(filter(lambda x: chisla(x), lst)))
    '''
    armstrong = '''
    armstrong_nums = list(filter(lambda n: sum(int(digit)**len(str(n)) for digit in str(n)) == n, lst))
    '''
    carm = '''
    import math
    lst = [561, 256, 8911, 1729, 2465, 147, 6601,12,31]
    def is_carmichael(n):
        for a in range(2, n):
            if math.gcd(a, n) == 1 and pow(a, n-1, n) != 1:
                return False
        return True
    carmichael_numbers = sorted(list(filter(lambda x: is_carmichael(x), lst)))
    print(f"Числа Кармайкла: {carmichael_numbers}")
    '''
    d = {'анаграммы': anagram, 'isprime': isprime, 'сумма квадратов': kv_sum, 'гласные': glasnie, 'капрекар': capr,
         'армстронг': armstrong, 'кармайкл': carm}
    print(d[key])


def leonov():
    a = '''
    lst = ['парк', 'карп', 'среда', 'антон', 'андрей', 'адрес', 'топор', 'грот', 'торг', 'ропот', 'повтор']
    a = set()
    f = lambda x, y: all((x.count(i) == y.count(i) and len(x) == len(y)) for i in x)
    for i in range(0, len(lst) - 1):
      for j in range(i+1, len(lst)):
        if f(lst[i],lst[j]):
          a.add(lst[i])
          a.add(lst[j])
    print(a)
    print(sorted(lst, key = lambda x: ((type(x) !=  str), x)))
    isprime = lambda x: x > 0 and all(x % i for i in range(2, int(x ** 0.5) + 1))
    gl = list('ауоыиэяюёе')
    print(sorted(lst, key = lambda x : sum(x.count(i) for i in gl)))

    def is_kapr(n):
      if n == 1:
        return True
      n2 = n ** 2
      for i in range(1,len(str(n2))):
        if not(int(str(n2)[i:]))==0 and n == int(str(n2)[:i])+int(str(n2)[i:]):
          return True
      return False
    def is_fib(n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
            if n == b:
              return True
        return False
    def is_arm(n):
      s,ch = 0,n
      ns = str(n)
      while ch > 0:
        s += (ch%10)**len(ns)
        ch //= 10
      if s == n:
        return True
      return False 
    def is_carm(n):
        for a in range(2, n):
            if math.gcd(a, n) == 1 and pow(a, n-1, n) != 1:
                return False
        return True
    '''
    print(a)
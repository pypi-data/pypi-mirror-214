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
    d = {'стек': stack, 'очередь': queue, 'двусвязный список': dll, 'вставками': ins_s, 'пузырьком': b_s, 'быстрая': q_s, 'выбором': sel_s}
    print(d[key])
  
def choice2(key):
    d = {'анаграммы':anagram, 'isprime': isprime, 'сумма квадратов': kv_sum, 'гласные': glasnie, 'капрекара': capr, 'армстронга': armstrong, 'кармайкл': carm}
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
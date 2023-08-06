def choice(key):
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
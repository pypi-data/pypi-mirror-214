import pyperclip
def n0():
    s = r'''
n1 классметод список объектов
n2 декоратор
n3 декоратор с доп параметрами
n4 стек связный список
n5 стек лист
n6 стек(любая структура) с условием
n7 однонаправленный список
n8 кольцевой список
n9 двунаправленный список
n10 быстрая сортировка
n11 дерево
n12 сортировка выбором
n13 cортировка вставками
n14 сортировка слияние
n15 сортировка шелла
'''
    return pyperclip.copy(s)
def n1():
    s=r'''
__objects__=[]
def __init__(self,brand,model,year):
        self.__class__.__objects__.append(self)
@classmethod
    def get_objects(cls):
        for i in cls.__objects__:
            print(i.brand)
    '''
    return pyperclip.copy(s)
def n2():
    s=r'''
import functools
def only5(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        kwargs={k:v for k,v in kwargs.items() if v[1]>=4.5}
        #result=function(*args, **kwargs)
        #return result**2
        function(*args, **kwargs)
    return wrapper
    '''
    return pyperclip.copy(s)
def n3():
    s=r'''
import functools
def tol(dlina,fill):
    def w1(func):
        @functools.wraps(func)
        def w2(*args,**kwargs):
            res=func(*args,**kwargs)
            ma=max(len(res),dlina)
            dres={k:v for k,v in zip(range(ma),res+(ma-len(res))*[fill])}
            return dres
        return w2
    return w1
    '''
    return pyperclip.copy(s)
def n4():
    s=r'''
class Node():
    def __init__(self,data):
        self.data=data
        self.next=None
class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None
    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def top(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")
    '''
    return pyperclip.copy(s)
def n5():
    s=r'''
class Stack():
    def __init__(self):
        self.vals=[]
    def add(self,x):
        self.vals.insert(0,x)
    def is_empty(self):
        return not bool(self.vals)
    def pop(self):
        return self.vals.pop(0)
    def top(self):
        return self.vals[0]
    def __str__(self):
        return ' '.join([str(x) for x in self.vals])
    '''
    return pyperclip.copy(s)
def n6():
    s=r'''
class Node():
    def __init__(self,data):
        self.data=data
        self.next=None
class Stack:
    def __init__(self,check):
        self.check=check
        self.head = None
    def push(self, x):
        if eval(self.check):
            new_node = Node(x)
            new_node.next = self.head
            self.head = new_node
    '''
    return pyperclip.copy(s)
def n7():
    s=r'''
class Node():
    def __init__(self,obj=None,nxt=None):
        self.obj=obj
        self.nxt=nxt
    def __str__(self):
        return f'{self.obj}'

class SingleLinkedList():
    def __init__(self):
        self.head=None
        self.tail=None
    def append_r(self,obj):
        if self.head==None and self.tail==None:
            new_obj=Node(obj)
            self.head=new_obj
            self.tail=new_obj
            print(new_obj.__dict__)
        elif self.head==self.tail:
            new_obj=Node(obj)
            self.head.nxt=new_obj
            self.tail=new_obj
            print(new_obj.__dict__)
        else:
            new_obj=Node(obj)
            self.tail.nxt=new_obj
            self.tail=new_obj
            print(new_obj.__dict__)
    def append_l(self,obj):
        if self.head==None and self.tail==None:
            new_obj=Node(obj)
            self.head=new_obj
            self.tail=new_obj
            print(new_obj.__dict__)
        elif self.head==self.tail:
            new_obj=Node(obj)
            a=self.head
            self.head=new_obj
            self.head.nxt=a
            print(new_obj.__dict__)
        else:
            new_obj=Node(obj)
            a=self.head
            self.head=new_obj
            self.head.nxt=a
            print(new_obj.__dict__)
    def append_m(self,obj,start):
        if self.head!=self.tail:
            temp=self.head
            for i in range(start):
                temp=temp.nxt
            new_obj=Node(obj)
            a=temp.nxt
            temp.nxt=new_obj
            new_obj.nxt=a
        else:
            print('В связном списке меньше двух значений')
    def pop_sll(self,n):
        if n==0:
            self.head=self.head.nxt
        elif len(self)!=1:
            temp=self.head
            for i in range(n-1):
                temp=temp.nxt
            a=temp.nxt
            temp.nxt=a.nxt
            if n==len(self):
                self.tail=temp
        else:
            self.head=None
            self.tail=None
            return 'Список пуст'
    def remove_sll(self,n):
        f=0
        temp=self.head
        last=None
        while temp!=None:
            if temp.obj==n:
                if f==0:
                    self.head=self.head.nxt
                    del(temp)
                    break
                last.nxt=temp.nxt
                del(temp)
                break
            last=temp
            temp=temp.nxt
            f=1
    def __str__(self):
        if self.head==None:
            return 'Список пуст'
        else:
            temp=self.head
            while temp!=None:
                print(temp,end=' ')
                temp=temp.nxt
            return 'конец списка'
    def shw(self):
        if self.head==None:
            return 'Список пуст'
        else:
            temp=self.head
            while temp!=None:
                print(temp,end='')
                temp=temp.nxt
    def __len__(self):
        cur=self.head
        c=0
        while cur is not None:
            cur=cur.nxt
            c+=1
        return c
    '''
    return pyperclip.copy(s)
def n8():
    s=r'''
class Node():
    def __init__(self,obj=None,nxt=None):
        self.obj=obj
        self.nxt=nxt
    def __str__(self):
        return f'{self.obj}'

class CycledLinkedList():
    def __init__(self):
        self.head=None
        self.tail=None
    def append_r(self,obj):
        if self.head==None and self.tail==None:
            new_obj=Node(obj)
            self.head=new_obj
            self.tail=new_obj
            self.tail.nxt=self.head
        elif self.head==self.tail:
            new_obj=Node(obj)
            self.head.nxt=new_obj
            self.tail=new_obj
            self.tail.nxt=self.head
        else:
            new_obj=Node(obj)
            self.tail.nxt=new_obj
            self.tail=new_obj
            self.tail.nxt=self.head
    def append_l(self,obj):
        if self.head==None and self.tail==None:
            new_obj=Node(obj)
            self.head=new_obj
            self.tail=new_obj
            self.tail.nxt=self.head
        elif self.head==self.tail:
            new_obj=Node(obj)
            a=self.head
            self.head=new_obj
            self.head.nxt=a
            self.tail.nxt=self.head
        else:
            new_obj=Node(obj)
            a=self.head
            self.head=new_obj
            self.head.nxt=a
            self.tail.nxt=self.head
    def __str__(self):
        if self.head==None:
            return 'Список пуст'
        else:
            temp=self.head
            while temp!=self.tail:
                print(temp,end=' ')
                temp=temp.nxt
            print(temp,end=' ')
            return 'конец списка'
    def append_m(self,obj,start):
        temp=self.head
        for i in range(start):
            temp=temp.nxt
        new_obj=Node(obj)
        a=temp.nxt
        temp.nxt=new_obj
        new_obj.nxt=a
        if self.tail==temp:
            self.tail=new_obj
    def printt(self,t=10):
        if self.head==None:
            print('Список пуст')
        else:
            temp=self.head
            for i in range(t):
                print(temp.obj,end=' ')
                temp=temp.nxt
            print('конец вывода')
    def __len__(self):
        if self.head==None:
            return 0
        else:
            cur=self.head
            c=1
            while cur!=self.tail:
                cur=cur.nxt
                c+=1
            return c
    def pop(self,elem_ind=0):
        le=len(self)
        if le==1:
            self.head=None
            self.tail=None
        elif le==elem_ind+1:
            temp=self.head
            for i in range(elem_ind-1):
                temp=temp.nxt
            self.tail=temp
            self.tail.nxt=self.head
        elif elem_ind==0 or le%(elem_ind)==0 or (elem_ind)%le==0:
            self.head=self.head.nxt
            self.tail.nxt=self.head
        else:
            temp=self.head
            for i in range(elem_ind):
                if i==elem_ind-1:
                    break
                temp=temp.nxt
            temp.nxt=temp.nxt.nxt
    '''
    return pyperclip.copy(s)
def n9():
    s=r'''
class Node():
    def __init__(self, obj = None, nxt = None, prv = None):
        self.obj = obj
        self.nxt = nxt
        self.prv = prv
    def __str__(self):
        return f"{self.obj}"
class DoubleLinkedList():
    def __init__(self):
        self.head = None
        self.tail = None
    def append(self, obj):
        if self.head:
            if self.tail:
                a = Node(obj)
                a.prv = self.tail
                self.tail.nxt = a
                self.tail = a
            else:
                self.tail = Node(obj)
                self.head.nxt = self.tail
                self.tail.prv = self.head
        else:
            self.head = Node(obj)
    def append_l(self, obj):
        if self.head:
            if self.tail:
                a = Node(obj)
                a.nxt = self.head
                self.head.prv = a
                self.head = a
            else:
                self.tail = self.head
                self.head = Node(obj)
                self.head.nxt = self.tail
                self.tail.prv = self.head
        else:
            self.head = Node(obj)
    def append_m(self, obj, n):
        assert n < len(self), 'Слишком большое n'
        node = self.head
        for i in range(n):
            node = node.nxt 
        if n == 0:
            self.append_l(obj)
        elif n == len(self) - 1:
            self.append(obj)
        else:
            a = Node(obj)
            a.prv = node.prv
            a.nxt = node
            node.prv.nxt = a
            node.prv = a   
    def delete(self, n):
        node = self.head
        last = self.head
        assert n < len(self), 'Слишком большое n'
        for i in range(n):
            last = node
            node = node.nxt
        if node == self.head:
            self.head = node.nxt
            self.head.prv = None
            del node
        elif node == self.tail:
            last.nxt = None
            self.tail = last
            del node
        else:
            last.nxt = node.nxt
            node.nxt.prv = last
            del node   
    def __str__(self):
        res = []
        if self.head == None:
            return None
        if self.tail == None:
            return str(self.head.obj)
        node = self.head
        while node != self.tail:
            res.append(node.obj)
            node = node.nxt
        res.append(node.obj)
        return ' '.join(map(str, res))
    def __len__(self):
        res = 0
        if self.head == None:
            return 0
        if self.tail == None:
            return 1
        node = self.head
        while node != self.tail:
            res += 1
            node = node.nxt
        return res + 1
    '''
    return pyperclip.copy(s)
def n10():
    s=r'''
def swap(A, i, j):
    A[i],A[j] = A[j],A[i]
def partition(a, start, end):
    pivot = a[end]
    pIndex = start
    for i in range(start, end):
        if a[i] <= pivot:
            swap(a, i, pIndex)
            pIndex = pIndex + 1
    swap(a, end, pIndex)
    return pIndex
def quicksort(a, start, end):
    if start >= end:
        return
    pivot = partition(a, start, end)
    quicksort(a, start, pivot - 1)
    quicksort(a, pivot + 1, end)
#quicksort(a, 0, len(a) - 1)
    '''
    return pyperclip.copy(s)
def n11():
    s=r'''
class Node:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None
class Tree:
    def __init__(self):
        self.root = None
    def __find(self, node, parent, value):
        if node is None:
            return None, parent, False
        if value == node.data:
            return node, parent, True
        if value < node.data:
            if node.left:
                return self.__find(node.left, node, value)
        if value > node.data:
            if node.right:
                return self.__find(node.right, node, value)
        return node, parent, False
    def append(self, obj):
        if self.root is None:
            self.root = obj
            return obj
        s, p, fl_find = self.__find(self.root, None, obj.data)
        if not fl_find and s:
            if obj.data < s.data:
                s.left = obj
            else:
                s.right = obj
        return obj
    def show_tree(self, node):
        if node is None:
            return
        self.show_tree(node.right)
        print(node.data)
        self.show_tree(node.left)
    def show_wide_tree(self, node):
        if node is None:
            return
        v = [node]
        while v:
            vn = []
            for x in v:
                print(x.data, end=" ")
                if x.left:
                    vn += [x.left]
                if x.right:
                    vn += [x.right]
            print()
            v = vn
    def __del_leaf(self, s, p):
        if p.left == s:
            p.left = None
        elif p.right == s:
            p.right = None
    def __del_one_child(self, s, p):
        if p.left == s:
            if s.left is None:
                p.left = s.right
            elif s.right is None:
                p.left = s.left
        elif p.right == s:
            if s.left is None:
                p.right = s.right
            elif s.right is None:
                p.right = s.left
    def __find_min(self, node, parent):
        if node.left:
            return self.__find_min(node.left, node)
        return node, parent
    def del_node(self, key):
        s, p, fl_find = self.__find(self.root, None, key)
        if not fl_find:
            return None
        if s.left is None and s.right is None:
            self.__del_leaf(s, p)
        elif s.left is None or s.right is None:
            self.__del_one_child(s, p)
        else:
            sr, pr = self.__find_min(s.right, s)
            s.data = sr.data
            self.__del_one_child(sr, pr)
    '''
    return pyperclip.copy(s)
def n12():
    s=r'''
def selection_sort(a_list):
    for fill_slot in range(len(a_list) - 1, 0, -1):
        pos_of_max = 0
        for location in range(1, fill_slot + 1):
            if a_list[location] > a_list[pos_of_max]:
                pos_of_max = location
        temp = a_list[fill_slot]
        a_list[fill_slot] = a_list[pos_of_max]
        a_list[pos_of_max] = temp
    return a_list
    '''
    return pyperclip.copy(s)
def n13():
    s=r'''
def insertion_sort(a_list):
    for index in range(1, len(a_list)):
        current_value = a_list[index]
        position = index
        while position > 0 and a_list[position - 1] > current_value:
            a_list[position] = a_list[position - 1]
            position -= 1
        a_list[position] = current_value
        print(a_list)
    return a_list
    '''
    return pyperclip.copy(s)
def n14():
    s=r'''
def merge_sort(a_list):
    if len(a_list) > 1:
        mid = len(a_list) // 2
        left_half = a_list[:mid]
        right_half = a_list[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        i = 0
        j = 0
        k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                a_list[k] = left_half[i]
                i += 1
            else:
                a_list[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            a_list[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            a_list[k] = right_half[j]
            j += 1
            k += 1
    return a_list
    '''
    return pyperclip.copy(s)
def n15():
    s=r'''
def shell_sort(arr):
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr
    '''
    return pyperclip.copy(s)
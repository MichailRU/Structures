'''
Структура данных Rope представляет из себя двоичное сбалансированное дерево по неявному ключу, позволяет хранит строку и  делать
операции вставки, удаления, конкатенации (например вырезать часть строки и переставить в другое место) с логарифмической асимптотикой.

Структура реализована за счет Splay-дерева с следующими операциями:
get_min() - возвращает минимальное значение
get_max() - возвращает максимальное значение
update_count(node) - пересчет атрибута count в узле
merge_tree(tree_1, tree_2) - склейка двух деревьев, возвращает новое дерево
split_tree(node, node_in_left=True) - разделение дерева по узлу node, параметр - в какое дерево node; выход - кортеж из 2 деревьев
splay(node) - функция 'всплытия' узла node
rotate(node) - отработка zig или zag для узла node
index_node(indx) - возврат узла по индексу
print_tree() - рекурсивная отладочная печать дерева начиная с узла node - обход аналогичен in_order
'''

class Node:
    def __init__(self, data, parent=None, left=None, right=None):
        self._parent = parent
        self._left = left
        self._right = right
        self._data, self._count = data, 1 # count - число вершин поддерева с корнем в этой вершине

    def __str__(self):
        return f'{self._data}'


class Rope:
    def __init__(self, node=None):
        self._root = node

    def get_min(self):  # минимум
        if self._root:
            node = self._root
            while node._left: node = node._left
            return node

    def get_max(self):  # максимум
        if self._root:
            node = self._root
            while node._right: node = node._right
            return node

    def update_count(self, node):
        return (node._left._count if node._left else 0) + (node._right._count if node._right else 0) + 1

    def merge_tree(self, tree_1, tree_2):  # слияние 2 деревьев, результат в new_tree
        if not tree_1._root: return tree_2
        if not tree_2._root: return tree_1
        if tree_1._root._count < tree_2._root._count:
            tree_1.splay(tree_1.get_max())
            tree_1._root._right = tree_2._root
            tree_1._root._right._parent = tree_1._root
            tree_1._root._count = self.update_count(tree_1._root)
            return tree_1
        else:
            tree_2.splay(tree_2.get_min())
            tree_2._root._left = tree_1._root
            tree_2._root._left._parent = tree_2._root
            tree_2._root._count = self.update_count(tree_2._root)
            return tree_2

    def split_tree(self, node, node_in_left=True):  # разделение на 2 дерева по node, на выходе кортеж
        self.splay(node)
        tree_1, tree_2 = Rope(), Rope()
        if node_in_left:
            if node._right:
                tree_2._root = node._right
                tree_2._root._parent = None
            tree_1._root = node
            tree_1._root._right = None
            tree_1._root._count = self.update_count(tree_1._root)
        else:
            if node._left:
                tree_1._root = node._left
                tree_1._root._parent = None
            tree_2._root = node
            tree_2._root._left = None
            tree_2._root._count = self.update_count(tree_2._root)
        return tree_1, tree_2

    def rotate(self, x):
        if x._parent._left == x:
            y = x._parent
            y._left, x._right, = x._right, y
            x._parent, y._parent = y._parent, x
            if y._left: y._left._parent = y
        else:
            y = x._parent
            y._right, x._left = x._left, y
            x._parent, y._parent = y._parent, x
            if y._right: y._right._parent = y
        if not x._parent:
            self._root = x
        else:
            if x._parent._left == y: x._parent._left = x
            if x._parent._right == y: x._parent._right = x
        y._count = self.update_count(y)
        x._count = self.update_count(x)

    def splay(self, node):
        if node:
            while node._parent:
                parent = node._parent
                grandparent = node._parent._parent
                if grandparent:
                    if (grandparent._left == parent and parent._left == node) or \
                            (grandparent._right == parent and parent._right == node):
                        self.rotate(parent)
                        self.rotate(node)
                    else:
                        self.rotate(node)
                        self.rotate(node)
                else:
                    self.rotate(node)

    def index_node(self, number):
        if self._root:
            node = self._root
            leftsize = node._left._count if node._left else 0
            while number != leftsize:
                if number < leftsize:
                    node = node._left
                elif number > leftsize:
                    node = node._right
                    number -= (leftsize + 1)
                leftsize = node._left._count if node._left else 0
            return node

    def print_tree(self, node, level=0):  # печать дерева обход аналогичен in_order
        if node:
            self.print_tree(node._right, level + 1)
            print(f'{" " * 15 * level}{node._data} - {node._count}({node._left},{node._right},{node._parent})')
            self.print_tree(node._left, level + 1)

    def print_itog(self):
        node = self._root
        pre = nex = None
        while node:
            if node._right and pre == node._right:
                nex = node._parent
            elif not node._left or pre == node._left:
                yield node._data
                nex = node._right or node._parent
            else:
                nex = node._left
            pre, node = node, nex



'''
Вход: первая строка содержит исходную строку S, вторая — число запросов q. Каждая из последующих q строк задаёт запрос тройкой
чисел i, j, k и означает следующее: вырезать подстроку S[i..j] (индекс с нуля) и вставить её после k-го символа оставшейся строки
(k индексируется с единицы), при этом если k = 0, то вставить вырезанный кусок надо в начало.
Вывод: полученная (после всех q запросов) строка.

Пример ввода:	hlelowrold	2	1 1 2	6 6 7
Пример вывода:	hlelowrold → hellowrold → helloworld
'''
if __name__ == "__main__":
    my_Rope = Rope()
    for char in input():
        my_Rope = my_Rope.merge_tree(my_Rope, Rope(Node(char)))
    for _ in range(int(input())):
        i, j, k = map(int, input().split())
        n_1, n_2 = my_Rope.split_tree(my_Rope.index_node(i), node_in_left=False)
        n_2, n_3 = my_Rope.split_tree(n_2.index_node(j - i), node_in_left=True)
        my_Rope = my_Rope.merge_tree(n_1, n_3)
        if k > 0:
            n_1, n_3 = my_Rope.split_tree(my_Rope.index_node(k - 1), node_in_left=True)
        else:
            n_1, n_3 = Rope(), my_Rope
        my_Rope = my_Rope.merge_tree(n_1, my_Rope.merge_tree(n_2, n_3))
    print(''.join(my_Rope.print_itog()))

'''
Двусвязный список LinkedList, состояший из объектов ObjList, которые связаны с соседними через свойства _next и _prev
В классе LinkedList реализованы методы:
add_obj(obj) - добавление нового объекта obj класса ObjList в конец связного списка;
remove_obj() - удаление последнего объекта из связного списка;
remove_obj(indx) - если задан indx - удаление объекта класса ObjList из связного списка по его порядковому номеру (индексу);
get_data() - получение списка из строк локального свойства _data всех объектов связного списка;

С объектами класса LinkedList выполняются команды:
- получение общего числа объектов в связном списке (n = len(linked_lst))
- возврат значения _data объекта класса ObjList, расположенного под индексом indx в связном списке (например out = linked_lst(indx))
'''

class LinkedList:

    def __init__(self):
        self._head = None	# ссылка на первый объект связного списка
        self._tail = None	# ссылка на последний объект связного списка

    def __len__(self):
        out, tmp = 0, self._head
        while tmp:
            out += 1
            tmp = tmp._next
        return out

    def add_obj(self, obj):
        if self._head:
            self._tail._next = obj
            obj._prev = self._tail
        else:
            self._head = obj
        self._tail = obj


    def remove_obj(self, indx = None):
        if indx:
            if 0 <= indx < len(self):
                obj = self.find_obj(indx)
                if obj._prev: obj._prev._next = obj._next
                if obj._next: obj._next._prev = obj._prev
                if self._head == obj: self._head = obj._next
                if self._tail == obj: self._tail = obj._prev
        else:
            if self._head == self._tail:
                self._head, self._tail = None, None
            else:
                self._tail._prev._next = None
                self._tail = self._tail._prev

    def get_data(self):
        lst, cur_obj = [], self._head
        while cur_obj:
            lst.append(cur_obj._data)
            cur_obj = cur_obj._next
        return lst

    def __call__(self, indx):
        return self.find_obj(indx)._data if 0 <= indx < len(self) else ''

    def find_obj(self, indx):
        tmp = self._head
        while indx > 0:
            indx -= 1
            tmp = tmp._next
        return tmp


class ObjList:
    def __init__(self, data):
        self._prev = None	# ссылка на предыдущий объект связного списка
        self._next = None	# ссылка на следующий объект связного списка
        self._data = data	# строка с данными



if __name__ == "__main__":
    print('тест работы')
    ls = LinkedList()
    ls.add_obj(ObjList(1))
    assert ls.get_data() == [1], "метод get_data вернул неверные данные"
    h, n = ls._head, 0
    while h: n += 1; h = h._next
    assert n == 1, "неверное число объектов в списке: возможно некорректно работает метод add_obj"
    ls.remove_obj()
    assert ls.get_data() == [], "метод get_data вернул неверные данные для пустого списка, неверно работает метод remove_obj"
    ls.add_obj(ObjList("данные 1"))
    ls.add_obj(ObjList("данные 2"))
    ls.add_obj(ObjList("данные 3"))
    ls.add_obj(ObjList("данные 34"))
    assert ls.get_data() == ['данные 1', 'данные 2', 'данные 3', 'данные 34'], "метод get_data вернул неверные данные"
    h, n = ls._head, 0
    while h: n += 1; h = h._next
    assert n == 4, "неверное число объектов в списке: возможно некорректно работает метод add_obj"
    h, n = ls._head, 0
    while h: h = h._next; n += 1
    assert n == 4, "неверное число объектов в списке: возможно некорректные значения в атрибутах _next"
    h, n = ls._tail, 0
    while h: n += 1; h = h._prev
    assert n == 4, "неверное число объектов в списке: возможно некорректно работает метод add_obj"
    h, n = ls._tail, 0
    while h: h = h._prev; n += 1
    assert n == 4, "неверное число объектов в списке: возможно некорректные значения в атрибутах _prev"
    ls.remove_obj(2)
    assert len(ls) == 3, "функция len вернула неверное число объектов в списке, возможно, неверно работает метод remove_obj()"
    ls.add_obj(ObjList("Python"))
    assert ls(3) == "Python", "неверное значение атрибута _data, взятое по индексу"
    assert len(ls) == 4, "функция len вернула неверное число объектов в списке"
    assert ls(1) == "данные 2", "неверное значение атрибута _data, взятое по индексу"

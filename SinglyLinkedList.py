'''
Односвязный список Stack, состояший из объектов StackObj
В классе Stack реализованы методы:
push(obj) - добавления нового объекта obj в конец списка;
pop() - извлечение последнего объекта с его удалением;
push_front(obj) - добавления нового объекта obj в начало списка;
get_data() - получение списка из объектов односвязного списка (список из строк локального атрибута _data).

С объектами класса Stack выполняются команды:
- получение общего числа объектов (n = len(st))
- перебор объектов с начала и до конца (например for obj in st: print(obj._data))
- получение данных из объекта по индексу (например data = st[indx])
- замена прежних данных на новые по порядковому индексу (indx) (например st[indx] = value)
- добавление нового объекта класса StackObj в конец односвязного списка (например st = st + obj или st += obj);
- добавление нескольких объектов в конец списка (например st = st * ['data_1', ..., 'data_N'] или st *= ['data_1', ..., 'data_N']).
'''

class Stack:
    def __init__(self):
        self._top = None

    def _check_indx(self, indx):
        if type(indx) != int or (not -len(self) <= indx < len(self)):
            raise IndexError('неверный индекс')
        indx = (len(self) + indx) if indx < 0 else indx
        obj = self._top
        for x in range(indx):
            obj = obj._next
        return obj

    def __iter__(self):
        obj = self._top
        while obj:
            yield obj
            obj = obj._next

    def __len__(self):
        '''
        obj, out = self._top, 0
        while obj:
            obj, out = obj._next, out + 1
        return out
        '''
        return sum(1 for _ in self)

    def __getitem__(self, indx):
        return self._check_indx(indx)._data

    def __setitem__(self, indx, item):
        self._check_indx(indx)._data = item

    def __add__(self, obj):
        self.push(obj)
        return self

    def __mul__(self, obj):
        if type(obj) == list:
            for x in obj: self.push(StackObj(x))
        return self

    def push(self, obj):
        if self._top:
            self._check_indx(-1)._next = obj
        else:
            self._top = obj

    def pop(self):
        if self._top and self._top._next:
            obj = self._check_indx(-2)
            out = obj._next
            obj._next = None
        else:
            out = self._top
            self._top = None
        return out

    def push_front(self, obj):
        obj._next = self._top
        self._top = obj

    def get_data(self):
        return [x._data for x in self]


class StackObj:
    def __init__(self, data):
        self._data = data	# ссылка на данные объекта списка
        self._next = None	# ссылка на следующий объект списка или None



if __name__ == "__main__":
    print('тест работы')
    st = Stack()
    st.push(StackObj("1"))
    st.push_front(StackObj("2"))
    assert len(st) == 2, "неверный расчет длины объекта"
    assert st[0] == "2" and st[1] == "1", "неверные значения данных из объекта, при обращении по индексу"
    st[0] = "0"
    assert st[0] == "0", "неверное значение из объекта - некорректно работает присваивание нового значения объекту"
    st.push(StackObj("3"))
    assert st.pop()._data == "3", "неверно отработало удаление объекта"
    assert len(st) == 2, "неверный расчет длины объекта"
    for obj in st:
        assert isinstance(obj, StackObj), "при переборе через цикл должны возвращаться объекты класса StackObj"
    try:
        a = st[3]
    except IndexError:
        assert True
    else:
        assert False, "не сгенерировалось исключение IndexError"
    st = st + StackObj("2")
    st = st + StackObj("3")
    obj = StackObj("4")
    st += obj
    st = st * ['data_1', 'data_2']
    st *= ['data_3', 'data_4']
    d = ["0", "1", "2", "3", "4", 'data_1', 'data_2', 'data_3', 'data_4']
    h, i = st._top, 0
    while h:
        assert h._data == d[i], "неверное значение атрибута _data, возможно, некорректно работают операторы + и *"
        h = h._next
        i += 1
    assert i == len(d), "неверное число объектов"
    res = st.get_data()
    assert res == d, f"метод get_data вернул неверные данные: {res}"

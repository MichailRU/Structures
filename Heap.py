'''
  Очередь с приоритетом (мин- или иах-куча).
  Двоичная куча - двоичное дерево (у каждой вершины не более 2 детей), реализовано как полностью заполненное двоичное дерево, т.е.
все уровни полностью заполнены кроме, возможно, последнего, который заполнен слева направо.
  Основное свойство мин- (макс-) кучи: значение в каждой вершине меньше или равно (больше или равно для макс-) значений в ее сыновьях,
кроме того минимальное значение хранится в корне (максимальное значение - для макс-кучи).

Операции:
  get() - возвращает элемент с максимальным (для макс-кучи) или минимальным приоритетом (для мин-кучи) [реализация: значение корня]
  insert(P) - добавить новый элемент с приоритетом P [реализация: подвесить листом и просеять вверх]
  extract() - извлечь элемент с максимальным (минимальным) приоритетом [реализация: обменять корень с последним листом и просеять вниз]
  change_priority(indx, P) - изменить приоритет элемента с индексом indx на Р [реализация: изменить приоритет и просеять вверх/вниз]
  remove(indx) - удалить элемент с индексом indx [реализация: изменить приоритет для мин-кучи на минус бесконечность, а для
макс-кучи на бесконечность и просеиваем вверх, затем извлекаем значение из корня]

Пример инициализации очереди с приоритетом:
lst = Heap([(chr(key), key) for key in range(97, 123)], False)
формируется список кортежей символов латинского алфавита с их кодами; второй аргумент - True (мин-куча), False (макс-куча)
'''

class Heap:
    def __init__(self, data = None, min_heap = True):
        self._data = []
        self._length = 0
        self.min_heap = min_heap
        if data:
            for elem in list(data):
                self.insert(elem)

    @staticmethod
    def _parent(i): return (i - 1) >> 1

    @staticmethod
    def _right_child(i): return 2 * i + 2

    @staticmethod
    def _left_child(i): return 2 * i + 1

    def __str__(self):
        return ' '.join(map(str, self._data))

    def get(self):
        return self._data[0] if self._length else None

    def insert(self, elem):
        self._data.append(elem)
        self._length += 1
        self.shift_up(self._length - 1)

    def shift_up(self, child):
        parent = self._parent(child)
        if child > 0 and ((self.min_heap and self._data[parent] > self._data[child]) or \
                          (not self.min_heap and self._data[parent] < self._data[child])):
            self._data[parent], self._data[child] = self._data[child], self._data[parent]
            self.shift_up(parent)

    def extract(self):
        out = None
        if self._length == 1:
            out, self._length = self._data.pop(), 0
        if self._length > 1:
            out, self._data[0], self._length = self._data[0], self._data.pop(), self._length - 1
            self.shift_down(0)
        return out

    def shift_down(self, parent):
        _right = self._right_child(parent) if self._right_child(parent) < self._length else parent
        _left = self._left_child(parent) if self._left_child(parent) < self._length else parent
        indx = _right if (self.min_heap and self._data[_right] < self._data[_left]) or (not self.min_heap and self._data[_right] > self._data[_left]) else _left
        if parent < indx and ((self.min_heap and self._data[parent] > self._data[indx]) or \
                              (not self.min_heap and self._data[parent] < self._data[indx])):
            self._data[indx], self._data[parent] = self._data[parent], self._data[indx]
            self.shift_down(indx)

    def remove(self, indx_elem):
        self.change_priority(indx_elem, float('-inf') if self.min_heap else float('inf'))
        self.extract()

    def change_priority(self, indx_elem, value):
        if (self._data[indx_elem] > value and self.min_heap) or (self._data[indx_elem] < value and not self.min_heap):
            self._data[indx_elem] = value
            self.shift_up(indx_elem)
        else:
            self._data[indx_elem] = value
            self.shift_down(indx_elem)


if __name__ == "__main__":
    lst = Heap([(chr(key), key) for key in range(97, 123)], False)
    print(lst)

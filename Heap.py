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
        if child > 0 and ((self.min_heap and self._data[parent] > self._data[child]) or (not self.min_heap and self._data[parent] < self._data[child])):
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
        if parent < indx and ((self.min_heap and self._data[parent] > self._data[indx]) or (not self.min_heap and self._data[parent] < self._data[indx])):
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

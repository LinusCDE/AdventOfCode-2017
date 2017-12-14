def is_position(pos):
    return ((isinstance(pos, tuple) or isinstance(pos, list))
            and len(pos) == 2
            and isinstance(pos[0], int) and isinstance(pos[1], int))


class SecondDimension:

    def __init__(self, x: int, parent: 'CoordinateField'):
        self._x = x
        self._parent = parent
        self._y_values = dict()

    @property
    def x(self):
        return self._x

    def in_field(self, y):
        parent = self._parent
        return parent.infinite or (y >= parent.min_y and y <= parent.max_y)

    def get(self, y: int, default=None):
        if not isinstance(y, int):
            raise TypeError('Y-Coordinate must be an int!')
        if not self.in_field(y):
            raise KeyError('This position is outside of the coordinate field!')
        return self._y_values[y] if y in self._y_values else default

    def __getitem__(self, y: int):
        return self.get(y)

    def __setitem__(self, y: int, value):
        if not isinstance(y, int):
            raise TypeError('Y-Coordinate must be an int!')
        if not self.in_field(y):
            raise KeyError('This position is outside of the coordinate field!')
        if value is None:
            del self[y]
            return
        self._y_values[y] = value

    def __delitem__(self, y: int):
        if not isinstance(y, int):
            raise TypeError('Y-Coordinate must be an int!')
        if not self.in_field(y):
            raise KeyError('This position is outside of the coordinate field!')
        if y in self._y_values:
            del self._y_values[y]

    def __iter__(self):
        for y in self._y_values.keys():
            yield y

    def __len__(self):
        return len(self._y_values)

    def items(self):
        if not self._parent.infinite:
            for y in range(self._parent.min_y, self._parent.max_y + 1):
                yield y, self[y]
            return
        for item in self._y_values.items():
            yield item

    def values(self):
        if not self._parent.infinite:
            for y in range(self._parent.min_y, self._parent.max_y + 1):
                yield self[y]
            return
        for value in self._y_values.values():
            yield value

    def filled(self, y):
        return y in self._y_values and self._y_values is not None


class CoordinateField:

    def __init__(self, min_x: int=None, max_x: int=None,
                 min_y: int=None, max_y: int=None):
        if min_x is None and max_x is None \
         and min_y is None and max_y is None:
            self._infinite = True
        else:
            if min_x is None or max_x is None \
             or min_y is None or max_y is None:
                raise TypeError('Either set all min/max-values or none!')
            self._infinite = False
        self._min_x, self._max_x = min_x, max_x
        self._min_y, self._max_y = min_y, max_y
        self._x_layers = dict()

    @property
    def infinite(self):
        return self._infinite

    @property
    def min_x(self):
        return self._min_x

    @property
    def max_x(self):
        return self._max_x

    @property
    def min_y(self):
        return self._min_y

    @property
    def max_y(self):
        return self._max_y

    def in_field(self, pos):
        if self.infinite:
            return True
        x, y = pos
        return (x >= self.min_x and x <= self.max_x
                and y >= self.min_y and y <= self.max_y)

    def __setitem__(self, pos, value):
        if not is_position(pos):
            raise TypeError('This operation must be used with a position!')
        if not self.in_field(pos):
            raise KeyError('This position is outside of the coordinate field!')
        self[pos[0]][pos[1]] = value

    def __delitem__(self, pos):
        if not is_position(pos):
            raise TypeError('This operation must be used with a position!')
        if not self.in_field(pos):
            raise KeyError('This position is outside of the coordinate field!')
        del self[pos[0]][pos[1]]

    def __getitem__(self, key):
        if is_position(key):
            return self[key[0]][key[1]]
        if not isinstance(key, int):
            raise TypeError('Key must be either an int, tuple or list!')

        # 'key' is at this point a x-position:
        if not self.infinite and (key < self.min_x or key > self.max_x):
            raise KeyError('This position is outside of the coordinate field!')
        if key not in self._x_layers:
            self._x_layers[key] = SecondDimension(key, self)
        return self._x_layers[key]

    def __iter__(self):
        for x in self._x_layers.keys():
            yield x

    def __len__(self):
        return len(self._x_layers)

    def clean_up(self):
        to_delete = list()
        for x in self:
            if len(self[x]) == 0:
                to_delete.append(x)
        for x in to_delete:
            del self._x_layers[x]

    def clear(self):
        self._x_layers.clear()

    def coordinates(self, only_existing=True):
        if not only_existing and self.infinite:
            raise TypeError('You can\'t demand all values from this '
                            'coordinate field, since it is inifnite!')
        if not only_existing:
            for x in range(self.min_x, self.max_x + 1):
                for y in range(self.min_y, self.max_y + 1):
                    yield x, y
            return
        for x, x_layer in self._x_layers.items():
            for y in x_layer:
                yield x, y

    def values(self, only_existing=True):
        if not only_existing:
            for _, _, value in self.items(only_existing=False):
                yield value
            return
        for x_layer in self._x_layers.values():
            for value in x_layer.values():
                yield value

    def items(self, only_existing=True):
        if not only_existing:
            for x, y in self.coordinates(only_existing=False):
                value = self[x][y] if self.filled((x, y)) else None
                yield x, y, value
            return
        for x, x_layer in self._x_layers.items():
            for y, value in x_layer.items():
                yield x, y, value

    def adjectents(self, pos, radius: int=1, diagonals: bool=True):
        if not is_position(pos):
            raise TypeError('\'center_pos\' (first argument) must be a '
                            'position!')
        source_x, source_y = pos

        for offset_x in range(-radius, radius + 1):
            for offset_y in range(-radius, radius + 1):
                if not diagonals and abs(offset_x) == abs(offset_y):
                    continue
                if offset_x == 0 and offset_y == 0:
                    continue
                adjecent = source_x + offset_x, source_y + offset_y
                if self.in_field(adjecent):
                    yield adjecent

    def filled(self, pos):
        if not is_position(pos):
            raise TypeError('The argument isn\'t a position!')
        x, y = pos
        if x in self._x_layers:
            return self[x].filled(y)

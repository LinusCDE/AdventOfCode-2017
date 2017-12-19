def is_position(pos) -> bool:
    '''Checks if 'pos' is a valid 2d-coordinate.'''
    return ((isinstance(pos, tuple) or isinstance(pos, list))
            and len(pos) == 2
            and isinstance(pos[0], int) and isinstance(pos[1], int))


def add(pos1, pos2) -> tuple:
    '''Returns addition of 'pos1' and 'pos2'.'''
    if not is_position(pos1) or not is_position(pos2):
        return None

    return pos1[0] + pos2[0], pos1[1] + pos2[1]


def direction(from_pos, to_pos) -> tuple:
    '''Returns the position that describes the way from 'from_pos' to
    'to_pos' (called a vector).'''
    if not is_position(from_pos) or not is_position(to_pos):
        return None

    return to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]


class SecondDimension:

    def __init__(self, x: int, parent: 'CoordinateField'):
        self._x = x
        self._parent = parent
        self._y_values = dict()

    def __ensure_int_and_in_field(self, y):
        if not isinstance(y, int):
            raise TypeError('Y-Coordinate must be an int!')
        if not self.in_field(y):
            raise KeyError('This position is outside of the coordinate field!')

    @property
    def x(self):
        return self._x

    def in_field(self, y) -> bool:
        '''Returns whether the y-value is in the coordinate field.
        Always returns 'True' if it is inifinite.'''
        field = self._parent
        return field.infinite or (y >= field.min_y and y <= field.max_y)

    def get(self, y: int, default=None):
        '''Allows getting a default value.'''
        self.__ensure_int_and_in_field(y)
        return self._y_values[y] if y in self._y_values else default

    def __getitem__(self, y: int):
        return self.get(y)

    def __setitem__(self, y: int, value):
        self.__ensure_int_and_in_field(y)

        if value is None:
            del self[y]  # Setting to 'None' is basically deleting
            return

        self._y_values[y] = value

    def __delitem__(self, y: int):
        self.__ensure_int_and_in_field(y)

        if y in self._y_values:  # No error will be raised if 'y' didn't exist.
            del self._y_values[y]

    def __iter__(self):
        '''Yields all existing y-coordinates.'''
        for y in self._y_values.keys():
            yield y

    def __len__(self):
        return len(self._y_values)

    def items(self):
        '''Yields all existing y-coordinates with their values.'''
        if not self._parent.infinite:
            for y in range(self._parent.min_y, self._parent.max_y + 1):
                yield y, self[y]
            return
        for item in self._y_values.items():
            yield item

    def values(self):
        '''Yields all existing values without their coordinate.'''
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

        self.set_size(min_x, max_x, min_y, max_y)
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

    def set_size(self, min_x: int=None, max_x: int=None,
                 min_y: int=None, max_y: int=None):
        '''Adds max- and minimum values to the coordinate field that can't
        be accessd.

        When set, only positions that are within or excactly at a range are
        allowed.
        If no arguments are supplied the coordinate field is infinite.

        Warning: The limits only apply for later use. There may still be
        values outside of this border.
        '''
        if min_x is None and max_x is None \
           and min_y is None and max_y is None:
            self._infinite = True
        else:
            if min_x is None or max_x is None \
               or min_y is None or max_y is None:
                raise TypeError('Either set all min/max-values or all to none!')
            self._infinite = False

        self._min_x, self._max_x = min_x, max_x
        self._min_y, self._max_y = min_y, max_y

    def in_field(self, pos) -> bool:
        '''Checks whether a position is in the coordinate field.
        If the coordinate field is infinite, it'll always be True.
        '''
        if self.infinite:
            return True
        x, y = pos
        return (x >= self.min_x and x <= self.max_x
                and y >= self.min_y and y <= self.max_y)

    def _ensure_position_syntax(self, pos):
        if not is_position(pos):
            raise TypeError('A position (tuple with 2 ints) was expected!')

    def _ensure_position_syntax_and_in_field(self, pos):
        self._ensure_position_syntax(pos)
        if not self.in_field(pos):
            raise KeyError('This position is outside of the coordinate field!')

    def __setitem__(self, pos, value):
        self._ensure_position_syntax_and_in_field(pos)
        self[pos[0]][pos[1]] = value

    def __delitem__(self, pos):
        self._ensure_position_syntax_and_in_field(pos)
        del self[pos[0]][pos[1]]

    def __getitem__(self, key):
        if is_position(key):
            return self[key[0]][key[1]]  # Changes self[x, y] to self[x][y]

        if not isinstance(key, int):
            raise TypeError('Int or position (tuple with 2 params) expected!')

        # 'key' is at this point the x-position:
        if not self.infinite and (key < self.min_x or key > self.max_x):
            raise KeyError('This position is outside of the coordinate field!')

        # Insert row if not existing.
        if key not in self._x_layers:
            self._x_layers[key] = SecondDimension(key, self)
        return self._x_layers[key]

    def __iter__(self):
        '''Yields all x-values that contains possible filled positions.
        To prevent empty x-values clean_up() before iterating.
        '''
        for x in self._x_layers.keys():
            yield x

    def __len__(self):
        return len(self._x_layers)

    def clean_up(self):
        '''Removes empty x-layers. Invoke manually for performance gain
        when deleting a lot of coordinates.
        '''
        to_delete = list()

        for x in self:
            if len(self[x]) == 0:
                # If deleted here, the iteration would break:
                to_delete.append(x)

        # Delete after savly iterating though:
        for x in to_delete:
            del self._x_layers[x]

    def clear(self):
        '''Removes all data for positions.'''
        self._x_layers.clear()

    def coordinates(self, only_existing=True):
        '''Yields all coordinates.
        If the 'only_existing' is True only the existing positions are yielded.
        WARNING: With 'only_existing' activated, the positions are NOT
        ordered!
        Turning 'only_existing' works ONLY on non-infinite coordinate-fields!
        '''
        if not only_existing and self.infinite:
            raise TypeError('You can\'t demand all values from this '
                            'coordinate field, since it is inifnite!')
        if not only_existing:
            for x in range(self.min_x, self.max_x + 1):
                for y in range(self.min_y, self.max_y + 1):
                    yield x, y
            return

        # Yield 'only_existing':
        for x, x_layer in self._x_layers.items():
            for y in x_layer:
                yield x, y

    def values(self, only_existing=True):
        '''Yields all values without their coordinates.
        If the 'only_existing' is True only the existing positions are yielded.
        WARNING: With 'only_existing' activated, the positions are NOT
        ordered!
        Turning 'only_existing' works ONLY on non-infinite coordinate-fields!
        '''
        if not only_existing:
            for _, _, value in self.items(only_existing=False):
                yield value
            return

        # Yield 'only_existing':
        for x_layer in self._x_layers.values():
            for value in x_layer.values():
                yield value

    def items(self, only_existing=True):
        '''Yields all coordinates and their values.
        If the 'only_existing' is True only the existing positions are yielded.
        WARNING: With 'only_existing' activated, the positions are NOT
        ordered!
        Turning 'only_existing' works ONLY on non-infinite coordinate-fields!
        '''
        if not only_existing:
            for x, y in self.coordinates(only_existing=False):
                value = self[x][y] if self.filled((x, y)) else None
                yield x, y, value
            return

        # Yield 'only_existing':
        for x, x_layer in self._x_layers.items():
            for y, value in x_layer.items():
                yield x, y, value

    def adjectents(self, pos, radius: int=1, diagonals: bool=True):
        '''Yields all surrounding coordinates of the given 'pos'.
        The default 'radius' is 1, which are the direct neighbours
        surrounding 'pos'.
        '''
        self._ensure_position_syntax_and_in_field(pos)
        source_x, source_y = pos

        for offset_x in range(-radius, radius + 1):
            for offset_y in range(-radius, radius + 1):

                # Check against diagonals if forbidden:
                if not diagonals and abs(offset_x) == abs(offset_y):
                    continue

                # Check against original postion:
                if offset_x == 0 and offset_y == 0:
                    continue

                adjecent = source_x + offset_x, source_y + offset_y
                if self.in_field(adjecent):
                    yield adjecent

    def filled(self, pos) -> bool:
        '''Checks if the position has a value other than 'None'.
        It also prevents the creation of the coordinate if it doesn't
        exist.
        '''
        self._ensure_position_syntax(pos)

        x, y = pos  # Unpack x- and y-coordinates from 'pos'
        if x in self._x_layers:
            return self[x].filled(y)

    def copy(self):
        '''Returns a copy of this coordinate field.'''
        copy = CoordinateField(self.min_x, self.max_x, self.min_y, self.max_y)
        for x, y, value in self.items():
            copy[x][y] = value
        return copy

    def get(self, pos, default=None):
        '''Gets value for position. If not filled, 'default' will be returned.
        Prevents the creation of more entries, if not found.
        '''
        self._ensure_position_syntax(pos)
        x, y = pos

        if x not in self._x_layers:
            return default
        return self[x].get(y, default=default)

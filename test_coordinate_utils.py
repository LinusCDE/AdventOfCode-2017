from unittest import TestCase
from coordinate_utils import CoordinateField, SecondDimension


class DummyType:
    '''For testing purposes.'''


class TestValues(TestCase):

    NO_INT_EXAMPLES = (2, 'abc', False, [0, 1, 2], (2, 'a'), DummyType())

    def test_valid_value_access(self):
        # Setting and getting different values, working of reset() and
        # default None type
        field = CoordinateField()

        # Set and check different values values:
        for test_value in self.NO_INT_EXAMPLES:
            field.clear()  # Delete all existing values

            field[0][0] = test_value
            field[1, 1] = test_value
            field[[-1, -1]] = test_value

            self.assertEqual(field[0, 0], test_value)
            self.assertEqual(field[[1, 1]], test_value)
            self.assertEqual(field[-1][-1], test_value)

        field.clear()
        # Should return None if no value was set:
        self.assertEqual(field[0, 0], None)

        # Should return a SecondDimension when requesting only one axis
        self.assertIsInstance(field[0], SecondDimension)

    def test_invalid_value_access(self):
        field = CoordinateField(0, 100, 0, 100)  # (Includes borders, too)

        # Try to get coordinates outside the border:
        self.assertRaises(KeyError, field.__getitem__, [50, 101])
        self.assertRaises(KeyError, field.__getitem__, [-1, 50])

        # Requesting wrong types for coordinates
        for wrong in ('abc', True, b'abc', list(), set(), dict(), 0.1):
            try:
                self.assertRaises(TypeError, field.__getitem__, [wrong, 1])
                self.assertRaises(TypeError, field.__getitem__, [1, wrong])
                self.assertRaises(TypeError, field.__getitem__, [wrong, wrong])
                self.assertRaises(TypeError, field.__getitem__, wrong)
            except AssertionError as error:
                print('Failed with type: %s' % type(wrong).__name__)
                raise error

    def test_adjecents(self):
        field = CoordinateField()

        expected = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),  # Own position is not yielded
            (1, -1),  (1, 0),  (1, 1)
        ]

        for pos_res, pos_expected in zip(field.adjectents((0, 0)), expected):
            self.assertEqual(pos_res, pos_expected)

    def test_adjecents_without_diagonals(self):
        field = CoordinateField()

        expected = [
            (-1, 0),
            (0, -1), (0, 1),  # Own position is not yielded
            (1, 0)
        ]

        for pos_res, pos_expected in zip(field.adjectents((0, 0), False),
                                         expected):
            self.assertEqual(pos_res, pos_expected)

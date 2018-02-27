import unittest
from generate import (
    cell,
    spanning_cell,
    row,
    grid
)


class TestCell(unittest.TestCase):
    def test_init_with_default_values(self):
        c = cell()
        self.assertEqual(c['colspan'], 1)
        self.assertEqual(c['rowspan'], 1)
        self.assertEqual(c['color'], 'white')


class TestRow(unittest.TestCase):
    def test_returns_list_with_given_number_of_cells(self):
        self.assertEqual(row(4), [cell(), cell(), cell(), cell()])

    def test_returns_an_empty_row(self):
        self.assertEqual(row(0), [])


class TestGrid(unittest.TestCase):
    def test_init_saves_the_passed_width_and_height(self):
        g = grid(11, 10)
        self.assertEqual(g['width'], 10)
        self.assertEqual(g['height'], 11)

    def test_init_creates_height_of_rows_with_width_of_cells(self):
        g = grid(2, 3)

        self.assertEqual(g['rows'], [
            [cell(), cell(), cell()],
            [cell(), cell(), cell()]
        ])


class TestSpanningCell(unittest.TestCase):
    def test_assigns_the_colspan_rowspan_keeping_the_color_white(self):
        c = spanning_cell(4, 5)
        self.assertEqual(c['rowspan'], 4)
        self.assertEqual(c['colspan'], 5)
        self.assertEqual(c['color'], 'white')


if __name__ == '__main__':
    unittest.main()

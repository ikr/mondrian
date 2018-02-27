import unittest

from generate import (
    cell,
    spanning_cell,
    row,
    grid,
    span_top_left
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


class TestSpanTopLeft(unittest.TestCase):
    def test_spanning_to_2_columns_removes_1_cell_from_top_row(self):
        g = grid(2, 3)
        span_top_left(g, 1, 2)
        self.assertEqual(g['rows'][0], [spanning_cell(1, 2), cell()])
        self.assertEqual(g['rows'][1], [cell(), cell(), cell()])

    def test_spanning_to_too_many_columns_results_in_1_cell_with_max_colspan(self):
        g = grid(2, 3)
        span_top_left(g, 1, 200)
        self.assertEqual(g['rows'][0], [spanning_cell(1, 3)])

    def test_spanning_to_2_rows_removes_1_cell_from_2nd_row(self):
        g = grid(3, 2)
        span_top_left(g, 2, 1)
        self.assertEqual(g['rows'][0], [spanning_cell(2, 1), cell()])
        self.assertEqual(g['rows'][1], [cell()])
        self.assertEqual(g['rows'][2], [cell(), cell()])

    def test_removes_2_by_2_square_from_top_left(self):
        g = grid(3, 3)
        span_top_left(g, 2, 2)
        self.assertEqual(g['rows'][0], [spanning_cell(2, 2), cell()])
        self.assertEqual(g['rows'][1], [cell()])
        self.assertEqual(g['rows'][2], [cell(), cell(), cell()])

    def test_removing_huge_square_spans_the_whole_grid(self):
        g = grid(2, 2)
        span_top_left(g, 222, 222)
        self.assertEqual(g['rows'][0], [spanning_cell(2, 2)])
        self.assertEqual(g['rows'][1], [])

    def test_degenerate_case_of_an_empty_grid(self):
        g = grid(0, 0)
        span_top_left(g, 222, 222)
        self.assertEqual(g['rows'], [])

    def test_degenerate_case_of_1_by_1_grid(self):
        g = grid(1, 1)
        span_top_left(g, 222, 222)
        self.assertEqual(g['rows'], [[cell()]])



if __name__ == '__main__':
    unittest.main()

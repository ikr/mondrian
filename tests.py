import unittest

from generate import (
    cell,
    spanning_cell,
    row,
    grid,
    span_top_left,
    split_vertically,
    split_horizontally,
    join_vertically,
    join_horizontally,
    html_td,
    html_tr,
    html_table,
    html
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
        g = span_top_left(grid(2, 3), 1, 2)
        self.assertEqual(g['rows'][0], [spanning_cell(1, 2), cell()])
        self.assertEqual(g['rows'][1], [cell(), cell(), cell()])

    def test_spanning_to_too_many_columns_results_in_1_cell_with_max_colspan(self):
        g = span_top_left(grid(2, 3), 1, 200)
        self.assertEqual(g['rows'][0], [spanning_cell(1, 3)])

    def test_spanning_to_2_rows_removes_1_cell_from_2nd_row(self):
        g = span_top_left(grid(3, 2), 2, 1)
        self.assertEqual(g['rows'][0], [spanning_cell(2, 1), cell()])
        self.assertEqual(g['rows'][1], [cell()])
        self.assertEqual(g['rows'][2], [cell(), cell()])

    def test_removes_2_by_2_square_from_top_left(self):
        g = span_top_left(grid(3, 3), 2, 2)
        self.assertEqual(g['rows'][0], [spanning_cell(2, 2), cell()])
        self.assertEqual(g['rows'][1], [cell()])
        self.assertEqual(g['rows'][2], [cell(), cell(), cell()])

    def test_removes_2_by_3_square_from_top_left(self):
        g = span_top_left(grid(5, 5), 2, 3)
        self.assertEqual(g['rows'][0], [spanning_cell(2, 3), cell(), cell()])
        self.assertEqual(g['rows'][1], [cell(), cell()])
        self.assertEqual(g['rows'][2], [cell(), cell(), cell(), cell(), cell()])
        self.assertEqual(g['rows'][3], [cell(), cell(), cell(), cell(), cell()])
        self.assertEqual(g['rows'][3], [cell(), cell(), cell(), cell(), cell()])

    def test_removing_huge_square_spans_the_whole_grid(self):
        g = span_top_left(grid(2, 2), 222, 222)
        self.assertEqual(g['rows'][0], [spanning_cell(2, 2)])
        self.assertEqual(g['rows'][1], [])

    def test_degenerate_case_of_an_empty_grid(self):
        g = span_top_left(grid(0, 0), 222, 222)
        self.assertEqual(g['rows'], [])

    def test_degenerate_case_of_1_by_1_grid(self):
        g = span_top_left(grid(1, 1), 222, 222)
        self.assertEqual(g['rows'], [[cell()]])

    def test_degenerate_case_of_not_actually_spanning(self):
        g = span_top_left(grid(2, 2), 1, 1)
        self.assertEqual(g['rows'][0], [cell(), cell()])
        self.assertEqual(g['rows'][1], [cell(), cell()])


class TestSplitVertically(unittest.TestCase):
    def test_rows_split_in_the_middle(self):
        g = grid(2, 2)
        g1, g2 = split_vertically(g, 1)
        self.assertEqual(g1['rows'], [[cell(), cell()]])
        self.assertEqual(g2['rows'], [[cell(), cell()]])

    def test_rows_split_on_top(self):
        g = grid(2, 2)
        g1, g2 = split_vertically(g, 0)
        self.assertEqual(g1['rows'], [])
        self.assertEqual(g2['rows'], [[cell(), cell()], [cell(), cell()]])

    def test_rows_split_in_the_bottom(self):
        g = grid(2, 2)
        g1, g2 = split_vertically(g, 2)
        self.assertEqual(g1['rows'], [[cell(), cell()], [cell(), cell()]])
        self.assertEqual(g2['rows'], [])


class TestSplitHorizontally(unittest.TestCase):
    def test_split_after_one_column(self):
        g = grid(3, 3)
        g1, g2 = split_horizontally(g, 1)
        self.assertEqual(g1['rows'], [[cell()], [cell()], [cell()]])
        self.assertEqual(g2['rows'], [[cell(), cell()], [cell(), cell()], [cell(), cell()]])

    def test_split_on_the_left(self):
        g = grid(2, 2)
        g1, g2 = split_horizontally(g, 2)
        self.assertEqual(g1['rows'], [[cell(), cell()], [cell(), cell()]])
        self.assertEqual(g2['rows'], [])


class TestJoinVertically(unittest.TestCase):
    def test_jouns_a_split_back(self):
        g = grid(2, 2)
        g1, g2 = split_vertically(g, 1)
        self.assertEqual(join_vertically(g1, g2), g)


class TestJoinHorizontally(unittest.TestCase):
    def test_jouns_a_split_back(self):
        g = grid(2, 3)
        g1, g2 = split_horizontally(g, 1)
        self.assertEqual(join_horizontally(g1, g2), g)


class TestHtml(unittest.TestCase):
    def test_html_td(self):
        self.assertEqual(
            html_td({'rowspan': 2, 'colspan': 3, 'color': 'blue'}),
            '<td rowspan="2" colspan="3" style="background-color: blue"/>'
        )

    def test_html_tr(self):
        h = html_tr(row(3))
        self.assertIn('<tr>', h)
        self.assertIn('</tr>', h)
        self.assertIn('<td ', h)

    def test_html_table(self):
        h = html_table(grid(2, 2))
        self.assertIn('<table>', h)
        self.assertIn('</table>', h)
        self.assertIn('<tr>', h)
        self.assertIn('</tr>', h)

    def test_html(self):
        h = html(grid(1, 1))
        self.assertIn('<style>', h)
        self.assertIn('</style>', h)
        self.assertIn('<body>', h)
        self.assertIn('</body>', h)


if __name__ == '__main__':
    unittest.main()

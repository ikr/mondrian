from itertools import repeat, islice


def span_top_left(g, rowspan, colspan):
    top_row_length = len(g['rows'][0])
    to_drop = min(top_row_length - 1, colspan - 1)
    g['rows'][0] = g['rows'][0][:top_row_length - to_drop]
    g['rows'][0][0]['colspan'] = min(top_row_length, colspan)
    return g


def grid(height, width):
    return {
        'height': height,
        'width': width,
        'rows': list(map(row, repeat(width, height)))
    }


def row(width):
    return list(islice(iter(cell, None), 0, width))


def spanning_cell(rowspan, colspan):
    return {
        'rowspan': rowspan,
        'colspan': colspan,
        'color': 'white'
    }


def cell():
    return {
        'rowspan': 1,
        'colspan': 1,
        'color': 'white'
    }

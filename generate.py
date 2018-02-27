from itertools import repeat, islice


def span_top_left(g, rowspan, colspan):
    if len(g['rows']) <= 0:
        return g

    row_length = len(g['rows'][0])
    to_drop_horz = min(row_length - 1, colspan - 1)
    g['rows'][0] = g['rows'][0][:row_length - to_drop_horz]
    g['rows'][0][0]['colspan'] = min(row_length, colspan)

    g['rows'][0][0]['rowspan'] = min(len(g['rows']), rowspan)

    i = 1
    to_drop_vert = min(len(g['rows']) - 1, rowspan - 1)
    while to_drop_vert > 0:
        g['rows'][i] = g['rows'][i][:row_length - to_drop_horz - 1]
        to_drop_vert -= 1
        i += 1

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

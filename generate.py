from itertools import repeat, islice


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

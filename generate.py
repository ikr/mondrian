from itertools import repeat, islice


def grid(height, width):
    return {
        'width': width,
        'height': height,
        'rows': list(map(row, repeat(width, height)))
    }


def row(width):
    return list(islice(iter(cell, None), 0, width))


def cell():
    return {
        'colspan': 1,
        'rowspan': 1,
        'color': 'white'
    }

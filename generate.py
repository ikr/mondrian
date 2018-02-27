from itertools import repeat, islice
from random import randrange
from copy import deepcopy


def mondrianize(g):
    height = len(g['rows'])
    width = len(g['rows'][0])

    rowspan = randrange(1, height + 1)
    colspan = randrange(1, width + 1)

    gPrime = span_top_left(g, rowspan, colspan)

    if rowspan == height and colspan == width:
        return gPrime

    coinToss = randrange(0, 2)
    splitVerticallyFirst = (
        (rowspan < height and colspan < width and coinToss == 0) or
        (colspan == width)
    )

    result = {'rows': [[gPrime['rows'][0][0]]]}

    if splitVerticallyFirst:
        gTop, gBottom = split_vertically(g, rowspan)
        _, gRight = split_horizontally(gTop, colspan)

        if gRight['rows']:
            result = join_horizontally(result, mondrianize(gRight))

        if gBottom['rows']:
            result = join_vertically(result, mondrianize(gBottom))
    else:
        gLeft, gRight = split_horizontally(g, colspan)
        _, gBottom = split_vertically(gLeft, rowspan)

        if gBottom['rows']:
            result = join_vertically(result, mondrianize(gBottom))

        if gRight['rows']:
            result = join_horizontally(result, mondrianize(gRight))

    return result


def join_horizontally(leftG, rightG):
    return {
        'rows': list(
            map(lambda t: t[0] + t[1], zip(leftG['rows'], rightG['rows']))
        )
    }


def join_vertically(topG, bottomG):
    return {'rows': topG['rows'] + bottomG['rows']}


def split_horizontally(g, columnsOnLeft):
    g1 = {'rows': []}
    g2 = {'rows': []}

    for r in g['rows']:
        if r[:columnsOnLeft]:
            g1['rows'].append(r[:columnsOnLeft])

        if r[columnsOnLeft:]:
            g2['rows'].append(r[columnsOnLeft:])

    return (g1, g2)


def split_vertically(g, rowsOnTop):
    return (
        {'rows': g['rows'][:rowsOnTop]},
        {'rows': g['rows'][rowsOnTop:]}
    )


def span_top_left(g, rowspan, colspan):
    g = deepcopy(g)

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
    return {'rows': list(map(row, repeat(width, height)))}


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


''' HTML '''


def html(g):
    return '\n'.join((
        '<!DOCTYPE html>'
        '<html>',
        '<head>',
        '<style>',
        'table {',
        'width: 500px;',
        'height: 500px;',
        'table-layout: fixed;',
        'border-collapse: collapse;',
        'border-spacing: 0;',
        '}',
        'td {',
        'border: 12px solid;',
        'padding: 0px;',
        '}',
        '</style>',
        '</head>',
        '<body>',
        html_table(g),
        '</body>',
        '</html>'
    ))



def html_table(g):
    return '\n'.join((
        '<table>',
        '\n'.join(map(html_tr, g['rows'])),
        '</table>'
    ))


def html_tr(r):
    return ' '.join((
        '<tr>',
        ' '.join(map(html_td, r)),
        '</tr>'
    ))


def html_td(c):
    return '<td rowspan="{}" colspan="{}" style="background-color: {}"/>'.format(
        c['rowspan'],
        c['colspan'],
        c['color']
    )


''' IO '''


if __name__ == '__main__':
    print(html(mondrianize(grid(32, 32))))

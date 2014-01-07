import shapefile
from collections import namedtuple
import math

def distance_km(ll1,ll2):
    """ Computes distance between two longlat points """
    lon1, lat1 = tuple(ll1)
    lon2, lat2 = tuple(ll2)
    R = 6371  # km
    dLat = math.radians(lat2-lat1);
    dLon = math.radians(lon2-lon1);
    lat1 = math.radians(lat1);
    lat2 = math.radians(lat2);

    a = math.sin(dLat/2) * math.sin(dLat/2)
    a += math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def path_len_km(path):
    """ Computes length of path in km """
    start = path[0]
    summ = 0
    for end in path[1:]:
        summ += distance_km(start, end)
        start = end
    return summ


def pointify(p):
    """ Turn namedtuple with lon and lat fields into simple tuple """
    return (float(p.lon), float(p.lat),)

def longest_cycle(path):
    """find longest cycle in path"""
    last_inx = 0
    beginning = path[last_inx]
    path.append(beginning)
    cycles = []
    while True:
        try:
            next_inx = path.index(beginning, last_inx + 1)
            cycles.append((last_inx, next_inx,))
            last_inx = next_inx
        except ValueError:
            break
    if len(cycles) > 0:
        mc = max(cycles, key=lambda x:x[1]-x[0])
        path = path[mc[0]:mc[1]]
    return path

def find_continuation(line, lines, eq, try_head):
    """ Find next section of line """
    last = line[-1]
    first = line[0]
    for i in range(0, len(lines)):
        beg_ok = False
        end_ok = False
        reverse = False
        if eq(lines[i][0], last):
            reverse = False
            end_ok = True

        if eq(lines[i][-1], last):
            reverse = True
            end_ok = True

        if try_head:
            if eq(lines[i][0], first):
                beg_ok = True
                reverse = True

            if eq(lines[i][-1], first):
                beg_ok = True
                reverse = False

        if not (end_ok or beg_ok):
            continue

        orig_merge = lines.pop(i)
        merge = orig_merge[:]
        if reverse:
            merge = merge[::-1]

        if end_ok:
            merge.pop(0)  #remove first point from suffixed part
            line.extend(merge)

        if beg_ok:
            merge.pop()  # remove last point from prefixed part
            merge.extend(line)
            line = merge

        return line, lines, True
    return line, lines, False


def line_up(orig_lines, eq=lambda x, y: x == y, try_head=True):
    """Connects tails of previous line to head of next line
    Returns list of longest possible paths merged into one
    """
    lines = orig_lines[:]
    new_lines = []
    orig_line = lines.pop(0)
    line = orig_line[:]

    while True:
        line, lines, found = find_continuation(line, lines, eq, try_head)
        if not found:
            new_lines.append(line)
            if len(lines) > 0:
                orig_line = lines.pop(0)
                line = orig_line[:]
            else:
                break
    return new_lines


def save_points(name, localities):
    w = shapefile.Writer(shapefile.MULTIPOINT)
    w.field('id')
    for i, lls in enumerate(localities):
        w.point(*lls)
        w.record(str(i))
    w.save(name)


def save_polylines(name, polys):
    w = shapefile.Writer(shapefile.POLYLINE)
    for poly in polys:
        w.line([poly])
    w.field("id", 'C','3')
    for i in range(0, len(polys)):
        w.record(str(i))
    w.save(name)


def save_polygons(name, polygons, metas, writer=None):
    if writer is None:
        writer = shapefile.Writer(shapefile.POLYGON)
    for polygon in polygons:
        writer.poly([polygon])

    meta = metas[0]
    for key in meta:
        writer.field(key,'C','40')

    for meta in metas:
        vals = map(lambda x: x[0:40], meta.values())
        writer.record(*vals)

    writer.save(name)


def save_polygon(name, vertices, meta=None, writer=None):
    w = writer
    if writer is None:
        w = shapefile.Writer(shapefile.POLYGON)

    l = list(vertices)
    w.poly([l])
    if meta is not None:
        for key in meta:
            w.field(key,'C','40')
        vals = map(lambda x: x[0:40], meta.values())
        w.record(*vals)
    w.save(name)

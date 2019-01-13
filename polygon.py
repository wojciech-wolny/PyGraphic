from matplotlib import pyplot


def put_point(surface, x, y):
    if len(surface) > x >= 0 and len(surface[x]) > y >= 0:
        surface[x][y] = (1., 1., 1.)


def check_values_if_str(n, m, points):
    values = [n, m]
    for a, b in points:
        values.append(a)
        values.append(b)
    for index in range(len(values)):
        if type(values[index]) is str:
            if values[index].isdigit():
                values[index] = int(values[index])
            else:
                raise ValueError("One of parameters are str: {}".format(values[index]))


def draw_line_via_bresenham(surface, start_point, end_point):
    points = []
    temp_point = list(start_point[:])
    if temp_point[0] < end_point[0]:
        step_x = 1
        dx = end_point[0] - temp_point[0]
    else:
        step_x = -1
        dx = temp_point[0] - end_point[0]
    if temp_point[1] < end_point[1]:
        step_y = 1
        dy = end_point[1] - temp_point[1]
    else:
        step_y = -1
        dy = temp_point[1] - end_point[1]
    put_point(surface, temp_point[0], temp_point[1])
    points.append([temp_point[0], temp_point[1]])
    if dx > dy:
        d = dy * 2 - dx
        while temp_point[0] != end_point[0]:
            if d >= 0:
                temp_point[0] += step_x
                temp_point[1] += step_y
                d += (dy - dx) * 2
            else:
                d += dy * 2
                temp_point[0] += step_x
            put_point(surface, temp_point[0], temp_point[1])
            points.append([temp_point[0], temp_point[1]])
    else:
        d = dx * 2 - dy
        while temp_point[1] != end_point[1]:
            if d >= 0:
                temp_point[0] += step_x
                temp_point[1] += step_y
                d += (dx - dy) * 2
            else:
                d += dx * 2
                temp_point[1] += step_y
            put_point(surface, temp_point[0], temp_point[1])
            points.append([temp_point[0], temp_point[1]])
    return points


def filter_none(value, default):
    if value[0]:
        return value[0], value[1] or default
    if value[1]:
        return value[0] or default, value[1]


def fill_pylogon(surface, lines):
    max_y, max_x, min_y, min_x = lines[0][0] * 2
    for line in lines:
        for point in line:
            if max_y < point[0]:
                max_y = point[0]
            if min_y > point[0]:
                min_y = point[0]
            if max_x < point[1]:
                max_x = point[1]
            if min_x > point[1]:
                min_x = point[1]

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            temp_l = 0
            temp_r = 0
            temp_u = 0
            temp_d = 0
            for line in lines:
                for point in line[1:-1]:
                    temp = False
                    if y == point[0]:
                        if min_x < point[1] <= x:
                            temp_l += 1
                            temp = True
                        if x < point[1] <= max_x:
                            temp_r += 1
                            temp = True
                    if point[1] == x:
                        if min_y < point[0] <= y:
                            temp_d += 1
                            temp = True
                        if y < point[0] <= max_y:
                            temp_u += 1
                            temp = True
                    if temp:
                        break
            if (temp_l % 2 == 1 or temp_r % 2 == 1) and (temp_d % 2 == 1 or temp_u % 2 == 1):
                put_point(surface, y, x)


def get_pylogon(m, n, starting_points, fill=False):
    if fill not in [0, 1] and type(fill) != bool:
        raise ValueError("Fill must be 1, 0 or boll value")
    check_values_if_str(m, n, starting_points)
    surface = [[(0., 0., 0.) for _ in range(m)] for _ in range(n)]
    if type(fill) is int:
        fill = True if fill == 1 else False
    previous_point = starting_points[0]
    lines = []
    for next_point in starting_points[1:]:
        if fill:
             lines.append(draw_line_via_bresenham(surface, previous_point, next_point))
        else:
            draw_line_via_bresenham(surface, previous_point, next_point)
        previous_point = next_point
    lines.append(draw_line_via_bresenham(surface, starting_points[0], previous_point))
    if fill:
        fill_pylogon(surface, lines)
    return surface


if __name__ == "__main__":
    result_1 = get_pylogon(200, 200,
                         [
                             (150, 80),
                             (100, 145),
                             (50, 120),
                             (100, 55),
                             (100, 100),
                             (110, 100),
                             (110, 90),
                             (130, 90),
                             (110, 70)
                          ], True
                         )
    pyplot.imshow(result_1, origin="lowest")
    pyplot.show()

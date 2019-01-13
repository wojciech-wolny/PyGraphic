from matplotlib import pyplot


def check_values_if_lower_equel_than_0(n, m, p1, p2, p3):
    values = [n, m] + list(p1) + list(p2) + list(p3)
    for index in range(len(values)):
        if values[index] <= 0:
            raise ValueError("One of parameters aren't greater than 0: {}".format((values[index])))
    return values[0], values[1], values[2:4], values[4:6], values[6:]


def check_values_if_str(n, m, p1, p2, p3):
    values = [n, m] + list(p1) + list(p2) + list(p3)
    for index in range(len(values)):
        if type(values[index]) is str:
            if values[index].isdigit():
                values[index] = int(values[index])
            else:
                raise ValueError("One of parameters are str: {}".format(values[index]))
    return values[0], values[1], values[2:4], values[4:6], values[6:]


def put_point(surface, x, y):
    if len(surface) > x >= 0 and len(surface[x]) > y >= 0:
        surface[x][y] = (1., 1., 1.)


def fill_triangle(surface, start_point, line):
    for destination_point in line:
        draw_line_via_bresenham(surface, start_point, destination_point)


def draw_triangle(surface, triangle_points_1):
    for point in triangle_points_1:
        put_point(surface, point[0], point[1])


def triangle(n, m, P1, P2, P3, fill=1):
    if fill not in [0, 1] and type(fill) != bool:
        raise ValueError("Fill must be 1, 0 or boll value")
    check_values_if_lower_equel_than_0(n, m, P1, P2, P3)
    surface = [[(0., 0., 0.) for y in range(m)] for x in range(n)]
    if type(fill) is int:
        fill = True if fill == 1 else False
    if fill:
        fill_triangle(surface, P3, draw_line_via_bresenham(surface, P1, P2))
        fill_triangle(surface, P2, draw_line_via_bresenham(surface, P1, P3))
        fill_triangle(surface, P1, draw_line_via_bresenham(surface, P2, P3))
    else:
        draw_triangle(surface, draw_line_via_bresenham(surface, P1, P2))
        draw_triangle(surface, draw_line_via_bresenham(surface, P1, P3))
        draw_triangle(surface, draw_line_via_bresenham(surface, P2, P3))
    return surface


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


if __name__ == '__main__':
    triangle = triangle(300, 450, (250, 250), (30, 20), (50, 400), 0)
    pyplot.imshow(triangle)
    pyplot.show()

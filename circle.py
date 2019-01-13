from matplotlib import pyplot


def check_values_if_lower_equel_than_0(n, m, point, radius):
    values = [n, m, point[0], point[1], radius]
    for index in range(len(values)):
        if values[index] < 0:
            raise ValueError("One of parameters aren't greater than 0: {}".format((values[index])))


def check_values_if_str(n, m, point, radius):
    values = [n, m, point[0], point[1], radius]
    for index in range(len(values)):
        if type(values[index]) is str:
            if values[index].isdigit():
                values[index] = int(values[index])
            else:
                raise ValueError("One of parameters are str: {}".format(values[index]))
    return values[0], values[1], (values[2], values[3]), values[4]


def draw_circle(surface, point, radius):
    if radius <= 0:
        return
    x_value = radius - 1
    y_value = 0
    dx = 0.1
    dy = 0.1
    err = dx - (radius << 1)
    while x_value >= y_value:
        draw_octens(surface, point, x_value, y_value)
        if err <= 0:
            y_value += 1
            err += dy
            dy += 2
        elif err > 0:
            x_value -= 1
            dx += 2
            err += (-radius << 1) + dx


def draw_octens(surface, point, x_value, y_value):
    put_point(surface, point[0] + x_value, point[1] + y_value)
    put_point(surface, point[0] + y_value, point[1] + x_value)
    put_point(surface, point[0] - y_value, point[1] + x_value)
    put_point(surface, point[0] - x_value, point[1] + y_value)
    put_point(surface, point[0] - x_value, point[1] - y_value)
    put_point(surface, point[0] - y_value, point[1] - x_value)
    put_point(surface, point[0] + y_value, point[1] - x_value)
    put_point(surface, point[0] + x_value, point[1] - y_value)


def put_point(surface, x, y):
    if len(surface) > x >= 0 and len(surface[x]) > y >= 0:
        surface[x][y] = (0.9, 0.9, 0.9)


def circle(n, m, O, radius, fill=1):
    if fill not in [0, 1] and type(fill) != bool:
        raise ValueError("Fill must be 1, 0 or boll value")
    if type(fill):
        fill = True if fill == 1 else False
    n, m, O, radius = check_values_if_str(n, m, O, radius)
    check_values_if_lower_equel_than_0(n, m, O, radius)
    surface = [[(0., 0., 0.) for y in range(m)] for x in range(n)]
    if fill:
        for i in range(radius):
            draw_circle(surface, O, i)
    else:
        draw_circle(surface, O, radius+1)
        draw_circle(surface, O, radius)
        draw_circle(surface, O, radius-1)
    return surface


if __name__ == '__main__':
    circle = circle(1000, 1000, [250, 250], 100, 1)
    pyplot.imshow(circle, interpolation='nearest')
    pyplot.show()

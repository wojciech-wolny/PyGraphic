from matplotlib import pyplot


def draw_line_via_bresenham(surface, start_point, end_point):
    temp_point = start_point[:]
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
    surface[temp_point[0]][temp_point[1]] = (0.9, 0.9, 0.9)
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
            if temp_point[0] < len(surface) and temp_point[1] < len(surface[temp_point[0]]):
                surface[temp_point[0]][temp_point[1]] = (0.9, 0.9, 0.9)
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
            if temp_point[0] < len(surface) and temp_point[1] < len(surface[temp_point[0]]):
                surface[temp_point[0]][temp_point[1]] = (0.9, 0.9, 0.9)


def get_line(n, m, start_point, end_point, size):
    surface = [[(0, 0, 0) for y in range(m)] for x in range(n)]
    if size <= 0:
        raise ValueError("Size must be greater than 0")
    draw_line_via_bresenham(surface, start_point, end_point)
    return surface


if __name__ == '__main__':
    start_point = [99, 450]
    end_point = [299, 100]
    line = get_line(500, 600, start_point, end_point, 6)
    pyplot.imshow(line, interpolation='nearest')
    pyplot.show()

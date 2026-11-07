# Параболическая интерполяция по трём точкам: y = a*x^2 + b*x + c
# Метод из учебника Самарского и Гулина (гл. 3, § 1): подставляем три точки
# в уравнение параболы и решаем систему из трёх уравнений методом Гаусса.
#
# Файл с данными (строки с # игнорируются):
#   строка 1: x1 x2 x3     - три разных узла
#   строка 2: y1 y2 y3     - значения в узлах
#   строка 3: точки, в которых нужно найти значение (можно несколько)
#
# Запуск:  python parabolic_interp.py input_parabolic.txt

import sys


def read_input(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            tokens = line.split("#")[0].replace(",", ".").split()
            if tokens:
                rows.append([float(t) for t in tokens])
    xs, ys = rows[0], rows[1]
    points = [v for row in rows[2:] for v in row]
    return xs, ys, points


def solve(xs, ys):
    """Решает систему a*x^2 + b*x + c = y для трёх точек методом Гаусса."""
    m = [[x * x, x, 1.0, y] for x, y in zip(xs, ys)]
    for i in range(3):
        p = max(range(i, 3), key=lambda r: abs(m[r][i]))   # выбор главного элемента
        m[i], m[p] = m[p], m[i]
        for r in range(i + 1, 3):
            k = m[r][i] / m[i][i]
            m[r] = [a - k * b for a, b in zip(m[r], m[i])]
    a = b = c = 0.0
    c = m[2][3] / m[2][2]
    b = (m[1][3] - m[1][2] * c) / m[1][1]
    a = (m[0][3] - m[0][1] * b - m[0][2] * c) / m[0][0]
    return a, b, c


def draw(xs, ys, points, a, b, c, filename):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("График не построен: установите matplotlib (pip install matplotlib).")
        return
    all_x = xs + points
    lo, hi = min(all_x), max(all_x)
    pad = (hi - lo) * 0.25 or 1.0
    grid = [lo - pad + (hi - lo + 2 * pad) * i / 300 for i in range(301)]
    plt.plot(grid, [a * x * x + b * x + c for x in grid], label="парабола")
    plt.scatter(xs, ys, color="red", label="заданные точки", zorder=3)
    if points:
        plt.scatter(points, [a * x * x + b * x + c for x in points],
                    color="green", marker="D", label="найденные значения", zorder=3)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.savefig(filename, dpi=120)
    print("График сохранён:", filename)


def main():
    if len(sys.argv) < 2:
        print("Запуск: python parabolic_interp.py input_parabolic.txt")
        return
    xs, ys, points = read_input(sys.argv[1])
    if len(xs) != 3 or len(ys) != 3 or len(set(xs)) != 3:
        print("Ошибка: нужны три разных узла x и три значения y.")
        return

    a, b, c = solve(xs, ys)
    print(f"Парабола: y = {a:g}*x^2 + {b:g}*x + {c:g}")
    for x in points:
        print(f"y({x:g}) = {a * x * x + b * x + c:g}")
    draw(xs, ys, points, a, b, c, "parabola.png")


main()

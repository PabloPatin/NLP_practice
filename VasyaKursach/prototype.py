from math import sqrt


def B(dx, dy):
    return round(sqrt(dx ** 2 + dy ** 2), 2)


def Q(S1, S2, B):
    return round(0.5*((S1**2-S2**2)/B+B), 2)


if __name__ == '__main__':
    # Ввод данных
    # points = []
    # for i in range(3):
    #     points.append(list(map(float, input(f"Введите координаты точки {i + 1}: ").split())))
    # Ss = []
    # for i in range(3):
    #     points.append(float(input(f"Введите S{i + 1}: ")))

    points = [[5914.10, 5420.42], [5692.23, 5180.03], [5155.23, 5489.01]]
    Ss = [571.46, 714.48, 583.43]

    # Считаем dx и dy
    dxs = []
    x = points[0][0]
    for i in points[1:]:
        dxs.append(round(i[0] - x, 2))
        x = i[0]
    dys = []
    y = points[0][1]
    for i in points[1:]:
        dys.append(round(i[1] - y, 2))
        y = i[1]
    # print(dxs, dys)

    # Считаем расстояния между точек
    Bs = []
    Bs.append(B(dxs[0], dys[0]))
    Bs.append(B(dxs[1], dys[1]))
    # print(Bs)

    # Считаем Q
    Qs = []
    Qs.append(Q(Ss[0], Ss[1], Bs[0]))
    Qs.append(Q(Ss[1], Ss[2], Bs[1]))
    # print(Qs)

    # Считаем координаты точки P
    x1 = round(points[0][0] + 1/Bs[0] * (Qs[0] * dxs[0] + dys[0] * sqrt(Ss[0]**2-Qs[0]**2)), 2)
    y1 = round(points[0][1] + 1/Bs[0] * (Qs[0] * dys[0] - dxs[0] * sqrt(Ss[0]**2-Qs[0]**2)), 2)
    x2 = round(points[1][0] + 1/Bs[1] * (Qs[1] * dxs[1] + dys[1] * sqrt(Ss[1]**2-Qs[1]**2)), 2)
    y2 = round(points[1][1] + 1/Bs[1] * (Qs[1] * dys[1] - dxs[1] * sqrt(Ss[1]**2-Qs[1]**2)), 2)
    P1 = [x1, y1]
    P2 = [x2, y2]
    P = [round((x1+x2)/2, 2), round((y1+y2)/2, 2)]
    # print(P1, P2)
    print(f'x = {P[0]}\ny = {P[1]}')
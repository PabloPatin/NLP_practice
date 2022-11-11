from classes import *


def rec(rast: float, ugol: Angle):
    """Находит смещения по расстоянию и углу"""
    dx = rast * ugol.cos
    dy = rast * ugol.sin
    return [geodezround(dx), geodezround(dy)]


def summauglov(ugolizm: Angle, ugoldir: Angle):
    """Вычисляет последующий дирекционный угол"""
    ugoldir += ugolizm - 180
    if ugoldir > 360:
        ugoldir -= 360
    if ugoldir < 0:
        ugoldir += 360
    return ugoldir


def count_dirs(kord: list[tuple[float, float], tuple[float, float]]) -> Angle:
    """Считает опорные дирекционные углы по координатам точек"""
    dx = kord[1][0] - kord[0][0]
    dy = kord[1][1] - kord[0][1]
    s = m.sqrt(dx ** 2 + dy ** 2)
    ugol = Angle(m.degrees(m.acos(dx / s)) * 60)
    return ugol


def find_correct(st, fin, ugli):
    corr = (sum(ugli) - fin + st)
    while corr >= 180:
        corr -= 360
    return -corr


def make_correct(ugli, corr, acc=0.1):
    """Вносит поправки в измеренные углы"""
    l = len(ugli)
    d = {j: i for i, j in enumerate(ugli)}
    e = {j: i for i, j in enumerate(sorted(ugli))}
    d = {d[i]: e[i] for i in ugli}
    if corr > 0:
        while corr > 0:
            for i in range(l):
                ugli[d[i]].add_min(acc)
                corr.add_min(-acc)
                if corr <= 0:
                    break
    else:
        while corr < 0:
            for i in range(l):
                ugli[d[i]].add_min(-acc)
                corr.add_min(acc)
                if corr >= 0:
                    break
    return ugli


def find_dir(ugli: list[Angle], direct: Angle) -> list[Angle]:
    dirs = []
    for ugol in ugli:
        direct = summauglov(ugol, direct)
        dirs.append(direct)
    return dirs


def find_prirosts(rasts: list[float], dirs: list[Angle]) -> list[list[float, float]]:
    prirosts = []
    for i in range(len(rasts)):
        ugol = dirs[i + 1]
        rast = rasts[i]
        prirosts.append(rec(rast, ugol))
    return prirosts


def find_dist_corrects(st: tuple[float, float], fin: tuple[float, float], prirosts: list[list[float, float]]) -> tuple[
    float, float]:
    x1, y1 = st
    x2, y2 = fin
    dx = x2 - x1
    dy = y2 - y1
    x = sum([i[0] for i in prirosts])
    y = sum([i[1] for i in prirosts])
    dx = dx - x
    dy = dy - y
    return dx, dy


def find_negatives(prirosts: list[list[float, float]]) -> tuple[float, float]:
    xm = sum([i[0] for i in prirosts if i[0] < 0])
    ym = sum([i[1] for i in prirosts if i[1] < 0])
    return xm, ym


def find_summs(prirosts: list[list[float, float]]) -> tuple[float, float]:
    x = sum([i[0] for i in prirosts])
    y = sum([i[1] for i in prirosts])
    return x, y


def using_corrects(prirosts: list[list[float, float]], x, y, dx, dy, xm, ym) -> list[list[float, float]]:
    for i in prirosts:
        i[0] = geodezround(i[0] + dx * abs(i[0]) / (x - 2 * xm), 2)
        i[1] = geodezround(i[1] + dy * abs(i[1]) / (y - 2 * ym), 2)
    return prirosts


def find_koords(x1: tuple[float, float], y1: tuple[float, float], prirosts: list[list[float, float]]) -> list[
    tuple[float, float]]:
    koords = []
    for i in prirosts:
        x = x1 + i[0]
        y = y1 + i[1]
        koords.append((geodezround(x), geodezround(y)))
        x1, y1 = x, y
    return koords


if __name__ == '__main__':
    # Задаём входные значения
    n = 6 - 2  # Кол-во искомых пунктов

    koords = []  # Список с координатами искомых пунктов

    koords_st = [(38122.69, 28097.19), (38480.4, 28098.46)]  # Координаты начальных точек

    koords_fin = [(39205.06, 29218.88), (38115.27, 29567.99)]  # Координаты конечных точек

    ugolki = ['257 31.2', '188 11.9', '83 58.4', '180 10.4', '273 30.4', '258 39.5']  # Измеренные углы
    ugolki = [Angle(i) for i in ugolki]

    rassts = ['330.95', '431.04', '286.66', '292.87', '470.65']  # Расстояния между пунктами
    rassts = [float(i) for i in rassts]

    prirosts = []  # Приращения координат
    prirostcorrs = []

    # Считаем диррекционные углы
    ugol_dir_st = count_dirs(koords_st)
    ugol_dir_fin = count_dirs(koords_fin)
    dirugly = [ugol_dir_st]  # Список дирекционных углов

    # Считаем угловые невязки
    corrections = find_correct(ugol_dir_st, ugol_dir_fin, ugolki)

    # TODO Добавить проверку на допустимость невязок?
    # Внесение угловых поправок
    ugolki = make_correct(ugolki, corrections, 0.1)
    print(ugolki)

    # Находим дирекционные углы
    dirugly += find_dir(ugolki, ugol_dir_st)
    print(dirugly)

    # Находим приращения координат
    prirosts = find_prirosts(rassts, dirugly)
    print(prirosts)

    # Учитываем поправки
    dx, dy = find_dist_corrects(koords_st[1], koords_fin[0], prirosts)
    xm, ym = find_negatives(prirosts)
    x, y = find_summs(prirosts)
    prirosts = using_corrects(prirosts, x, y, dx, dy, xm, ym)

    # Высчитываем координаты
    x1, y1 = koords_st[1]
    koords = koords_st + find_koords(x1, y1, prirosts)[:-1] + koords_fin
    print(koords)

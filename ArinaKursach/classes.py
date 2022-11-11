import math as m
from functools import total_ordering
from collections.abc import Iterable


def geodezround(a, ndigits=2):
    a = int(a * 10 ** (1 + ndigits))
    b = a % 10
    a = a // 10
    if b == 5:
        if a % 10 % 2 == 1:
            a += 1
    elif b > 5:
        a += 1
    if ndigits <= 0:
        return int(a)
    return round(a / 10 ** ndigits, ndigits)


@total_ordering
class Angle:
    '''Поддерживает все необходимые математические операции с углами:
    1) суммирует/вычитает углы в градусной мере
    2) умножает угол на число
    3) делит угол на угол/число
    4) производит сравнение в градусах

        На вход:
    1) значение в минутах или строка вида "x y" (x градусов y минут)    ОБЯЗАТЕЛЬНО
    2) степень округления (кол-во знаков после запятой (по умолчанию 1))
    3) тип выходных данных ('str'/'min'/'deg') для print(<class Angle>)

        Имеет аттрибуты:
    .value - значение угла в минутах
    .minutes - минуты угла (без градусов)
    .degrees - целое число градусов
    .rad - мера в радианах
    .sin - синус угла
    .cos - косинус угла
    .tan - тангенс угла'''
    def __init__(self, value: int | float | str | Iterable, rounding=1, outtype='str'):
        if type(value) == str:
            v = value.split()
            degrees = int(v[0])
            minutes = float(v[1])
            self.value = degrees * 60 + minutes
        elif type(value) == Angle:
            self.value = value.value
        elif isinstance(value, Iterable) and len(value) == 2:
            self.value = value[0] * 60 + value[1]
        else:
            self.value = value
        if self.value >= 0:
            self.degrees = int(self.value // 60)
            self.minutes = geodezround(self.value % 60, rounding)
        else:
            self.degrees = abs(int(-self.value // 60))
            self.minutes = geodezround(-self.value % 60, rounding)
        self.value = geodezround(self.value, rounding)
        self.outtype = outtype
        self.rounding = rounding
        self.rad = m.radians(self.value / 60)
        self.sin = m.sin(self.rad)
        self.cos = m.cos(self.rad)
        self.tan = self.sin/self.cos

    def __recount(self):
        if self.value >= 0:
            self.degrees = int(self.value // 60)
            self.minutes = geodezround(self.value % 60, self.rounding)
        else:
            self.degrees = abs(int(-self.value // 60))
            self.minutes = geodezround(-self.value % 60, self.rounding)
        self.value = geodezround(self.value, self.rounding)
        self.rad = m.radians(self.value / 60)

    def add_min(self, minut):
        self.value += minut
        self.__recount()

    def __eq__(self, other):
        if type(other) == Angle:
            return self.value == other.value
        else:
            return self.value == other * 60

    def __gt__(self, other):
        if type(other) == Angle:
            return self.value > other.value
        else:
            return self.value > other * 60

    def __add__(self, other):
        if type(other) != Angle:
            other = Angle(other * 60, self.rounding)
        return Angle(self.value + other.value, self.rounding, self.outtype)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if type(other) != Angle:
            other = Angle(other * 60, self.rounding)
        return Angle(self.value - other.value, self.rounding, self.outtype)

    def __rsub__(self, other):
        if type(other) != Angle:
            other = Angle(other * 60, self.rounding, self.outtype)
        return Angle(other.value - self.value, self.rounding, self.outtype)

    def __mul__(self, other):
        if type(other) == Angle:
            return Angle(self.value * (other.value / 60), self.rounding, self.outtype)
        else:
            return Angle(self.value * other, self.rounding, self.outtype)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) == Angle:
            return Angle(self.value / (other.value / 60), self.rounding, self.outtype)
        else:
            return Angle(self.value / other, self.rounding, self.outtype)

    def __floordiv__(self, other):
        return Angle(self.value // other, self.rounding, self.outtype)

    def __mod__(self, other):
        if type(other) != Angle:
            other = Angle(other, self.rounding)
        return Angle(self.value % (other.value * 60), self.rounding, self.outtype)

    def __neg__(self):
        self.value = -self.value
        return self

    def __int__(self):
        return int(self.value)

    def __repr__(self):
        if self.outtype == 'str':
            if self.value >= 0:
                return f"{self.degrees}° {self.minutes}'"
            else:
                return f"-{self.degrees}° {self.minutes}'"
        elif self.outtype == 'min':
            return str(self.value)
        elif self.outtype == 'degrees':
            return str(self.value // 60)
        else:
            raise ValueError

    def __hash__(self):
        return int(self.value)

if __name__ == "__main__":
    a = Angle('257 31.29558')
    print(a)

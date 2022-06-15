class TrueTable(list):
    def __init__(self, num, funk):
        super().__init__()
        self.num = num
        for i in range(2 ** num - 1, -1, -1):
            self.append(self.__bin(i))

    def __bin(self, j):
        ret = []
        for i in range(self.num):
            if j // 2 != 0 or j % 2 != 0:
                ret.append(j % 2)
                j //= 2
            else:
                ret.append(0)
        return list(reversed(ret))

    def pr(self):
        for i in range(65, self.num+65):
            print(chr(i), end=' ')
        print('Funk')
        for i in self:
            print(*i)


if __name__ == '__main__':
    t = TrueTable(3, 'X and not Y or not Z')
    for i in t:
        A, B, C = i
        if A and not B or C:
            i.append(1)
        else:
            i.append(0)
    t.pr()
    new_text = 'Новый текст'


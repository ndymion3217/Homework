      +ㄷ+ㅇㅇ+야.ㄷ결려오ㅗㅇㅇ엉어로치ㅏㄴimport random as rd
import numpy as np


class StarSeekerCase:
    def __init__(self, fos):
        def case(n):
            l = list(range(1, n+1))
            counter = 0
            rd.shuffle(l)
            for i in l:
                counter += 1
                if i == n:
                    break
            return counter
        self.starseeker_counter = case(30)
        self.starseeker_counter = 7 if self.starseeker_counter < 7 else self.starseeker_counter
        self.starseeker_turn = self.starseeker_counter - 3 if fos == "f" else self.starseeker_counter - 4
        self.map_counter = case(30 - self.starseeker_counter + 1)
        self.monkey_counter = case(30 - self.starseeker_counter - self.map_counter) - 1
        self.fos = fos

    def get_total_turn(self):
        return self.starseeker_turn + self.map_counter + self.monkey_counter


n = int(input('몇번 시뮬레이션 할까요? : '))
fos = int(input('1.선공 2.후공 : '))
a = []
for i in range(n):
    a.append(StarSeekerCase('f')) if fos == 1 else a.append(StarSeekerCase('s'))
b = np.array([x.get_total_turn() for x in a])
print('전체 케이스의 턴의 합 : {} 턴'.format(b.sum()))
print('케이스중 원숭이를 뽑는데까지 걸린 최소의 턴 : {} 턴'.format(b.min()))
print('케이스중 원숭이를 뽑는데까지 걸린 최대의 턴 : {} 턴'.format(b.max()))
print('모든 케이스의 평균값 : {} 턴'.format(round(b.mean(), 4)))
print('모든 케이스의 표준편차 : {}'.format(round(b.std(), 4)))
print('모든 케이스의 분산 : {}'.format(round(b.var(), 4)))
c = np.bincount(b, minlength=28)
for i in range(4, 28):
    print('{} 번쨰턴에 원숭이가 들어올 확률 : {} %'.format(i, round(c[i] / n * 100, 2)))



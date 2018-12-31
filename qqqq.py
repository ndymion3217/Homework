import random as rd
n = int(input())
l = list(range(1, n+1))
counter = 0
print(l)
ori= n
while True:
    counter += 1
    n-= 1
    pop = l.pop(rd.randint(0, n))
    if pop == ori:
        break
    print(pop)
print(counter)

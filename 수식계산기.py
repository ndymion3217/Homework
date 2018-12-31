# (2 + (1 + 2)) ^ 2 - 10
def main(string):
    stuff = [x for x in string if x != ' ']
    if checker(stuff):
        pass
    else:
        return 'INCORRECT FORMAT ERROR'
    return first(stuff)


def cal(n, s, n1):
    print(n, s, n1)
    if s == '+':
        return int(n) + int(n1)
    elif s == '-':
        return int(n) - int(n1)
    elif s == '*':
        return int(n) * int(n1)
    elif s == '^':
        return int(n) ** int(n1)
    elif s == '/':
        if n1 == '0' or n1 == 0:
            print('CANNOT DIVIDE WITH 0')
        else:
            return int(n) / int(n1)


def checker(arr):
    bef = 2
    for i in arr:
        try:
            int(i)
            cur = 0
        except:
            if i == '(':
                cur = 3
            elif i == ')':
                cur = 4
            else:
                cur = 1
        if bef == 4 and cur == 3 or bef == 3 and cur == 4:
            bef = cur
        elif bef == 3 and cur == 1 or bef == 4 and cur == 0 or bef == 0 and cur == 3:
            return False
        elif bef != cur:
            bef = cur
    return True


def first(arr):
    while len(arr) > 1:
        if '(' in arr or ')' in arr:
            if arr.count('(') != arr.count(')'):
                return 'INCORRECT FORMAT ERROR'
            while arr.count('(') != 0:
                idx = arr.index('(')
                do_this_first_lol = []
                first_one = True
                while True:
                    i = arr[idx]
                    if i == '(' and first_one:
                        first_one = False
                        do_this_first_lol.append(arr.pop(idx))
                    elif i == '(':
                        while do_this_first_lol:
                            arr.insert(idx, do_this_first_lol.pop(0))
                            idx += 1
                        do_this_first_lol.append(arr.pop(idx))
                    elif i == ')' and first_one == True:
                        return 'INCORRECT FORMAT ERROR'
                    elif i == ')':
                        arr.pop(idx)
                        do_this_first_lol.pop(0)
                        arr.insert(idx, first(do_this_first_lol))
                        break
                    else:
                        do_this_first_lol.append(arr.pop(idx))
        elif '^' in arr:
            idx = arr.index('^') - 1
            arr.insert(idx, cal(arr.pop(idx), arr.pop(idx), arr.pop(idx)))
        elif '*' in arr or '/' in arr:
            idx = 0
            for i in arr:
                if i == '*' or i == '/':
                    arr.insert(idx  - 1, cal(arr.pop(idx - 1), arr.pop(idx - 1), arr.pop(idx - 1)))
                idx += 1
        else:
            arr.insert(0, cal(arr.pop(0), arr.pop(0), arr.pop(0)))
    return arr[0]


print(main(input()))
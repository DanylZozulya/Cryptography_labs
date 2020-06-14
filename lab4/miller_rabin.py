import random


def check(a: int, s: int, d: int, n: int) -> bool:
    x = pow(a, d, n)
    if x == 1:
        return True
    for i in range(s - 1):
        if x == n - 1:
            return True
        x = pow(x, 2, n)
    return x == n - 1


def miller_rabin_test(n: int, round_count: int) -> bool:
    d = n - 1
    s = 0
    while d & 1 == 0:
        d //= 2
        s += 1

    flag = True
    for i in range(round_count):
        a = random.randrange(2, n-1)
        if not check(a, s, d, n):
            flag = False
            break

    return flag


if __name__ == '__main__':
    print(miller_rabin_test(71, 12))
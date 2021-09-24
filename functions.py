import random
import math
import sys
import hashlib
sys.setrecursionlimit(1500)

# генерация большого простого числа
def randPrime(n):
    rangeStart = 10 ** (n-1)
    rangeEnd = (10 ** n) - 1
    while True:
        num = random.randint(rangeStart, rangeEnd)
        if isPrime(num):
            return num

# определение простое ли число
def isPrime(num):
    if (num < 2):
        return False
    for prime in LOW_PRIMES:
        if (num == prime):
            return True
        if (num % prime == 0):
            return False
    return MillerRabin(num)

# решето Эратосфена
def primeSieve(sieveSize):
    sieve = [True] * sieveSize
    sieve[0] = False # Ноль и единица не являются простыми числами
    sieve[1] = False
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)
    return primes

LOW_PRIMES = primeSieve(100)

# тест Миллера-Рабина
def MillerRabin(num):
    if num % 2 == 0 or num < 2:
        return False
    if num == 3:
        return True
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = power(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

# рекурентный алгоритм к КЦД
def fct(arr, b):
    if arr == []:
        return 'Null division', 0
    elif arr == [0.0]:
        return 0, b
    p = []
    q = []
    for i in range(len(arr)):
        q.append(0)
        p.append(0)
    p[0] = arr[0]
    p[1] = arr[0] * arr[1] + 1
    q[0] = 1
    q[1] = arr[1]
    for n in range(2,len(arr)):
        p[n] = arr[n] * p[n-1] + p[n-2]
        q[n] = arr[n] * q[n-1] + q[n-2]
    return p[-2], len(p)

# расширенный алгоритм Евклида
def gcdex(a, m, b = 1, d = 1):
    a //= d
    b //= d
    m //= d
    newM = m

    arr = []
    while m != 1:
        division = m // a
        arr.append(float(division))
        p = m
        m = a
        a = p - (p // a) * a

    pN_1, n = fct(arr, b)

    x0 = (((-1) ** (n - 1)) * pN_1 * b) % newM

    arrX = []
    for i in range(d):
        arrX.append(int(x0 + i * newM))
    return arrX

# нахождение рандомного числа num при условии НОД(num, b) = 1
def randGcd1(b):
    rangeStart = 2
    rangeEnd = b - 1
    while True:
        num = random.randint(rangeStart, rangeEnd)
        if math.gcd(num, b) == 1:
            return num

# быстрый поиск модуля от степени числа
def power(x, n, mod):
    if n == 0:
        return 1
    elif n % 2 == 0:
        p = power(x, n / 2, mod)
        return (p * p) % mod
    else:
        return (x * power(x, n - 1, mod)) % mod

# генерация ключей d, e и числа N
def generatePublicAndSecretKeys(size = 5):
    p, q = randPrime(size), randPrime(size)
    N = p * q
    f = (p - 1) * (q - 1)

    e = randGcd1(f)

    d = gcdex(e, f)[0]

    keys = {'d' :  d, 'e' : e, 'N' : N}

    return keys

# упрощённое хэширование текста алгоритмом SHA256 с обрезкой хэша
def hashing(M, size = 5):
    return int(hashlib.sha256(M.encode('utf-8')).hexdigest(), 16) % 10 ** (size * 2 - 2)

# создание подписи для подписанного сообщения
def signMessage(M, d, N):
    hashM = hashing(M)
    s = power(hashM, d, N)
    return s

# проверка пары сообщение + подпись по открытой паре ключей
def verifySign(signPair, keys):
    s = signPair[1]
    M = signPair[0]
    e = keys[1]
    N = keys[0]
    w = power(s, e, N)
    hashM = hashing(M)
    return w == hashM
import functions as fn

# генерирование ключей абонента А для подписи сообщения
keys = fn.generatePublicAndSecretKeys()
print('A`s keys                 :', keys)

# формирование пары открытого ключа N + e
publicPair = (keys['N'], keys['e'])

# задание сообщения М
M = """Hello"""

# формирование подписи к сообщению M
s = fn.signMessage(M, keys['d'], keys['N'])

# формирование пары сообщение + подпись
signPair = (M, s)
print('Pair (M, s) with A`s sign:', signPair)

# проверка пары 
result = fn.verifySign(signPair, publicPair)
print('\nMessage has verified with `', result, '` result')
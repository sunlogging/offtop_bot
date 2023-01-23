from concurrent.futures import ThreadPoolExecutor

def f1(n):
    # Функция для обработки асинхронного запроса
    print(f'работает функция №1 с параметров: {n}')

def f2(m):
    # Функция для обработки асинхронного запроса
    print(f'работает функция №2 с параметров: {m}')

params_1 = [1, 2, 3]
params_2 = [4, 5, 6]

with ThreadPoolExecutor() as executor:
    future_1 = executor.submit(f1, params_1)
    future_2 = executor.submit(f2, params_2)
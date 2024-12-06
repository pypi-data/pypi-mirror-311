import os
import random
import base64

def create_keys() -> list:
    """Создает список зашифрованных ключей с использованием случайных солей."""
    # Генерация 128 случайных солей
    salts = [os.urandom(16).hex() for _ in range(128)]

    # Перемешивание солей
    random.shuffle(salts)

    # Объединение солей в одну строку
    salt_str = "".join(salts)

    # Перемешивание символов в строке
    shuffled_salts = list(salt_str)
    random.shuffle(shuffled_salts)

    # Формирование списка солей по 32 символа
    salt_list = [salt_str[i:i + 32] for i in range(0, len(salt_str), 32)]

    # Перемешивание списка солей
    random.shuffle(salt_list)

    # Уменьшение списка до 2 солей
    while len(salt_list) > 2:
        salt_list = random.sample(salt_list, len(salt_list) - 2)

    # Кодирование солей в base64
    encoded_salts = [base64.b64encode(salt.encode()).decode() for salt in salt_list]

    return encoded_salts

def generate_random_key(size: int) -> str:
    """Генерирует случайный ключ заданного размера."""
    # Генерация 128 случайных солей
    salts = [os.urandom(16).hex() for _ in range(128)]

    # Объединение солей в одну строку
    salt_str = "".join(salts)

    # Перемешивание символов в строке
    shuffled_salts = list(salt_str)
    random.shuffle(shuffled_salts)

    # Формирование списка ключей заданного размера
    keys = [salt_str[i:i + size] for i in range(0, len(salt_str), size)]
    random.shuffle(keys)

    # Возвращаем случайный ключ из списка
    return random.choice(keys)


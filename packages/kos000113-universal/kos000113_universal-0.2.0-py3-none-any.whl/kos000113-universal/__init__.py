# __init__.py

# Импортируем функции из crypter
from .crypter import pad, unpad, crypt_data, decrypt_data

# Импортируем функции из database
from .database import create_db, get_data as db_get_data, execute_SQL

# Импортируем функции из generate_key
from .generate_key import create_keys, generate_random_key

# Импортируем функции из json_handler
from .json_mananger import update_data, get_data

# Импортируем функции из generate_custom_cer
from .generate_custom_cer import generate_cer_SDTP

# Создаем пространства имен для категорий
class Crypter:
    pad = pad
    unpad = unpad
    crypt_data = crypt_data
    decrypt_data = decrypt_data

class Database:
    create_db = create_db
    get_data = db_get_data
    execute_query = execute_SQL

class GenerateKey:
    create_keys = create_keys
    generate_random_key = generate_random_key

class JsonHandler:
    update_data = update_data
    get_data = get_data

class GenerateCustomCer:
    generate_cer_SDTP = generate_cer_SDTP

# Экспортируем категории
__all__ = [
    'Crypter',
    'Database',
    'GenerateKey',
    'JsonMananger',
    'GenerateCustomCer'
]

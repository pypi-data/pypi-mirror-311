import base64
import binascii
import tgcrypto

def pad(data: bytes) -> bytes:
    """Дополняет данные нулевыми байтами до кратности 16 байтам.

    Args:
        data (bytes): Данные в байтах.

    Returns:
        bytes: Данные, дополненные нулевыми байтами, чтобы размер был кратен 16 байтам.
    """
    block_size = 16
    padding_needed = block_size - (len(data) % block_size)
    if padding_needed == block_size:
        return data
    return data + (b'\x00' * padding_needed)

def unpad(data: bytes) -> bytes:
    """Удаляет нулевые байты из конца данных.

    Args:
        data (bytes): Данные в байтах.

    Returns:
        bytes: Данные без нулевых байтов в конце.
    """
    return data.rstrip(b'\x00')


def crypt_data(data: str, key: str, iv: str) -> str:
    """Шифрует данные с использованием AES в режиме IGE.

    Args:
        data (str): Данные для шифрования.
        key (str): Ключ шифрования, должен быть длиной 32 байта после декодирования.
        iv (str): Вектор инициализации, должен быть длиной 32 байта после декодирования.

    Returns:
        str: Зашифрованные данные в формате base64.

    Raises:
        ValueError: Если возникает ошибка при преобразовании данных или шифровании.
    """
    # Преобразование строк в байты
    try:
        data = data.encode()
        key = base64.b64decode(key.encode())
        iv = base64.b64decode(iv.encode())
    except (TypeError, binascii.Error, ValueError) as e:
        raise ValueError(f"Ошибка преобразования данных: {e}")

    # Дополнение данных до кратности 16 байтам
    data = pad(data)

    # Шифрование данных
    try:
        crypted_data = tgcrypto.ige256_encrypt(data, key, iv)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Ошибка шифрования: {e}")

    # Кодирование зашифрованных данных в base64
    try:
        return base64.b64encode(crypted_data).decode()
    except (binascii.Error, ValueError) as e:
        raise ValueError(f"Ошибка кодирования в base64: {e}")


def decrypt_data(data: str, key: str, iv: str) -> str:
    """Дешифрует данные, зашифрованные с использованием AES в режиме IGE.

    Args:
        data (str): Зашифрованные данные в формате base64.
        key (str): Ключ шифрования, должен быть длиной 32 байта после декодирования.
        iv (str): Вектор инициализации, должен быть длиной 32 байта после декодирования.

    Returns:
        str: Расшифрованные данные.

    Raises:
        ValueError: Если возникает ошибка при преобразовании данных или дешифровании.
    """
    # Преобразование строк в байты
    try:
        data = base64.b64decode(data.encode())
        key = base64.b64decode(key.encode())
        iv = base64.b64decode(iv.encode())
    except (TypeError, binascii.Error, ValueError) as e:
        raise ValueError(f"Ошибка преобразования данных: {e}")

    # Дешифрование данных
    try:
        decrypted_data = tgcrypto.ige256_decrypt(data, key, iv)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Ошибка дешифрования: {e}")

    # Удаление возможных нулевых байтов
    return unpad(decrypted_data).decode('utf-8')

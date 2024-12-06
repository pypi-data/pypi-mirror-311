import sqlite3
from typing import Tuple, Any

def create_db(db_name: str, SQL_request: str, params: Tuple = ()) -> bool:
    """Создание базы данных и выполнение SQL-запроса.

    Args:
        db_name (str): Имя базы данных.
        SQL_request (str): SQL-запрос для выполнения на базе данных.
        params (Tuple): Параметры для SQL-запроса. По умолчанию пустой кортеж.

    Raises:
        Exception: Если возникает ошибка при выполнении SQL-запроса.

    Returns:
        bool: True, если выполнение прошло успешно.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(SQL_request, params)  # Используем параметризованный запрос
        conn.commit()
        return True
    except sqlite3.Error as e:
        raise Exception(f"Sqlite3.Error: {e}")
    finally:
        conn.close()  # Закрываем соединение с базой данных






def get_data(db_name: str, SQL_request: str, params: Tuple[Any] = (), formatted: bool = False, method: str = 'fetchall', size: int = 1) -> str:
    """Получение данных из базы данных с использованием SQL-запроса.

    Args:
        db_name (str): Имя базы данных, к которой нужно подключиться.
        SQL_request (str): SQL-запрос для выполнения на базе данных.
        params (Tuple[Any]): Параметры для SQL-запроса. По умолчанию пустой кортеж.
        formatted (bool): Нужно ли возвращать данные в "красивом" формате. 
                          Пример: [(1,), (2,), (3,)] - без форматирования. 
                          [1, 2, 3] - с форматированием.
        method (str): Метод получения данных; может быть 'fetchone', 'fetchall' или 'fetchmany'.
        size (int): Количество записей для метода 'fetchmany'.

    Raises:
        Exception: Если возникает ошибка при выполнении SQL-запроса.
        Exception: Если указанный метод не является одним из допустимых ('fetchone', 'fetchall', 'fetchmany').
        Exception: Если данные не найдены для 'fetchone'.
        Exception: Если нет данных для 'fetchall' или 'fetchmany'.

    Returns:
        str: Данные, полученные из базы данных, в формате строки. 
             Если formatted=True, возвращает данные в "красивом" формате, 
             иначе возвращает данные в обычном виде.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(SQL_request, params)  # Используем параметризованный запрос
    except sqlite3.Error as e:
        raise Exception(f"Sqlite3.Error: {e}")

    try:
        if method == "fetchone":
            data_row = cursor.fetchone()
        elif method == "fetchall":
            data_row = cursor.fetchall()
        elif method == "fetchmany":
            data_row = cursor.fetchmany(size)
        else:
            raise Exception("Error, allowed arguments not found! Please check variable method! Allowed arguments: fetchone, fetchall, fetchmany")
    except sqlite3.Error as e:
        raise Exception(f"Sqlite3.Error: {e}")

    try:
        if method == "fetchone":
            if data_row is not None:
                if formatted:
                    return str(data_row)  # Преобразуем в строку без кортежа, если formatted = True
                else:
                    return str(data_row)  # Возвращаем как строку
            else:
                raise Exception("Error, Data not found")
        elif method == "fetchall":
            if data_row:
                if formatted:
                    # Форматируем все строки как список значений
                    return str([item for row in data_row for item in row])  # Преобразуем в плоский список
                else:
                    return str(data_row)  # Возвращаем как строку
            else:
                raise Exception("Error, No data found")
        elif method == "fetchmany":
            if data_row:
                if formatted:
                    # Форматируем выборку как список значений
                    return str([item for row in data_row for item in row])  # Преобразуем в плоский список
                else:
                    return str(data_row)  # Возвращаем как строку
            else:
                raise Exception("Error, No data found")
    finally:
        conn.close()


def execute_SQL(db_name: str, SQL_request: str, params: Tuple[Any] = ()) -> None:
    """Выполнение SQL-запроса для изменения данных в базе данных.

    Args:
        db_name (str): Имя базы данных, к которой нужно подключиться.
        SQL_request (str): SQL-запрос для выполнения на базе данных.
        params (Tuple[Any]): Параметры для SQL-запроса. По умолчанию пустой кортеж.

    Raises:
        Exception: Если возникает ошибка при выполнении SQL-запроса.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(SQL_request, params)  # Используем параметризованный запрос
        conn.commit()  # Подтверждаем изменения
    except sqlite3.Error as e:
        raise Exception(f"Sqlite3.Error: {e}")
    finally:
        conn.close()

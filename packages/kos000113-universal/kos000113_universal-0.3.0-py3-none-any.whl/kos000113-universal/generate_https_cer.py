from OpenSSL import crypto
import socket
import os

def create_https_cer(company: str, department: str, city: str, country_code: str, validity_period: int) -> None:
    """
    Создает HTTPS сертификат и соответствующие ключи.

    :param company: Название компании.
    :param department: Отдел компании.
    :param city: Город.
    :param country_code: Код страны.
    :param validity_period: Период действия сертификата в секундах.
    """

    # Получаем имя хоста
    hostname = socket.gethostname()

    # Генерируем пару ключей RSA
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    # Создаем запрос на сертификат (CSR)
    req = crypto.X509Req()
    req.get_subject().CN = hostname
    req.get_subject().O = company
    req.get_subject().OU = department
    req.get_subject().L = city
    req.get_subject().ST = city
    req.get_subject().C = country_code
    req.set_pubkey(key)
    req.sign(key, 'sha256')

    # Сохраняем закрытый ключ в файл
    with open(f"{hostname}.key", "wb") as key_file:
        key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    # Сохраняем запрос на сертификат в файл
    with open(f"{hostname}.csr", "wb") as csr_file:
        csr_file.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))

    # Создаем сам сертификат
    cert = crypto.X509()
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.gmtime_adj_notBefore(0)  # Сертификат активен немедленно
    cert.gmtime_adj_notAfter(validity_period)  # Устанавливаем время действия сертификата
    cert.sign(key, 'sha256')

    # Сохраняем сертификат в файл
    with open(f"{hostname}.crt", "wb") as cert_file:
        cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    # Удаляем файл запроса на сертификат, так как он больше не нужен
    os.remove(f"{hostname}.csr")

    print(f"Сертификат успешно создан: {hostname}.crt")
    print(f"Закрытый ключ сохранен: {hostname}.key")

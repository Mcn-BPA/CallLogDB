from datetime import datetime


def parse_datetime(date_str: str) -> datetime | None:
    """
    Преобразует строку в datetime объект, если строка соответствует формату "%Y-%m-%d %H:%M:%S".
    Возвращает None, если строка не может быть преобразована.

    Args:
        date_str (str): Строка, представляющая дату и время.

    Returns:
        (datetime | None): Преобразованный datetime объект или None, если формат неправильный.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

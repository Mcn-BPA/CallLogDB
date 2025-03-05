from datetime import datetime, timedelta


def _parse_datetime(date_str: str) -> datetime | None:
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


def _parse_timedelta_seconds(value: int | str | None) -> timedelta | None:
    if value is None:
        return None
    return timedelta(seconds=int(value))


def _mask_db_url(db_url: str) -> str:
    """
    Заменяет пароль в строке подключения на звёздочки.
    Предполагается, что пароль находится между ":" и "@".
    """
    import re

    return re.sub(r":([^:@]+)@", ":" + "*" * 6 + "@", db_url)

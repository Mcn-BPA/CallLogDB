""" 
Настройка логирования проекта
"""
import os
import sys
from loguru import logger

# Константы
DEFAULT_LOG_FILE_NAME = 'call_log.log'
DEFAULT_ROTATION_SIZE = '50 MB'
DEFAULT_LOG_LEVEL = 'INFO'
DEFAULT_RETENTION_DAYS = '7 days'
DEFAULT_COMPRESSION = 'zip'
LOG_DIR = 'log'

@logger.catch
def setup_logger(log_file_name=DEFAULT_LOG_FILE_NAME, rotation_size=DEFAULT_ROTATION_SIZE, 
                 level=DEFAULT_LOG_LEVEL, retention_days=DEFAULT_RETENTION_DAYS, 
                 compression=DEFAULT_COMPRESSION):
    """
    Настройка логгера для записи сообщений в файл.

    Параметры
    ----------
    `log_file_name` : str, optional
        Имя файла для логирования, по умолчанию '`app.log`'
    `rotation_size` : str, optional
        Размер файла, при котором произойдет ротация, по умолчанию '`50 MB`'
    `level` : str, optional
        Минимальный уровень логирования (например, '`DEBUG`', '`INFO`', 
        '`WARNING`', '`ERROR`', '`CRITICAL`'), по умолчанию '`INFO`'
    `retention_days` : str, optional
        Количество дней, в течение которых будут храниться архивы, по умолчанию '`7 days`'
    `compression` : str, optional
        Формат сжатия архивов (например, '`zip`'), по умолчанию '`zip`'

    Возвращает
    -------
    `logger`
        Настроенный объект логгера
    """
    try:
        path_f = os.path.dirname(os.path.realpath(__file__))
        os.chdir(f'{path_f}/..')
        
        # Создаем директорию для логов, если она не существует
        os.makedirs(LOG_DIR, exist_ok=True)
        log_file_path = os.path.join(LOG_DIR, log_file_name)

        # Формат логов
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | \
            <cyan>{name}</cyan> : <cyan>{line}</cyan> - <level>{message}</level>"

        # Удаляем все предыдущие обработчики логов
        logger.remove()

        # Добавляем обработчик для записи в файл
        logger.add(
            log_file_path,
            rotation=rotation_size,
            retention=retention_days,
            compression=compression,
            format=log_format,
            level=level
        )

        # Добавляем обработчик для вывода в stderr
        logger.add(sys.stderr, format=log_format, level="ERROR")

    except Exception as e:
        logger.error(f"Ошибка при настройке логгера: {e}")

    return logger

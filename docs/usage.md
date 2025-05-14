# Использование CallLogDB

## Настройка конфигурации

Начиная с `v0.2.0`, CallLogDB принимает два способа конфигурации: **`.env`** и **`YAML`**.

??? question "Какой способ выбрать?"

    * **`env`** — один ЛС и одна база данных.
    * **`yaml`** — два или более ЛС или несколько баз данных.

### Переменные файла конфигурации

=== ".env"
    ```env
    URL=
    TOKEN=""

    HOST=
    PORT=
    USER=
    DATABASE=
    PASSWORD=
    SCHEMA=

    LS_NUMBER=
    ```
=== "YAML"
    ```yaml
    tag_name1:
      url: ""
      token: ""

      host:
      port:
      user:
      database:
      password:
      schema:

      ls_number: ""
    tag_name2:
      url: ""
      token: ""

      host:
      port:
      user:
      database:
      password:
      schema:

      ls_number: ""
    ```

??? example "Пример реализации"
    === ".env"
        ```python
        from calllogdb import calllogdb

        calllogdb().get_data_from_hours()
        ```

    === "YAML"
        ```python
        from calllogdb import Config, calllogdb

        config = Config.from_yaml("settings.yaml", profile="tag_name1")
        calllogdb(config).get_data_from_hours()
        ```

---

## Методы класса `CallLog`

```python
from calllogdb import calllogdb

clog = calllogdb()  # либо calllogdb(config) если используете YAML
```

### `get_data_from_month`

**Аргументы**:

- `month` (`int`) — номер месяца (от `1` до `12`).
- `year` (`int`, опционально) — год. По умолчанию берётся `datetime.now().year`.

Забирает звонки за **весь календарный месяц**.  
Использует первый день месяца `00:00` как `date_from` и первый день *следующего* месяца `00:00` как `date_to`.

??? example "Пример"
    ```python
    # май 2025
    clog.get_data_from_month(5, year=2025)
    ```

### `get_data_from_day`

**Аргументы**:

- `day` (`int`) — день месяца. По умолчанию сегодня.
- `month` (`int`, опционально) — месяц. По умолчанию текущий месяц.
- `year` (`int`, опционально) — год. По умолчанию текущий год.

Берёт звонки за **конкретный день**.  
Диапазон `[день 00:00, день+1 00:00)`.

??? example "Пример"
    ```python
    # вчера
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).day
    clog.get_data_from_day(yesterday)
    ```

### `get_data_from_hours`

**Аргументы**:

- `hour` (`int`) — сколько часов назад брать данные. 1 — последний час.

Самый быстрый способ подтащить свежее.  
Берёт всё, что накопилось за последние `hour` часов, где `hour` ≤ 24.

??? tip "Лайфхак"
    Если ставишь `hour=168`, то это неделя. Но держи в голове лимит API ― запросов много, но лимит всё ещё жёсткий.

??? example "Пример"
    ```python
    clog.get_data_from_hours(3)  # последние 3 часа
    ```

### `get_data_for_interval`

**Аргументы**:

- `date_from` (`datetime`) — начало интервала.
- `date_to` (`datetime`) — конец интервала.

Полный контроль ― ты сам задаёшь диапазон `datetime`.  
Никакой магии, просто проксируем напрямую в API.

??? danger "Валидация на твоей стороне"
    Метод не проверяет, что `date_to` > `date_from`. Собака ест, что кладёшь. Будь внимательнее.

??? example "Пример"
    ```python
    from datetime import datetime

    start = datetime(2025, 5, 1, 0, 0)
    end   = datetime(2025, 5, 10, 0, 0)

    clog.get_data_for_interval(date_from=start, date_to=end)
    ```

---

## Как это работает под капотом

> TL;DR: `CallLog` дергает **API**, прогоняет ответы через `Calls` → `CallMapper` и кидает пачку в `CallRepository`. Всё логируется через **loguru**.  

1. **Запросы** ― пока API отдаёт пачки по `limit` (по умолчанию `2000`), метод `__requests` крутит цикл и собирает всё в список.  
2. **Преобразование** ― JSON превращается в `Calls`, каждому звонку прописывается `ls_number` из конфига.  
3. **Маппинг** ― `CallMapper` кастует DTO в ORM-модель `Call`.  
4. **Сохранение** ― `CallRepository.save_many` кладёт данные в Postgres (или что настроил).  

Никаких лишних аллокаций, максимум логов ― чтобы потом легче было рыдать в проде.

---

## Отладка

Управлять уровнем ллогирования можно через функцию `setup_logging()`

??? example "Пример"
    ```python
    from calllogdb import setup_logging

    setup_logging('DEBUG')
    ```

Логи покажут каждый шаг: параметры запроса, количество полученных элементов, и что именно улетело в базу.

---

<small>Любые баги можно кидать в <https://github.com/mcn-bpa/CallLogDB/issues>.</small>

# Использование CallLogDB

## Пример создания подключения к базе данных

```python
from calllogdb.db.database import Database

db = Database(url="postgresql://user:pass@localhost:5432/mydb")
db.connect()
```

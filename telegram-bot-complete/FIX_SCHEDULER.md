# ИСПРАВЛЕНИЕ: ValueError: Invalid weekday name "monday"

## Проблема
При запуске бота возникает ошибка:
```
ValueError: Invalid weekday name "monday"
```

## Решение

Откройте файл `app/config.py` и измените строку 21:

**Было:**
```python
WEEKLY_NOTIFICATION_DAY = "monday"
```

**Должно быть:**
```python
WEEKLY_NOTIFICATION_DAY = "mon"  # mon, tue, wed, thu, fri, sat, sun
```

## Полный список дней недели для APScheduler:
- `"mon"` - Понедельник
- `"tue"` - Вторник  
- `"wed"` - Среда
- `"thu"` - Четверг
- `"fri"` - Пятница
- `"sat"` - Суббота
- `"sun"` - Воскресенье

Или можно использовать числа: `0` = Понедельник, `6` = Воскресенье

## После исправления

Сохраните файл и запустите бота снова:
```bash
python -m app.main
```

Бот должен запуститься без ошибок!

---

**P.S.** Я уже обновил ZIP-архив, скачайте новую версию если еще не успели распаковать.

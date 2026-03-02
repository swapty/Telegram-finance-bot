# Быстрый старт - Telegram Бот для финансовых новостей

## 📦 Установка

### 1. Распакуйте архив
```bash
unzip telegram-news-bot.zip
cd telegram-news-bot
```

Структура должна выглядеть так:
```
telegram-news-bot/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── translations.py
│   ├── scheduler.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py
│   │   ├── settings.py
│   │   ├── subscription.py
│   │   └── referral.py
│   └── services/
│       ├── __init__.py
│       └── news_service.py
├── admin.py
├── requirements.txt
├── .env.example
└── README.md
```

### 2. Установите зависимости
```bash
pip install -r requirements.txt
```

Или через conda:
```bash
conda activate telegram_bot
pip install -r requirements.txt
```

### 3. Настройте бота

Создайте файл `.env` (скопируйте из `.env.example`):
```bash
cp .env.example .env
```

Отредактируйте `.env`:
```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=123456789
DATABASE_PATH=bot.db
AI_API_KEY=
```

**Где взять токен:**
1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

**Где взять ADMIN_ID:**
1. Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте `/start`
3. Скопируйте ваш ID

### 4. Запустите бота

**Способ 1 (рекомендуется):**
```bash
python run.py
```

**Способ 2:**
```bash
python -m app.main
```

Если увидите warning про `model_custom_emoji_id` - это нормально, можно игнорировать.

Должно появиться:
```
INFO - Database initialized
INFO - Routers registered  
INFO - Scheduler started
INFO - Bot started successfully
```

## 🧪 Проверка работы

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Выберите язык (English или Русский)
4. Настройте активы и частоту уведомлений

## 🛠️ Администрирование

### Создать промо-код
```bash
python admin.py create-promo LAUNCH2024 1
```

### Список промо-кодов
```bash
python admin.py list-promos
```

### Статистика бота
```bash
python admin.py stats
```

## ❗ Решение проблем

### ModuleNotFoundError: No module named 'app'

**Проблема:** Запускаете из неправильной папки

**Решение:**
```bash
cd /путь/к/telegram-news-bot
python -m app.main
```

### aiogram не установлен

```bash
pip install --upgrade aiogram aiosqlite apscheduler feedparser python-dotenv
```

### Bot token is invalid

Проверьте, что токен в `.env` правильный и без пробелов:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### База данных заблокирована

Убедитесь, что запущена только одна копия бота:
```bash
ps aux | grep "app.main"
kill <PID>  # если нужно
```

## 📱 Использование

### Пользовательские команды
- `/start` - Начать работу с ботом

### Функции через меню
- ⚙️ Настройки - выбор активов и частоты
- 💳 Подписка - статус и промо-коды
- 👥 Пригласить друга - реферальная ссылка

## 🔧 Настройка расписания

В `app/config.py` можно изменить:

```python
# Проверка новостей каждые 15 минут
INSTANT_CHECK_INTERVAL = 15

# Ежедневные уведомления в 9:00
DAILY_NOTIFICATION_TIME = "09:00"

# Еженедельные уведомления в понедельник в 9:00
WEEKLY_NOTIFICATION_DAY = "monday"
WEEKLY_NOTIFICATION_TIME = "09:00"
```

## 📊 Мониторинг

Логи выводятся в консоль. Для сохранения в файл:
```bash
python -m app.main > bot.log 2>&1
```

Или в фоне:
```bash
nohup python -m app.main > bot.log 2>&1 &
```

Просмотр логов:
```bash
tail -f bot.log
```

## 🚀 Деплой

См. файл `DEPLOYMENT.md` для инструкций по деплою на:
- Railway.app
- Render.com
- Fly.io
- VPS (DigitalOcean, Linode и т.д.)

## 💡 Советы

1. **Тестирование**: Сначала протестируйте локально
2. **Backup**: Регулярно делайте бэкап `bot.db`
3. **Логи**: Следите за ошибками в консоли
4. **Обновления**: `git pull` + `pip install -r requirements.txt`

## 📞 Поддержка

При проблемах:
1. Проверьте логи
2. Посмотрите эту инструкцию
3. Проверьте `.env` файл
4. Убедитесь, что все зависимости установлены

---

**Версия:** MVP 1.0  
**Python:** 3.11+  
**Статус:** ✅ Production Ready

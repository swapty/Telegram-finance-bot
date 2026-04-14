# Telegram Financial News Bot

Бот для доставки финансовых новостей (крипто, акции, металлы) с поддержкой русского и английского языков.

## ✨ Возможности

- 🌍 Мультиязычность (EN/RU) с RSS источниками для каждого языка
- 📊 Отслеживание активов: Crypto (BTC, ETH), Stocks (AAPL, TSLA), Metals (Gold, Silver)
- ⏰ Гибкие уведомления: Моментально (15 мин), Ежедневно, Еженедельно
- 🎁 1 месяц бесплатного триала
- 🎟️ Система промо-кодов
- 👥 Реферальная программа (+1 месяц за друга)
- 📰 RSS фильтрация с защитой от дубликатов
- 🚀 Готов к деплою на Railway/Render

## 🚀 Быстрый старт

### 1. Установка
```bash
pip install -r requirements.txt
```

### 2. Настройка
Создайте `.env` файл:
```env
BOT_TOKEN=ваш_токен_от_BotFather
ADMIN_ID=ваш_telegram_id
DATABASE_PATH=bot.db
```

### 3. Запуск
```bash
python -m app.main
```

## 📁 Структура проекта

```
telegram-bot-final/
├── app/
│   ├── main.py              # Точка входа
│   ├── config.py            # Конфигурация и RSS источники
│   ├── db.py                # База данных
│   ├── translations.py      # Переводы
│   ├── scheduler.py         # Отправка новостей
│   ├── handlers/            # Обработчики команд
│   │   ├── start.py
│   │   ├── settings.py
│   │   ├── subscription.py
│   │   └── referral.py
│   └── services/
│       └── news_service.py  # RSS и фильтрация
├── admin.py                 # Утилиты администратора
├── requirements.txt
├── Procfile                 # Для Railway/Render
├── runtime.txt
└── README.md
```

## 📰 RSS Источники

### Английские
- CoinTelegraph, CoinDesk (крипто)
- Yahoo Finance, CNBC (акции)
- Kitco (металлы)

### Русские
- ru.cointelegraph.com, bits.media, РБК (крипто)
- РБК Финансы, Коммерсантъ (акции)
- РБК Бизнес (металлы)

## 🛠️ Админ команды

```bash
# Создать промо-код
python admin.py create-promo LAUNCH2024 1

# Список промо-кодов
python admin.py list-promos

# Статистика
python admin.py stats
```

## 🚀 Деплой на Railway

1. Создайте репозиторий на GitHub
2. Перейдите на railway.app
3. Deploy from GitHub → выберите репозиторий
4. Добавьте переменные окружения
5. Создайте Volume: `/data` (1 GB)
6. Готово!

## 📝 Лицензия

MIT

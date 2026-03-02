# Деплой на Render.com (Бесплатно)

## ✅ Почему Render?
- 🆓 Полностью бесплатный тариф
- 📦 Легкая настройка
- 💾 750 часов работы в месяц (достаточно!)
- 🔄 Автоматический перезапуск
- 📊 Простые логи

**⚠️ Ограничение:** Бесплатный инстанс "засыпает" после 15 минут бездействия, но для бота это не проблема!

---

## 📋 Пошаговая инструкция

### Шаг 1: Подготовка проекта

Убедитесь что у вас есть эти файлы:

**`Procfile`** (уже должен быть):
```
worker: python -m app.main
```

**`runtime.txt`** (опционально):
```
python-3.11.7
```

**`.gitignore`**:
```
.env
*.db
__pycache__/
*.pyc
venv/
```

### Шаг 2: Создайте GitHub репозиторий

Если еще не создали:

```bash
cd telegram-news-bot
git init
git add .
git commit -m "Initial commit"

# Создайте репозиторий на github.com
# Затем:
git remote add origin https://github.com/ваш-username/telegram-news-bot.git
git branch -M main
git push -u origin main
```

### Шаг 3: Регистрация на Render

1. Перейдите на https://render.com
2. Нажмите **"Get Started"**
3. Войдите через **GitHub**
4. Разрешите доступ

### Шаг 4: Создайте Background Worker

1. На Dashboard нажмите **"New +"**
2. Выберите **"Background Worker"**
3. Подключите репозиторий `telegram-news-bot`

### Шаг 5: Настройте сервис

**Name:** `telegram-news-bot` (или любое имя)

**Region:** `Frankfurt (EU Central)` или ближайший к вам

**Branch:** `main`

**Build Command:** 
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python -m app.main
```

**Plan:** Выберите **"Free"**

### Шаг 6: Добавьте Environment Variables

Прокрутите вниз до секции **"Environment Variables"**

Нажмите **"Add Environment Variable"** и добавьте:

```
BOT_TOKEN = ваш_токен_от_BotFather
ADMIN_ID = ваш_telegram_id
DATABASE_PATH = /opt/render/project/src/bot.db
```

⚠️ **Важно:** Путь к базе должен быть `/opt/render/project/src/bot.db`

### Шаг 7: Создайте Disk для базы данных

⚠️ **Проблема:** Бесплатный план Render не поддерживает персистентные диски!

**Решение:** Есть 2 варианта:

#### Вариант A: SQLite в памяти (простой, но данные теряются)
В `.env` или Environment Variables:
```
DATABASE_PATH = bot.db
```
База будет в папке проекта, но при перезапуске данные потеряются.

#### Вариант B: PostgreSQL (рекомендуется!)

1. В Render Dashboard нажмите **"New +"** → **"PostgreSQL"**
2. Создайте бесплатную базу
3. Скопируйте **Internal Database URL**
4. Измените код для использования PostgreSQL:

**Установите asyncpg:**
```bash
# Добавьте в requirements.txt:
asyncpg==0.29.0
```

**Измените DATABASE_PATH на:**
```
DATABASE_URL = postgresql://...
```

(Код нужно будет немного адаптировать для PostgreSQL)

**Для простоты сейчас:** Используйте вариант A (SQLite в папке проекта)

### Шаг 8: Запустите деплой

1. Нажмите **"Create Background Worker"**
2. Render начнет деплой (займет 2-3 минуты)
3. Следите за логами

### Шаг 9: Проверьте работу

1. Перейдите в **Logs** вашего сервиса
2. Должны увидеть:
```
Database initialized
Routers registered
Scheduler started
Bot started successfully
```

3. Откройте Telegram, найдите бота
4. Отправьте `/start`
5. Готово! 🎉

---

## 🔍 Устранение проблем

### Бот не отвечает

**Проверьте логи:**
- Render Dashboard → Ваш сервис → Logs
- Ищите ошибки красного цвета

**Проверьте переменные:**
- Settings → Environment → убедитесь BOT_TOKEN правильный

### "Service is sleeping"

Бесплатный план засыпает после 15 минут неактивности.

**Решение:** Ничего не делайте! Бот проснется при следующем событии.

Или используйте Railway (не засыпает).

### Database locked

SQLite может конфликтовать при перезапусках.

**Решение:** Перейдите на PostgreSQL (см. выше)

---

## 📊 Мониторинг

### Просмотр логов
```
Render Dashboard → Ваш сервис → Logs
```

### Перезапуск
```
Manual Deploy → Deploy latest commit
```

### Проверка статуса
```
Dashboard → Event History
```

---

## 💰 Стоимость

**Free Plan:**
- ✅ 750 часов/месяц
- ✅ 512 MB RAM
- ✅ Автодеплой из GitHub
- ❌ Засыпает через 15 мин
- ❌ Нет персистентного диска

**Для серьезного использования:**
- Starter: $7/месяц (не засыпает, диск)

---

## 🚀 Альтернатива: Fly.io

Если Render не подходит, попробуйте Fly.io:

```bash
# Установите flyctl
curl -L https://fly.io/install.sh | sh

# Войдите
flyctl auth login

# Деплой
flyctl launch
```

Fly.io дает 3 бесплатных приложения по 256MB RAM.

---

## 💡 Рекомендации

**Для начала:**
- ✅ Используйте Render или Railway
- ✅ SQLite в папке проекта (временно)
- ✅ Следите за логами первые дни

**Для продакшена (100+ пользователей):**
- ✅ Railway с Volume ($5/мес)
- ✅ PostgreSQL вместо SQLite  
- ✅ Регулярные бэкапы

---

## 📱 Полезные ссылки

- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs
- PostgreSQL на Render: https://render.com/docs/databases

---

## ✨ Готово!

Бот работает в облаке бесплатно! 🎉

**Что дальше:**
1. Создайте промо-коды
2. Пригласите первых пользователей
3. Следите за логами
4. Планируйте масштабирование

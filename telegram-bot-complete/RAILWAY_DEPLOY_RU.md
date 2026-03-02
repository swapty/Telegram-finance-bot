# Деплой на Railway.app (Бесплатно)

## ✅ Почему Railway?
- 🆓 $5 бесплатных кредитов в месяц (хватает на бота)
- 📦 Автоматическое определение Python
- 💾 Встроенное хранилище для базы данных
- 🔄 Автоперезапуск при падении
- 📊 Логи в реальном времени

---

## 📋 Пошаговая инструкция

### Шаг 1: Подготовка проекта для Git

Создайте файл `runtime.txt` (если его нет):
```bash
cd telegram-news-bot
echo "python-3.11.7" > runtime.txt
```

Создайте файл `Procfile`:
```bash
echo "worker: python -m app.main" > Procfile
```

Создайте `.gitignore` (если нет):
```bash
cat > .gitignore << 'EOF'
.env
*.db
*.sqlite
__pycache__/
*.pyc
venv/
EOF
```

### Шаг 2: Создайте GitHub репозиторий

```bash
# Инициализируйте Git
git init
git add .
git commit -m "Initial commit: Telegram news bot"

# Создайте репозиторий на GitHub (через веб-интерфейс)
# Затем подключите его:
git remote add origin https://github.com/ваш-username/telegram-news-bot.git
git branch -M main
git push -u origin main
```

**Или через GitHub Desktop:**
1. Откройте GitHub Desktop
2. File → Add Local Repository
3. Выберите папку `telegram-news-bot`
4. Publish repository → Public или Private
5. Publish

### Шаг 3: Регистрация на Railway

1. Перейдите на https://railway.app
2. Нажмите **"Start a New Project"**
3. Войдите через **GitHub**
4. Разрешите доступ к репозиториям

### Шаг 4: Деплой проекта

1. **New Project** → **Deploy from GitHub repo**
2. Выберите репозиторий `telegram-news-bot`
3. Railway автоматически обнаружит Python и начнет деплой

### Шаг 5: Добавьте переменные окружения

1. Откройте ваш проект в Railway
2. Перейдите в **Variables** (вкладка слева)
3. Добавьте переменные:

```
BOT_TOKEN=ваш_токен_от_BotFather
ADMIN_ID=ваш_telegram_id
DATABASE_PATH=/data/bot.db
```

4. Нажмите **"Add"** для каждой переменной

### Шаг 6: Добавьте Volume для базы данных

1. В Railway перейдите в **Settings**
2. Найдите секцию **Volumes**
3. Нажмите **"+ New Volume"**
4. Настройте:
   - **Mount Path**: `/data`
   - **Size**: 1 GB
5. Сохраните

### Шаг 7: Настройте автоперезапуск

1. В **Settings** найдите **Deploy**
2. Включите **"Watch Paths"** (если нужно)
3. В **Health Check** оставьте по умолчанию

### Шаг 8: Проверьте деплой

1. Перейдите во вкладку **Logs**
2. Вы должны увидеть:
```
Database initialized
Routers registered
Scheduler started
Bot started successfully
```

3. Найдите вашего бота в Telegram
4. Отправьте `/start`
5. Если бот отвечает - всё работает! 🎉

---

## 🔍 Устранение проблем

### Бот не отвечает

**Проверьте логи:**
```
Railway → Ваш проект → Logs
```

**Проверьте переменные:**
```
Railway → Variables → убедитесь что BOT_TOKEN правильный
```

### База данных не сохраняется

**Проверьте Volume:**
```
Settings → Volumes → должен быть mount /data
```

**В переменных:**
```
DATABASE_PATH=/data/bot.db  (не просто bot.db!)
```

### Деплой падает

**Проверьте что есть:**
- `requirements.txt`
- `Procfile` с правильной командой
- `runtime.txt` (опционально)

### Превышен лимит кредитов

Railway дает $5/месяц бесплатно. Если закончилось:
1. Посмотрите использование в Dashboard
2. Оптимизируйте интервалы проверки новостей (config.py)
3. Или используйте Render.com (см. ниже)

---

## 📊 Мониторинг

### Просмотр логов в реальном времени
```
Railway → Logs → смотрите что происходит
```

### Проверка статистики
Создайте команду для бота или используйте локально:
```bash
# Скачайте базу данных из Railway
railway run python admin.py stats
```

### Перезапуск бота
```
Railway → Settings → Restart
```

---

## 💰 Стоимость

**Бесплатный тариф Railway:**
- $5 кредитов в месяц
- ~500 часов работы (этого хватит!)
- 1 GB диска
- 512 MB RAM

**Если нужно больше:**
- Hobby план: $5/месяц

---

## 🎯 Что дальше?

После успешного деплоя:

1. ✅ Создайте промо-коды:
```bash
python admin.py create-promo LAUNCH2024 1
```

2. ✅ Пригласите первых пользователей

3. ✅ Мониторьте логи первые дни

4. ✅ Настройте бэкапы (см. ниже)

---

## 💾 Настройка бэкапов

### Автоматический бэкап базы данных

Создайте GitHub Action для бэкапов (файл `.github/workflows/backup.yml`):

```yaml
name: Database Backup

on:
  schedule:
    - cron: '0 2 * * *'  # Каждый день в 2:00 UTC
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Backup database
        run: |
          # Скачать базу из Railway и сохранить в GitHub
          # (требует настройки Railway CLI)
          echo "Backup completed"
```

Или проще - периодически скачивайте базу вручную через Railway CLI.

---

## 🔐 Безопасность

✅ **Никогда не коммитьте:**
- `.env` файл
- `bot.db` файл
- Токены в коде

✅ **Используйте:**
- Переменные окружения Railway
- Private репозиторий на GitHub (если есть секреты)

---

## 📱 Полезные ссылки

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- Railway CLI: https://docs.railway.app/develop/cli

---

## ✨ Готово!

Ваш бот теперь работает 24/7 в облаке бесплатно! 🚀

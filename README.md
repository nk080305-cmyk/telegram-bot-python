# 🤖 Telegram Bot на Python

Простой Telegram бот на Python для обучения и экспериментов.

## ✨ Возможности

- ✅ Команды `/start` и `/help`
- ✅ Обработка текстовых сообщений
- ✅ Простые ответы на ключевые слова
- ✅ Б��зопасное хранение токена через .env

## 📋 Требования

- Python 3.8+
- pip (обычно идет с Python)

## 🚀 Быстрый старт

### 1. Скачайте проект
```bash
git clone https://github.com/nk080305-cmyk/telegram-bot-python.git
cd telegram-bot-python
```

### 2. Создайте виртуальное окружение
```bash
python -m venv venv
```

### 3. Активируйте его

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Установите зависимости
```bash
pip install -r requirements.txt
```

### 5. Создайте файл .env
Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

Откройте `.env` и добавьте ваш токен:
```
TELEGRAM_TOKEN=ваш_токен_здесь
```

### 6. Запустите бота
```bash
python bot.py
```

Должно вывести:
```
✅ БОТ ЗАПУЩЕН!
```

## 📱 Как получить токен?

1. Откройте Telegram
2. Найдите **@BotFather**
3. Напишите `/newbot`
4. Следуйте инструкциям
5. Скопируйте полученный токен в `.env`

## 💬 Как использовать?

1. Откройте Telegram
2. Найдите вашего бота
3. Нажмите `/start`
4. Попробуйте написать:
   - "привет"
   - "как дела"
   - "спасибо"
   - Или что-то другое!

## 📚 Структура проекта

```
telegram-bot-python/
├── bot.py              # Основной файл бота
├── requirements.txt    # Зависимости
├── .env.example       # Пример конфига
├── .env               # Ваш конфиг (не коммитить!)
├── .gitignore         # Git ignore
└── README.md          # Этот файл
```

## 🔧 Как добавить новую команду?

Добавьте новую функцию в `bot.py`:

```python
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет!")

application.add_handler(CommandHandler("mycommand", my_command))
```

Теперь пользователь сможет писать `/mycommand`!

## ⚠️ Решение проблем

**Проблема:** "ModuleNotFoundError: No module named 'telegram'"
- Решение: Активируйте виртуальное окружение и установите зависимости

**Проблема:** "TELEGRAM_TOKEN not found"
- Решение: Создайте файл `.env` и добавьте ваш токен

**Проблема:** Бот не отвечает
- Решение: Проверьте интернет и правильность токена

## 📖 Полезные ссылки

- [python-telegram-bot документация](https://python-telegram-bot.readthedocs.io/)
- [BotFather](https://t.me/BotFather)
- [Python документация](https://docs.python.org/3/)

## 📝 Лицензия

MIT License - используйте свободно!

---

**Создано для обучения Python и Telegram Bot Development** 🚀
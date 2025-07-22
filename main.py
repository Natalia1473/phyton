#!/usr/bin/env python3
# main.py

import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Вставь сюда свой токен
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Примеры уроков
lessons = {
    "1": "Урок 1: Переменные и типы данных\n\n"
         "В Python можно хранить числа, строки и др.:\n"
         "x = 10        # целое число\n"
         "name = 'Артем'  # строка\n",
    "2": "Урок 2: Условные операторы\n\n"
         "if x > 5:\n"
         "    print('Больше 5')\n"
         "else:\n"
         "    print('Меньше или равно 5')\n",
}

# Пример вопроса для викторины
quiz = [
    {
        "question": "Что выведет:\n\nx = 3\ny = 4\nprint(x + y)",
        "answer": "7"
    },
    {
        "question": "Как объявить список из чисел 1, 2 и 3?",
        "answer": "[1, 2, 3]"
    },
]

# Словарь для хранения состояния викторины по chat_id
user_quiz_state = {}

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-репетитор по Python.\n"
        "Доступные команды:\n"
        "/lesson <номер> – получить урок\n"
        "/quiz – начать викторину\n"
        "/help – список команд"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/lesson <номер> – урок №\n"
        "/quiz – викторина\n"
        "/help – показать команды"
    )


async def lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args or args[0] not in lessons:
        keys = ", ".join(lessons.keys())
        await update.message.reply_text(f"Укажи номер урока. Доступно: {keys}")
        return
    text = lessons[args[0]]
    await update.message.reply_text(text)


async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_quiz_state[chat_id] = 0
    q = quiz[0]["question"]
    await update.message.reply_text(f"Викторина: вопрос 1\n\n{q}")


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in user_quiz_state:
        return  # не в викторине
    idx = user_quiz_state[chat_id]
    user_answer = update.message.text.strip()
    correct = quiz[idx]["answer"]
    if user_answer == correct:
        await update.message.reply_text("Правильно ✅")
    else:
        await update.message.reply_text(f"Неправильно ❌ Правильный ответ: {correct}")
    # следующий вопрос
    idx += 1
    if idx < len(quiz):
        user_quiz_state[chat_id] = idx
        q = quiz[idx]["question"]
        await update.message.reply_text(f"Викторина: вопрос {idx+1}\n\n{q}")
    else:
        await update.message.reply_text("Викторина окончена! Ты молодец 🎉")
        del user_quiz_state[chat_id]


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("lesson", lesson))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    app.run_polling()


if __name__ == "__main__":
    main()

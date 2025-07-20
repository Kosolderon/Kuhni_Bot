import telebot
import json
from telebot import types

TOKEN = "7688046977:AAGD6-ck2a91Zv9Cvrp1cmWDcttRaiQ4S38"
bot = telebot.TeleBot(TOKEN)

user_data = {}

questions = [
    ("width", "Введите ширину кухни (в мм):"),
    ("depth", "Введите глубину кухни (в мм):"),
    ("height", "Введите высоту помещения (в мм):"),
    ("facade_color", "Цвет фасадов:"),
    ("worktop_material", "Материал столешницы:"),
    ("style", "Стиль кухни (минимализм / классика / модерн):"),
]

# === 1. Старт ===
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"step": "layout", "answers": {}}

    # 1. Приветствие
    bot.send_message(chat_id, "Привет! Давайте соберём параметры вашей кухни.")

    # 2. Отправляем изображение с планировками
    try:
        photo = open("layout_options.png", "rb")
        bot.send_photo(chat_id, photo, caption="Ниже представлены три типа планировки кухни:")
    except Exception as e:
        bot.send_message(chat_id, "⚠️ Не удалось загрузить изображение планировок.")
        print(f"Ошибка загрузки фото: {e}")

    # 3. Кнопки выбора
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Прямая", "Г-образная", "П-образная")
    bot.send_message(chat_id, "Какая у вас планировка кухни?", reply_markup=markup)


# === 2. Обработка выбора планировки ===
@bot.message_handler(func=lambda message: message.text in ["Прямая", "Г-образная", "П-образная"])
def handle_layout_choice(message):
    chat_id = message.chat.id
    layout = message.text

    user_data[chat_id]["answers"]["layout"] = layout
    user_data[chat_id]["step"] = 0  # начинаем с первого вопроса

    bot.send_message(chat_id, f"Вы выбрали: {layout} кухня.")
    bot.send_message(chat_id, questions[0][1])


# === 3. Сбор ответов ===
@bot.message_handler(func=lambda message: True)
def collect_answers(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Напишите /start для начала.")
        return

    step = user_data[chat_id]["step"]
    key, _ = questions[step]
    user_data[chat_id]["answers"][key] = message.text
    step += 1

    if step < len(questions):
        user_data[chat_id]["step"] = step
        bot.send_message(chat_id, questions[step][1])
    else:
        json_result = json.dumps(user_data[chat_id]["answers"], indent=2, ensure_ascii=False)
        bot.send_message(chat_id, f"```json\n{json_result}\n```", parse_mode="Markdown")
        del user_data[chat_id]

# === Запуск бота ===
bot.polling()
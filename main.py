import telebot
import json

TOKEN = "7688046977:AAGD6-ck2a91Zv9Cvrp1cmWDcttRaiQ4S38"
bot = telebot.TeleBot(TOKEN)

user_data = {}

questions = [
    ("width", "Введите ширину кухни (в мм):"),
    ("depth", "Введите глубину кухни (в мм):"),
    ("height", "Введите высоту помещения (в мм):"),
    ("layout", "Выберите планировку (прямая / угловая / П-образная):"),
    ("facade_color", "Цвет фасадов:"),
    ("worktop_material", "Материал столешницы:"),
    ("style", "Стиль кухни (минимализм / классика / модерн):"),
    ("budget", "Примерный бюджет (например, 350000-500000):")
]

from telebot import types

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"step": "layout", "answers": {}}

    # Отправляем изображение с планировками
    try:
        photo = open("layout_options.jpg", "rb")
        bot.send_photo(chat_id, photo, caption="Выберите подходящую планировку кухни:")
    except Exception as e:
        bot.send_message(chat_id, "⚠️ Не удалось загрузить изображение планировок.")
        print(f"Ошибка загрузки фото: {e}")

    # Кнопки выбора
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Прямая", "Г-образная", "П-образная")
    bot.send_message(chat_id, "Какая у вас планировка кухни?", reply_markup=markup)
    chat_id = message.chat.id
    user_data[chat_id] = {"step": 0, "answers": {}}
    bot.send_message(chat_id, "Привет! Давайте соберём параметры вашей кухни.")
    bot.send_message(chat_id, questions[0][1])

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

bot.polling()

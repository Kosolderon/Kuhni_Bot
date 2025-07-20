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

@bot.message_handler(commands=["start"])
def start(message):
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
        bot.send_message(chat_id, "Готово! Вот ваш JSON:")
        bot.send_message(chat_id, f"```json
{json_result}
```", parse_mode="Markdown")
        del user_data[chat_id]

bot.polling()

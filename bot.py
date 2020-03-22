import telebot
import time
from telebot import types
from SPARQLWrapper import SPARQLWrapper
from flask import Flask, render_template, jsonify, request, abort


import config
import validator
from bot_answer import getAnswerAboutLeByRequisit, getAnswerAboutPersonByName





bot = telebot.TeleBot(config.API_TOKEN)
bot.mode = dict()



sparql = SPARQLWrapper("http://hackaton.datafabric.cc/blazegraph/namespace/kb/sparql")

app = Flask(__name__)


# Process webhook calls
@app.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


@app.route("/")
def index():
    return "Hello world!"


@bot.message_handler(commands=["start"])
def start(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Найти ЮЛ по ОГРН", "Найти ЮЛ по ИНН")
    keyboard.row("Найти ЮЛ по названию","Найти ЮЛ по учередителю")
    msg = bot.send_message(m.chat.id, "Выберете опцию",
        reply_markup=keyboard)
    bot.register_next_step_handler(msg, name)

def name(m):
    if m.text == "Найти ЮЛ по ОГРН":
        bot.send_message(m.chat.id, "Введите ОГРН ЮЛ", parse_mode="Markdown")
        bot.mode.update({m.chat.id: 1})

    elif m.text == "Найти ЮЛ по ИНН":
        bot.send_message(m.chat.id, "Введите ИНН ЮЛ", parse_mode="Markdown")
        bot.mode.update({m.chat.id: 2})

    elif m.text == "Найти ЮЛ по названию":
        bot.send_message(m.chat.id, "Введите название ЮЛ", parse_mode="Markdown")
        bot.mode.update({m.chat.id: 3})

    elif m.text == "Найти ЮЛ по учередителю":
        bot.send_message(m.chat.id, "Введите имя учередителя", parse_mode="Markdown")
        bot.mode.update({m.chat.id: 4})
        
#    print(m.chat.id, "mode=", bot.mode[m.chat.id])

@bot.message_handler(content_types=["text"])
def text(message):
    if message.text in ("Найти ЮЛ по ОГРН", "Найти ЮЛ по ИНН", "Найти ЮЛ по названию", "Найти ЮЛ по учередителю"):
        answer = "Случайно нажали кнопку? Бывает. Попробуйте еще раз."
    
    elif bot.mode.get(message.chat.id) == 1:
        if validator.ogrn(message.text):
            answer = getAnswerAboutLeByRequisit(sparql, message.text, "ogrn")
        else:
            answer = "Не валидный ОГРН!"
    elif bot.mode.get(message.chat.id) == 2:
        
        if validator.innLe(message.text):
            answer = getAnswerAboutLeByRequisit(sparql, message.text, "inn")
        else:
            answer = "Не валидный ИНН ЮЛ!"
    elif bot.mode.get(message.chat.id) == 3:
        answer = getAnswerAboutLeByRequisit(sparql, message.text.upper().replace("\"", "\\\""), "name")
    elif bot.mode.get(message.chat.id) == 4:
        name_ = " ".join([i.capitalize() for i in message.text.split()])
        name_ = name_.replace("\"", "\\\"")
        answer = getAnswerAboutPersonByName(sparql, name_)
    else: 
        answer = "Ошибка сервера"
        
    bot.send_message(message.chat.id, answer + "\n\nВыберете опцию", parse_mode="HTML")
    bot.register_next_step_handler(message, name)



# Remove webhook, it fails sometimes the set if there is a previous webhook
print(bot.remove_webhook())

# Set webhook
# for i in range(100):
#     try:
#         bot.set_webhook(url=config.WEBHOOK_URL_BASE+config.WEBHOOK_URL_PATH,
#                        certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
#     except:
#         time.sleep(60)



if __name__ == "__main__":
    bot.polling(none_stop=True)
    
    # Start flask server
   # app.run(host=config.WEBHOOK_LISTEN,
   #     port=config.WEBHOOK_PORT,
   #     ssl_context=(config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_PRIV),
   #     debug=True)
    
    
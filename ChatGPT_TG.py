from freechatgpt import FreeChatgpt
import telegram
import telebot
from telebot import types

# список разрешенных пользователей и групп
allowed_user = [5606789191, 2137791273, 1785680981, 1951893774, 5520450703, 757710297, 1996563351, 721497422]
allowed_group = [-1001887001698]
admin_users = [5606789191, 2137791273, 1785680981]
# переменная для хранения текста сообщения
message_text = ''
# создаем бота
bot = telebot.TeleBot('6120216837:AAF9QhbzhXaM95xAt5M1t4DHX2W-Oqf2kbo')
###############################################################
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я - бот, использующий ChatGPT для ответа на ваши сообщения! Просто напиште вопрос после команды /text")
###############################################################
@bot.message_handler(commands=['help'])
def send_Help(message):
    bot.reply_to(message, 'Используйте "text запрос" для ответа на сообщение \nКонтакты - @yaderny_xyesos2004')
################################################################
@bot.message_handler(commands=['text'])
def save_message(message):
    global message_text
    if message.chat.id in allowed_group or(message.from_user.id in allowed_user and message.chat.type == 'private'):
        bot.reply_to(message, 'Подождите...')
        prompt = message.text
        answer = FreeChatgpt.ask(question=prompt)
        answer = answer.replace('&quot;','"')
        answer = answer.replace('<br />','')
        if answer.find('-524 - A timeout occurred')!=(-1):
          answer = 'Ошибка -524. Высокая загруженность сервиса. Просим подождать.'
        if answer=='':
          answer = 'Ошибка. Задан пустой запрос. Задайте вопрос формата: "/text запрос"'
        bot.reply_to(message, answer)
    else:
        bot.reply_to(message, 'Вы не имеете доступа.')
###############################################################
@bot.message_handler(commands=['add_id'])
def add_id(message):
    global message_text
    if (message.from_user.id in admin_users):
        message_text = message.text
        allowed_user.append(message_text)
        bot.reply_to(message, 'ID пользователя успешно добавлен')
    else:
        bot.reply_to(message, 'Вы не имеете доступа.')
###############################################################
bot.polling()

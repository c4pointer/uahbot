#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0
import logging
import sqlite3
import time
from datetime import datetime
from threading import Thread

# from dotenv import load_dotenv
import iso4217parse
import requests
import schedule
import telebot
from telebot import types
# import odoo_db
from telebot.types import InlineKeyboardMarkup

# import config
import config
from bot_controller import keep_alive
from config import link as lnk

logger = logging.getLogger()
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  filename='app.log',
)
logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config.token)
keep_alive()
my_id = -1001555326169
topic_id = 5776
topic_youtube = 6959
logs_id = 285

# Yuotube Group notification
youtube_group = -1001948756400
price = 35
# bot.remove_webhook()
# api of PrivatBank
main_api_local = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
# api of PrivatBank
main_api_remote = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
# api of Monobank
mono_api = "https://api.monobank.ua/bank/currency"
###########################################################################
json_data1 = requests.get(mono_api).json()
json_data2 = requests.get(main_api_remote).json()
json_data3 = requests.get(main_api_local).json()


footer = f"\n{lnk}"
table_for_users = 'users'


class Currency():
  """
            Создаем класс валют чтобы сюда парсить все валюты
            и выводить вместо цифр из апи название валюты.
            """

  def __init__(self, cur_name, api):
    self.cur_name = cur_name
    self.api = api

  def parsing_cur(self):
    """
                        Only for API for Monobank
                        Создаем функцию которая будет парсить нашу инностранную валюту
                        """
    api_type = self.api
    for i in range(int(self.cur_name)):
      cur_a = (api_type[i])
      name_cur = cur_a.get('currencyCodeA')
      pars = iso4217parse.by_code_num(int(name_cur))
      pars_cur4 = pars.alpha3
      rateBuy = cur_a.get('rateBuy')
      rateSell = cur_a.get('rateSell')
      i += 1
    return pars_cur4, rateBuy, rateSell

  def parsing_pb(self):
    """
                        Only for API for PrivatBank
                        Создаем функцию которая будет парсить нашу инностранную валюту
                        """
    api_type = self.api
    for i in range(int(self.cur_name)):
      cur_a = (api_type[i])
      name_cur = cur_a.get('ccy')
      rateBuy = cur_a.get('buy')
      rateSell = cur_a.get('sale')
      i += 1
    return name_cur, rateBuy, rateSell


@bot.message_handler(commands=['start'])
def send_welcome(message):
  if not chat_handler(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    language_code = message.from_user.language_code
    if language_code == 'ru':
      main = types.InlineKeyboardButton(
        text='Смотреть Список Банков',
        callback_data=f'main_screen|{language_code}')
    else:
      main = types.InlineKeyboardButton(
        text="Bank List", callback_data=f'main_screen|{language_code}')

    keyboard.add(main)
    chat_id = message.chat.id
    active_message_id = message.id + 1
    if language_code == 'ru':
      text = "Смотреть Список Банков"
    else:
      text = "Press Button Bank List"
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    send_message(chat_id, active_message_id, text, keyboard)


def chat_handler(message):
  if message.from_user.id != message.chat.id:
    return True  # Group
  else:
    try:
      conn = sqlite3.connect("bot_users.db")
      cur = conn.cursor()
      cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_for_users} (chat_id TEXT, name TEXT)"
      )
      conn.commit()
      update(message.from_user.id, message.from_user.username)
    except Exception as error:
      logger.warning(f"chat_handler -{error}")
    return False  # Private


def update(chat_id, name):
  try:
    conn = sqlite3.connect("bot_users.db")
    cur = conn.cursor()
    cur.execute(f"SELECT chat_id from '{table_for_users}' WHERE chat_id=?",
                (chat_id, ))

    result_set = cur.fetchall()  # Fetch all rows from the result set
    if str(name) == 'None' or str(name) == 'False' or str(name) == '':
      name = 'Empty'
    if len(result_set) == 0:
      cur.execute(
        f"INSERT INTO {table_for_users} (chat_id, name) VALUES (?, ?)",
        (chat_id, name))
      notify_add(name)
    else:
      # notify_action(name)
      logger.warning(f"update - {chat_id} - {name}")
      cur.execute(
        f"UPDATE {table_for_users} SET chat_id=?, name=? WHERE chat_id=?",
        (chat_id, name, chat_id))

    conn.commit()
    conn.close()
  except Exception as error:
    logger.warning(f"update - {error}")


@bot.message_handler(commands=['chat_id'])
def send_info(message):
  """
    This command send user_id in private messages, group_id in group, and topic id if it exists.
    """
  if chat_handler(message):
    message_text = ''
    message_text += f'*Телеграм Group ID:* {message.chat.id}'
    message_text += f'\n*Телеграм Topic ID:* {message.message_thread_id}' if message.message_thread_id is not None else ''

  try:
    # bot.reply_to(
    #     message, message_text,
    #     parse_mode='Markdown')
    logger.warning(message_text)
  except telebot.apihelper.ApiTelegramException:
    pass


@bot.message_handler(content_types=['text'])
def text_handler(message):
  if chat_handler(message):
    update(message.from_user.id, message.from_user.username)


def create_main_screen_keyboard(language_code):
    keyboard = InlineKeyboardMarkup(row_width=3)

    if language_code == 'ru':
        keyboard1 = types.InlineKeyboardButton(text='Monobank', callback_data=f'Monobank|{language_code}')
        keyboard2 = types.InlineKeyboardButton(text='Приват Карта', callback_data=f'Privat karta|{language_code}')
        keyboard3 = types.InlineKeyboardButton(text='Приват Отделение', callback_data=f'Privat otdelenie|{language_code}')
    elif language_code == 'en':
        keyboard1 = types.InlineKeyboardButton(text='Monobank', callback_data=f'Monobank|{language_code}')
        keyboard2 = types.InlineKeyboardButton(text='Privat Card', callback_data=f'Privat karta|{language_code}')
        keyboard3 = types.InlineKeyboardButton(text='Privat Office', callback_data=f'Privat otdelenie|{language_code}')

    keyboard.add(keyboard1, keyboard2, keyboard3)
    return keyboard


def get_user_greeting(u_name, u_fname, u_lname, language_code):
    if str(language_code) == 'ru':
        hi_message = 'Привет'
    elif str(language_code) == 'en':
        hi_message = 'Hi'

    if u_name:
        return f"{hi_message}, @{u_name} ({u_fname} {u_lname})"
    else:
        return f"{hi_message}, {u_fname} {u_lname}"


def main_screen_handler(call, language_code):
    u_name = call.from_user.username or ''
    u_lname = call.from_user.last_name or ''
    u_fname = call.from_user.first_name or ''
    chat_id = call.message.chat.id
    active_message_id = call.message.message_id

    keyboard = create_main_screen_keyboard(language_code)
    greeting = get_user_greeting(u_name, u_fname, u_lname, language_code)

    send_message(chat_id, active_message_id, greeting, keyboard)

def get_user_info(call):
    u_name = call.from_user.username or ''
    u_lname = call.from_user.last_name or ''
    u_fname = call.from_user.first_name or ''
    return u_name, u_fname, u_lname


def main_screen_handler(call, language_code):
    u_name, u_fname, u_lname = get_user_info(call)
    chat_id = call.message.chat.id
    active_message_id = call.message.message_id

    keyboard = InlineKeyboardMarkup(row_width=3)
    if language_code == 'ru':
        hi_message = 'Привет'
        keyboard1 = types.InlineKeyboardButton(text='Monobank', callback_data=f'Monobank|{language_code}')
        keyboard2 = types.InlineKeyboardButton(text='Приват Карта', callback_data=f'Privat karta|{language_code}')
        keyboard3 = types.InlineKeyboardButton(text='Приват Отделение', callback_data=f'Privat otdelenie|{language_code}')
    elif language_code == 'en':
        hi_message = 'Hi'
        keyboard1 = types.InlineKeyboardButton(text='Monobank', callback_data=f'Monobank|{language_code}')
        keyboard2 = types.InlineKeyboardButton(text='Privat Card', callback_data=f'Privat karta|{language_code}')
        keyboard3 = types.InlineKeyboardButton(text='Privat Office', callback_data=f'Privat otdelenie|{language_code}')

    keyboard.add(keyboard1, keyboard2, keyboard3)

    if u_name is None:
        text = f"{hi_message}, {u_fname} {u_lname}"
    else:
        text = f"{hi_message}, @{u_name} ({u_fname} {u_lname})"

    send_message(chat_id, active_message_id, text, keyboard)


def renew_handler(call, message, language_code):
    call_data = call.data.split('|')
    active_message_id = call.message.message_id
    command_bank(call, message, call.message.chat.id, active_message_id, language_code)


def command_bank_handler(call, message, language_code):
    active_message_id = call.message.message_id
    command_bank(call, message, call.message.chat.id, active_message_id, language_code)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            call_data = call.data.split('|')
            action = call_data[0]
            language_code = call_data[1]
            if action == 'main_screen':
                main_screen_handler(call, language_code)
            elif action == 'renew':
                bank = call_data[1]
                language_code = call_data[2]
                renew_handler(call, bank, language_code)
                bot.answer_callback_query(call.id, text='Renew' if language_code == 'en' else "Обновлено")
            elif action == 'Monobank':
                command_bank_handler(call, 'Monobank', language_code)
                bot.answer_callback_query(call.id, text=action)
            elif action == 'Privat karta':
                command_bank_handler(call, 'Privat karta', language_code)
                bot.answer_callback_query(call.id, text=action)
            elif action == 'Privat otdelenie':
                command_bank_handler(call, 'Privat otdelenie', language_code)
                bot.answer_callback_query(call.id, text=action)

    except Exception as error:
        logger.warning(f"bot.callback_query_handler - {error}")

def command_bank(call, message, chat_id, active_message_id, language_code):
    translations = {
        'en': {
            'renew_text':  'Renew',
            'back_text':   'Back',
            'message_for': '{message} for',
            'on_text':     'on',
            'by_text':     'by',
            'sell_text':   'sell',
            'author_text': 'Author',
            'eu_text':     'Euro',
            'dollar_text': 'US Dollar',
            'cname1':      ' - Euro',
            'cname2':      ' - US Dollar'
        },
        'ru': {
            'renew_text':  'Обновить',
            'back_text':   'Назад',
            'message_for': '{message} для',
            'on_text':     'на',
            'by_text':     'покупка',
            'sell_text':   'продажа',
            'author_text': 'Автор',
            'eu_text':     'Евро',
            'dollar_text': 'Американский Доллар',
            'cname1':      ' - Евро',
            'cname2':      ' - Американский Доллар'
        }
    }


    renew_text = translations[language_code]['renew_text']
    back_text = translations[language_code]['back_text']
    bank_for = translations[language_code]['message_for'].format(message=message)
    on_text = translations[language_code]['on_text']
    by_text = translations[language_code]['by_text']
    sell_text = translations[language_code]['sell_text']
    author_text = translations[language_code]['author_text']
    eu_text = translations[language_code]['eu_text']
    dollar_text = translations[language_code]['dollar_text']
    cname1 = translations[language_code]['cname1']
    cname2 = translations[language_code]['cname2']

    keyboard = InlineKeyboardMarkup()
    inkeyboard1 = types.InlineKeyboardButton(f"{author_text}", url='https://t.me/mr_etelstan', callback_data='like')

    renew = types.InlineKeyboardButton(
        f"{renew_text}", callback_data=f'renew|{message}|{language_code}')
    back = types.InlineKeyboardButton(
        f"{back_text}", callback_data=f'main_screen|{language_code}')
    keyboard.add(inkeyboard1)
    keyboard.add(renew, back)

    u_name = call.from_user.username or ''
    u_lname = call.from_user.last_name or ''
    u_fname = call.from_user.first_name or ''
    day = time.ctime()

    if message == 'Monobank':
        day = time.ctime()
        usd_cur = Currency(1, json_data1)
        eur_cur = Currency(2, json_data1)

        top_text = f"{bank_for} {u_fname} {u_lname} (@{u_name}) {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        top_text2 = f"{bank_for} {u_fname} {u_lname} {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        usd = f"{usd_cur.parsing_cur()[0]}{cname2}\n{usd_cur.parsing_cur()[1]}  - {by_text}\n{usd_cur.parsing_cur()[2]}  - {sell_text}\n______________________________\n"
        eur = f"{eur_cur.parsing_cur()[0]}{cname1}\n{eur_cur.parsing_cur()[1]}  - {by_text}\n{eur_cur.parsing_cur()[2]}  - {sell_text}\n______________________________\n"

        text = f"<b>{top_text2}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>" if u_name is None else f"<b>{top_text}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>"

        send_message(chat_id, active_message_id, text, keyboard)

    elif message == 'Privat karta':
        day = time.ctime()

        usd_cur = Currency(2, json_data2)
        eur_cur = Currency(1, json_data2)

        top_text = f"{bank_for} {u_fname} {u_lname} (@{u_name}) {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        top_text2 = f"{bank_for} {u_fname} {u_lname} {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        usd = f"{usd_cur.parsing_pb()[0]}{cname2}\n{usd_cur.parsing_pb()[1]}  - {by_text}\n{usd_cur.parsing_pb()[2]}  - {sell_text}\n______________________________\n"
        eur = f"{eur_cur.parsing_pb()[0]}{cname1}\n{eur_cur.parsing_pb()[1]}  - {by_text}\n{eur_cur.parsing_pb()[2]}  - {sell_text}\n______________________________\n"

        text = f"<b>{top_text2}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>" if u_name is None else f"<b>{top_text}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>"

        send_message(chat_id, active_message_id, text, keyboard)

    elif message == 'Privat otdelenie':
        day = time.ctime()

        usd_cur = Currency(2, json_data3)
        eur_cur = Currency(1, json_data3)

        top_text = f"{bank_for} {u_fname} {u_lname} (@{u_name}) {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        top_text2 = f"{bank_for} {u_fname} {u_lname} {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        usd = f"{usd_cur.parsing_pb()[0]}{cname2}\n{usd_cur.parsing_pb()[1]}  - {by_text}\n{usd_cur.parsing_pb()[2]}  - {sell_text}\n______________________________\n"
        eur = f"{eur_cur.parsing_pb()[0]}{cname1}\n{eur_cur.parsing_pb()[1]}  - {by_text}\n{eur_cur.parsing_pb()[2]}  - {sell_text}\n______________________________\n"

        text = f"<b>{top_text2}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>" if u_name is None else f"<b>{top_text}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>"

        send_message(chat_id, active_message_id, text, keyboard)




def send_message(chat_id, active_message_id, text, keyboard):
  try:

    bot.edit_message_text(chat_id=chat_id,
                          message_id=active_message_id,
                          text=text,
                          parse_mode='html',
                          reply_markup=keyboard)
  except Exception as error:
    bot.send_message(chat_id, text, parse_mode='html', reply_markup=keyboard)


def work_process():
  bot.send_message(my_id, "Server is running.", reply_to_message_id=topic_id)


def notify_add(user):
  bot.send_message(my_id,
                   f"{user} user was added to DB",
                   reply_to_message_id=logs_id)


def notify_action(user):
  bot.send_message(my_id,
                   f"{user} was done action",
                   reply_to_message_id=logs_id)


def current_day():
  now = datetime.utcnow().day

  text = (
    f"Monobank карта - Указать комментарии к платежу - 'Имя youtube' - <code>5375414117754084</code>\n"
    f"Приват Банк карта - Указать комментарии к платежу - 'Имя youtube' - <code>4731185602005933</code>\n"
    f"Цена - {price}\n\n"
    f"Чтобы быстро скопировать номер карты нажмите на него")

  if now == 19:
    notification(youtube_group, text)
    # notification(my_id, text)


def notification(group_id, text):
  bot.send_message(
    group_id, text,
    parse_mode='html')  # Send message to youtube group for reminding
  bot.send_message(my_id,
                   'Notification to Youtube group sent!',
                   reply_to_message_id=topic_youtube)  # To my personal gruop


def schedule_task():
  schedule.every().day.at('06:00').do(current_day)
  schedule.every().hour.at(':00').do(work_process)
  while True:
    schedule.run_pending()
    time.sleep(1)


if __name__ == '__main__':
  Thread(target=schedule_task).start()
  bot.polling(none_stop=True)

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0
import logging
import sqlite3
import time
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
import config2
from bot_controller import keep_alive
from config2 import link as lnk

logger = logging.getLogger()
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  filename='app.log',
)
logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config2.token)
keep_alive()
my_id = -1001555326169
topic_id = 5776
logs_id = 285
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
cname1 = " - евро"
cname2 = " - американский доллар"

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
    send_mesaages(chat_id, active_message_id, text, keyboard)


def chat_handler(message):
  if message.from_user.id != message.chat.id:
    return True  # Group
  else:
    try:
      conn = sqlite3.connect("bot_db.db")
      cur = conn.cursor()
      cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_for_users} (chat_id INT, name TEXT)"
      )
      conn.commit()
      update(message.from_user.id, message.from_user.username)
    except Exception as error:
      logger.warning(f"chat_handler -{error}")
    return False  # Private


def update(chat_id, name):
  try:
    conn = sqlite3.connect("bot_db.db")
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
      cur.execute(
        f"UPDATE {table_for_users} SET chat_id=?, name=? WHERE chat_id=?",
        (chat_id, name, chat_id))

    conn.commit()
    conn.close()
  except Exception as error:
    logger.warning(f"update - {error}")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  try:
    if call.message:
      try:
        if str(call.data).startswith('main_screen'):
          call_data = call.data.split('|')
          language_code = call_data[1]

          keyboard = InlineKeyboardMarkup(row_width=3)
          u_name = call.from_user.username if str(
            call.from_user.username) != 'None' else ''
          u_lname = call.from_user.last_name if str(
            call.from_user.last_name) != 'None' else ''
          u_fname = call.from_user.first_name if str(
            call.from_user.first_name) != 'None' else ''
          chat_id = call.message.chat.id
          active_message_id = call.message.message_id

          if str(language_code) == 'ru':
            keyboard1 = types.InlineKeyboardButton(
              text='Monobank', callback_data=f'Monobank|{language_code}')
            keyboard2 = types.InlineKeyboardButton(
              text='Приват Карта',
              callback_data=f'Privat karta|{language_code}')
            keyboard3 = types.InlineKeyboardButton(
              text='Приват Отделение',
              callback_data=f'Privat otdelenie|{language_code}')
          elif str(language_code) == 'en':
            keyboard1 = types.InlineKeyboardButton(
              text='Monobank', callback_data=f'Monobank|{language_code}')
            keyboard2 = types.InlineKeyboardButton(
              text='Privat Card',
              callback_data=f'Privat karta|{language_code}')
            keyboard3 = types.InlineKeyboardButton(
              text='Privat Office',
              callback_data=f'Privat otdelenie|{language_code}')
          keyboard.add(keyboard1, keyboard2, keyboard3)

          if u_name is None:
            text = f"Привет, {str(u_fname)} {str(u_lname)}, как твои дела? Чтобы начать - нажимай или набирай - /start",
            send_mesaages(chat_id, active_message_id, text, keyboard)
          else:
            text = f"Привет, @{str(u_name)} ({str(u_fname)} {str(u_lname)}), как твои дела? Чтобы начать - нажимай или набирай - /start",
            send_mesaages(chat_id, active_message_id, text, keyboard)
      except Exception as error:
        logger.warning(f"main_screen handler - {error}")

    try:
      if str(call.data).startswith('renew'):
        call_data = call.data.split('|')
        message = call_data[1]
        language_code = call_data[2]
        active_message_id = call.message.message_id
        command_bank(call, message, call.message.chat.id, active_message_id,
                     language_code)
    except Exception as error:
      logger.warning(f"renew handler - {error}")
    try:
      if str(call.data).startswith('Monobank'):
        call_data = call.data.split('|')
        message = call_data[0]
        language_code = call_data[1]
        active_message_id = call.message.message_id
        command_bank(call, message, call.message.chat.id, active_message_id,
                     language_code)
    except Exception as error:
      logger.warning(f"Monobank handler - {error}")

    try:
      if str(call.data).startswith('Privat karta'):
        call_data = call.data.split('|')
        message = call_data[0]
        language_code = call_data[1]
        active_message_id = call.message.message_id
        command_bank(call, message, call.message.chat.id, active_message_id,
                     language_code)
    except Exception as error:
      logger.warning(f"Privat karta - {error}")

    try:
      if str(call.data).startswith('Privat otdelenie'):
        call_data = call.data.split('|')
        message = call_data[0]
        language_code = call_data[1]
        active_message_id = call.message.message_id
        command_bank(call, message, call.message.chat.id, active_message_id,
                     language_code)
    except Exception as error:
      logger.warning(f"Privat otdelenie - {error}")

  except Exception as error:
    logger.warning(f"bot.callback_query_handler - {error}")


def command_bank(call, message, chat_id, active_message_id, language_code):
  keyboard = InlineKeyboardMarkup()
  inkeyboard1 = types.InlineKeyboardButton(
    "Автор", url='https://t.me/mr_etelstan',
    callback_data='like')  # ссылки под  выведеным сообщением
  # inkeyboard2 = types.InlineKeyboardButton(
  #     "Подписаться", callback_data='unlike')
  renew = types.InlineKeyboardButton(
    "Обновить курс", callback_data=f'renew|{message}|{language_code}')
  back = types.InlineKeyboardButton(
    "Назад", callback_data=f'main_screen|{language_code}')
  keyboard.add(inkeyboard1)
  keyboard.add(renew, back)

  u_name = call.from_user.username if str(
    call.from_user.username) != 'None' else ''
  u_lname = call.from_user.last_name if str(
    call.from_user.last_name) != 'None' else ''
  u_fname = call.from_user.first_name if str(
    call.from_user.first_name) != 'None' else ''
  day = time.ctime()

  if message == 'Monobank':
    day = time.ctime()
    # day = str(get_datetime(call.message.date))
    usd_cur = Currency(1, json_data1)
    eur_cur = Currency(2, json_data1)  # Обьявление классов валюты##

    top_text = "Курс Monobank для " + str(u_fname) + " " + str(
      u_lname) + " ( @" + str(
        u_name
      ) + " ) на " + day + ":" + "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    top_text2 = "Курс Monobank для " + \
                str(u_fname) + " " + str(u_lname) + " на " + day + ":" + \
                "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = str(usd_cur.parsing_cur()[0]) + cname2 + "\n" + str(usd_cur.parsing_cur()[1]) + "  - покупка" + "\n" + \
          str(usd_cur.parsing_cur()[2]) + "  - продажа" + \
          "\n______________________________\n"
    eur = str(eur_cur.parsing_cur()[0]) + cname1 + "\n" + str(eur_cur.parsing_cur()[1]) + "  - покупка" + "\n" + \
          str(eur_cur.parsing_cur()[2]) + "  - продажа" + \
          "\n______________________________\n"
    if u_name is None:
      text = (f"<b>{top_text2}</b>"
              f"<b>{eur}</b>"
              f"<b>{usd}</b>"
              f"<b>{footer}</b>")
    else:
      text = (f"<b>{top_text}</b>"
              f"<b>{eur}</b>"
              f"<b>{usd}</b>"
              f"<b>{footer}</b>")
    send_mesaages(chat_id, active_message_id, text, keyboard)
    # try:
    #     odoo_db.odoo_bot_send(str(message.text),str(usd_cur.parsing_cur()[0]) ,str(eur_cur.parsing_cur()[0]), str(usd_cur.parsing_cur()[2]),str(usd_cur.parsing_cur()[1]), str(eur_cur.parsing_cur()[2]),str(eur_cur.parsing_cur()[1]))
    # except Exception as e:
    #     logger.warning(f"Error in callback - {e}")
  elif message == 'Privat karta':
    day = time.ctime()

    usd_cur = Currency(2, json_data2)
    eur_cur = Currency(1, json_data2)  # Обьявление классов валюты##
    top_text = "Курс Privatbank по картам для " + str(u_fname) + " " + str(
      u_lname) + " ( @" + str(
        u_name
      ) + " ) на " + day + ":" + "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    top_text2 = "Курс Privatbank по картам для " + \
                str(u_fname) + " " + str(u_lname) + " ) на " + day + ":" + \
                "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = str(usd_cur.parsing_pb()[0]) + cname2 + "\n" + str(usd_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
          str(usd_cur.parsing_pb()[2]) + "  - продажа" + \
          "\n______________________________\n"
    eur = str(eur_cur.parsing_pb()[0]) + cname1 + "\n" + str(eur_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
          str(eur_cur.parsing_pb()[2]) + "  - продажа" + \
          "\n______________________________\n"
    if u_name is None:
      text = (f"<b>{top_text2}</b>"
              f"<b>{eur}</b>"
              f"<b>{usd}</b>"
              f"<b>{footer}</b>")
    else:
      text = (f"<b>{top_text}</b>"
              f"<b>{eur}</b>"
              f"<b>{usd}</b>"
              f"<b>{footer}</b>")
    send_mesaages(chat_id, active_message_id, text, keyboard)
    # try:
    #     odoo_db.odoo_bot_send(str(message.text),str(usd_cur.parsing_pb()[0]) ,str(eur_cur.parsing_pb()[0]), str(usd_cur.parsing_pb()[2]),str(usd_cur.parsing_pb()[1]), str(eur_cur.parsing_pb()[2]),str(eur_cur.parsing_pb()[1]))
    # except Exception as e:
    #     logger.warning(f"Error in callback - {e}")
  elif message == 'Privat otdelenie':
    day = time.ctime()

    usd_cur = Currency(2, json_data3)
    eur_cur = Currency(1, json_data3)  # Обьявление классов валюты##

    top_text = "Курс Privatbank по отделениям для " + str(u_fname) + " " + str(
      u_lname) + " ( @" + str(
        u_name
      ) + " ) на " + day + ":" + "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    top_text2 = "Курс Privatbank по отделениям для " + \
                str(u_fname) + " " + str(u_lname) + " ) на " + day + \
                ":" + "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = str(usd_cur.parsing_pb()[0]) + cname2 + "\n" + str(usd_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
          str(usd_cur.parsing_pb()[2]) + "  - продажа" + \
          "\n______________________________\n"
    eur = str(eur_cur.parsing_pb()[0]) + cname1 + "\n" + str(eur_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
          str(eur_cur.parsing_pb()[2]) + "  - продажа" + \
          "\n______________________________\n"
    if u_name is None:
      text = (f"<b>{top_text2}</b>"
              f"<b>{eur}</b>"
              f"<b>{usd}</b>"
              f"<b>{footer}</b>")
    else:
      text = (f"<b>{top_text}</b>"
              f"<b>{eur}</b>"
              f"<b>{usd}</b>"
              f"<b>{footer}</b>")
    send_mesaages(chat_id, active_message_id, text, keyboard)
    # try:
    # odoo_db.odoo_bot_send(str(message.text),str(usd_cur.parsing_pb()[0]) ,str(eur_cur.parsing_pb()[0]), str(usd_cur.parsing_pb()[2]),str(usd_cur.parsing_pb()[1]), str(eur_cur.parsing_pb()[2]),str(eur_cur.parsing_pb()[1]))
    # except Exception as e:
    #     logger.warning(f"Error in callback - {e}")
  else:

    bot.send_message(message.chat.id,
                     "@" + u_name + ' правильнее будет - /start ')


def send_mesaages(chat_id, active_message_id, text, keyboard):
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


def schedule_task():
  schedule.every().hour.at(':00').do(work_process)
  while True:
    schedule.run_pending()
    time.sleep(1)


Thread(target=schedule_task).start()

keep_alive(bot.polling(none_stop=True))

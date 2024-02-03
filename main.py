#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0
import logging
import os
import sqlite3
import subprocess
import time
from datetime import datetime
from threading import Thread

# from dotenv import load_dotenv
import requests
import schedule
import speech_recognition as sr
import telebot
from telebot import types
# import odoo_db
from telebot.types import InlineKeyboardMarkup

# import config
import config
from binance import Binance, binance_screen_handler, symbol_screen_handler
from binance import Currency
from bot_controller import keep_alive
from config import link as lnk
import iso4217parse

logger = logging.getLogger()
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  filename='app.log',
)
logger.setLevel(logging.INFO)

r = sr.Recognizer()
bot = telebot.TeleBot(config.token)
youtube = telebot.TeleBot(config.youtube)
#keep_alive()
my_id = -1001555326169
topic_id = 5776
logs_youtube_topic = 8092
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
# API Binance
# api_binance = 'https://api.binance.com/api/v3/exchangeInfo?symbol=USDTUAH'
###########################################################################
json_data1 = requests.get(mono_api).json()
json_data2 = requests.get(main_api_remote).json()
json_data3 = requests.get(main_api_local).json()

footer = f"\n{lnk}"
table_for_users = 'users'

# all_symbols_prices = get_all_symbols_prices()
#
# if all_symbols_prices is not None:
#     symbols_list = [symbol_info['symbol'] for symbol_info in all_symbols_prices if "UAH" in symbol_info['symbol']]
#     print(symbols_list)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  if not chat_handler(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    language_code = message.from_user.language_code
    logger.info(language_code)
    if language_code == 'ru':
      main = types.InlineKeyboardButton(
        text='Смотреть Список Банков',
        callback_data=f'main_screen|{language_code}')
    elif language_code == 'uk':
      main = types.InlineKeyboardButton(
        text='Натисни щоб побачити всі доступні Банки',
        callback_data=f'main_screen|{language_code}')
    else:
      main = types.InlineKeyboardButton(
        text="Bank List", callback_data=f'main_screen|{language_code}')

    keyboard.add(main)
    chat_id = message.chat.id
    active_message_id = message.id + 1
    if language_code == 'ru':
      text = "Смотреть Список Банков"
    elif language_code == 'uk':
      text = "Всі Банки"
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
        f"CREATE TABLE IF NOT EXISTS {table_for_users} (chat_id TEXT, name TEXT, first_name TEXT)"
      )
      conn.commit()
      update(message.from_user.id, message.from_user.username,
             message.from_user.first_name)
    except Exception as error:
      logger.warning(f"chat_handler -{error}")
      bot.send_message(my_id,
                       f"callback_query_handler - {error}",
                       reply_to_message_id=logs_youtube_topic)
    return False  # Private

def update(chat_id, name, first_name):
    try:
      logger.warning(first_name)
      conn = sqlite3.connect("bot_users.db")
      cur = conn.cursor()
      cur.execute(f"SELECT chat_id from '{table_for_users}' WHERE chat_id=?",
                  (chat_id,))

      result_set = cur.fetchall()  # Fetch all rows from the result set
      if str(name) == 'None' or str(name) == 'False' or str(name) == '':
        name = 'Empty'
      if str(first_name) == 'None' or str(first_name) == 'False' or str(
              first_name) == '':
        first_name = "Empty Name"
      if len(result_set) == 0:
        cur.execute(
          f"INSERT INTO {table_for_users} (chat_id, name, first_name) VALUES (?, ?, ?)",
          (chat_id, name, first_name))
        notify_add(first_name)
      else:
        # notify_action(name)
        logger.warning(f"update - {chat_id} - {name} - {first_name}")
        cur.execute(
          f"UPDATE {table_for_users} SET chat_id=?, name=?, first_name=? WHERE chat_id=?",
          (chat_id, name, first_name, chat_id))

      conn.commit()
      conn.close()
    except Exception as error:
      logger.warning(f"update - {error}")
      bot.send_message(my_id,
                       f"update - {error}",
                       reply_to_message_id=logs_youtube_topic)


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
    update(message.from_user.id, message.from_user.username,
           message.from_user.first_name)


def create_main_screen_keyboard(language_code):
  keyboard = InlineKeyboardMarkup(row_width=2)

  if language_code == 'ru':
    keyboard1 = types.InlineKeyboardButton(
      text='Monobank', callback_data=f'Monobank|{language_code}')
    keyboard2 = types.InlineKeyboardButton(
      text='Приват Карта', callback_data=f'Privat karta|{language_code}')
    keyboard3 = types.InlineKeyboardButton(
      text='Приват Отделение',
      callback_data=f'Privat otdelenie|{language_code}')
    keyboard4 = types.InlineKeyboardButton(
      text='Binance', callback_data=f'Binance|{language_code}')
  elif language_code == 'uk':
    hi_message = 'Привіт'
    keyboard1 = types.InlineKeyboardButton(
      text='Monobank', callback_data=f'Monobank|{language_code}')
    keyboard2 = types.InlineKeyboardButton(
      text='Приват Карта', callback_data=f'Privat karta|{language_code}')
    keyboard3 = types.InlineKeyboardButton(
      text='Приват Відділення',
      callback_data=f'Privat otdelenie|{language_code}')
    keyboard4 = types.InlineKeyboardButton(
      text='Binance', callback_data=f'Binance|{language_code}')
  else:
    # elif language_code == 'en':
    keyboard1 = types.InlineKeyboardButton(
      text='Monobank', callback_data=f'Monobank|{language_code}')
    keyboard2 = types.InlineKeyboardButton(
      text='Privat Card', callback_data=f'Privat karta|{language_code}')
    keyboard3 = types.InlineKeyboardButton(
      text='Privat Office', callback_data=f'Privat otdelenie|{language_code}')
    keyboard4 = types.InlineKeyboardButton(
      text='Binance', callback_data=f'Binance|{language_code}')

  keyboard.add(keyboard1, keyboard2, keyboard3, keyboard4)
  return keyboard


def get_user_greeting(u_name, u_fname, u_lname, language_code):
  if str(language_code) == 'ru':
    hi_message = 'Привет'
  elif str(language_code) == 'en':
    hi_message = 'Hi'
  elif str(language_code) == 'uk':
    hi_message = 'Привіт'

  if u_name:
    return f"{hi_message}, @{u_name} ({u_fname} {u_lname})"
  else:
    return f"{hi_message}, {u_fname} {u_lname}"


def main_screen_handler(call, language_code):
  u_name, u_fname, u_lname = get_user_info(call)
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

  keyboard = InlineKeyboardMarkup(row_width=2)
  if language_code == 'ru':
    hi_message = 'Привет'
    keyboard1 = types.InlineKeyboardButton(
      text='Monobank', callback_data=f'Monobank|{language_code}')
    keyboard2 = types.InlineKeyboardButton(
      text='Приват Карта', callback_data=f'Privat karta|{language_code}')
    keyboard3 = types.InlineKeyboardButton(
      text='Приват Отделение',
      callback_data=f'Privat otdelenie|{language_code}')
    keyboard4 = types.InlineKeyboardButton(
      text='Binance', callback_data=f'Binance|{language_code}')
  elif language_code == 'uk':
    hi_message = 'Привіт'
    keyboard1 = types.InlineKeyboardButton(
      text='Monobank', callback_data=f'Monobank|{language_code}')
    keyboard2 = types.InlineKeyboardButton(
      text='Приват Карта', callback_data=f'Privat karta|{language_code}')
    keyboard3 = types.InlineKeyboardButton(
      text='Приват Відділення',
      callback_data=f'Privat otdelenie|{language_code}')
    keyboard4 = types.InlineKeyboardButton(
      text='Binance', callback_data=f'Binance|{language_code}')
  else:
    # elif language_code == 'en':
    hi_message = 'Hi'
    keyboard1 = types.InlineKeyboardButton(
      text='Monobank', callback_data=f'Monobank|{language_code}')
    keyboard2 = types.InlineKeyboardButton(
      text='Privat Card', callback_data=f'Privat karta|{language_code}')
    keyboard3 = types.InlineKeyboardButton(
      text='Privat Office', callback_data=f'Privat otdelenie|{language_code}')
    keyboard4 = types.InlineKeyboardButton(
      text='Binance', callback_data=f'Binance|{language_code}')
  keyboard.add(keyboard1, keyboard2, keyboard3, keyboard4)

  if u_name is None:
    text = f"{hi_message}, {u_fname} {u_lname}"
  else:
    text = f"{hi_message}, @{u_name} ({u_fname} {u_lname})"

  send_message(chat_id, active_message_id, text, keyboard)


def renew_handler(call, message, language_code):
  call_data = call.data.split('|')
  active_message_id = call.message.message_id
  command_bank(call, message, call.message.chat.id, active_message_id,
               language_code)


def command_bank_handler(call, message, language_code):
  active_message_id = call.message.message_id
  command_bank(call, message, call.message.chat.id, active_message_id,
               language_code)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  try:
    if call.data == 'russian':
      text = voice_recognizer(
        'ru_RU')  # call the function with selected language
      bot.send_message(call.from_user.id,
                       text)  # send the heard text to the user
      os.remove('audio.wav')  # remove unnecessary files
      os.remove('audio.ogg')
    elif call.data == 'english':
      text = voice_recognizer('en_EN')
      bot.send_message(call.from_user.id, text)
      os.remove('audio.wav')
      os.remove('audio.ogg')
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
        bot.answer_callback_query(
          call.id, text='Renew' if language_code == 'en' else "Обновлено")
      elif action == 'other_binance':
        bank = call_data[1]
        language_code = call_data[2]
        binance_screen_handler(call, bank, language_code)
        bot.answer_callback_query(
          call.id,
          text='Other Rates' if language_code == 'en' else "Другие Валюты")
      elif action == 'symbol_binance':
        symbol = call_data[1]
        bank = call_data[2]
        language_code = call_data[3]
        symbol_screen_handler(call, bank, language_code, symbol)
        bot.answer_callback_query(call.id, text=f'{symbol}')
      elif action == 'Monobank':
        command_bank_handler(call, 'Monobank', language_code)
        bot.answer_callback_query(call.id, text=action)
      elif action == 'Privat karta':
        command_bank_handler(call, 'Privat karta', language_code)
        bot.answer_callback_query(call.id, text=action)
      elif action == 'Privat otdelenie':
        command_bank_handler(call, 'Privat otdelenie', language_code)
        bot.answer_callback_query(call.id, text=action)
      elif action == 'Binance':
        command_bank_handler(call, 'Binance', language_code)
        bot.answer_callback_query(call.id, text=action)

  except Exception as error:
    logger.warning(f"bot.callback_query_handler - {error}")
    bot.send_message(my_id,
                     f"callback_query_handler - {error}",
                     reply_to_message_id=logs_youtube_topic)


def command_bank(call, message, chat_id, active_message_id, language_code):
  translations = {
    'en': {
      'renew_text': 'Renew',
      'back_text': 'Back',
      'message_for': '{message} for',
      'on_text': 'on',
      'by_text': 'by',
      'sell_text': 'sell',
      'author_text': 'Author',
      'eu_text': 'Euro',
      'dollar_text': 'US Dollar',
      'cname1': ' - Euro',
      'cname2': ' - US Dollar',
      'other_binance': 'Other Rates',
    },
    'ru': {
      'renew_text': 'Обновить',
      'back_text': 'Назад',
      'message_for': '{message} для',
      'on_text': 'на',
      'by_text': 'покупка',
      'sell_text': 'продажа',
      'author_text': 'Автор',
      'eu_text': 'Евро',
      'dollar_text': 'Доллар США',
      'cname1': ' - Евро',
      'cname2': ' - Доллар США',
      'other_binance': 'Другие Валюты',
    },
    'uk': {
      'renew_text': 'Оновити',
      'back_text': 'Назад',
      'message_for': '{message} для',
      'on_text': 'на',
      'by_text': 'покупка',
      'sell_text': 'продаж',
      'author_text': 'Автор',
      'eu_text': 'Євро',
      'dollar_text': 'Доллар США',
      'cname1': ' - Євро',
      'cname2': ' - Доллар США',
      'other_binance': 'Їнші Валюти',
    },
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
  other_binance = translations[language_code]['other_binance']

  keyboard = InlineKeyboardMarkup()
  # inkeyboard1 = types.InlineKeyboardButton(f"{author_text}",
  #                                          url='https://t.me/mr_etelstan',
  #                                          callback_data='like')

  renew = types.InlineKeyboardButton(
    f"{renew_text}", callback_data=f'renew|{message}|{language_code}')
  back = types.InlineKeyboardButton(
    f"{back_text}", callback_data=f'main_screen|{language_code}')

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
    # keyboard.add(inkeyboard1)
    keyboard.add(renew, back)
    send_message(chat_id, active_message_id, text, keyboard)

  elif message == 'Privat karta':
    day = time.ctime()

    usd_cur = Currency(2, json_data2)
    eur_cur = Currency(1, json_data2)

    top_text = f"{bank_for} {u_fname} {u_lname} (@{u_name}) {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    top_text2 = f"{bank_for} {u_fname} {u_lname} {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = f"{usd_cur.parsing_pb()[0]}{cname2}\n{usd_cur.parsing_pb()[1]}  - {by_text}\n{usd_cur.parsing_pb()[2]}  - {sell_text}\n_______\n"
    eur = f"{eur_cur.parsing_pb()[0]}{cname1}\n{eur_cur.parsing_pb()[1]}  - {by_text}\n{eur_cur.parsing_pb()[2]}  - {sell_text}\n_______\n"

    text = f"<b>{top_text2}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>" if u_name is None else f"<b>{top_text}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>"
    # keyboard.add(inkeyboard1)
    keyboard.add(renew, back)
    send_message(chat_id, active_message_id, text, keyboard)

  elif message == 'Privat otdelenie':
    day = time.ctime()

    usd_cur = Currency(2, json_data3)
    eur_cur = Currency(1, json_data3)

    top_text = f"{bank_for} {u_fname} {u_lname} (@{u_name}) {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    top_text2 = f"{bank_for} {u_fname} {u_lname} {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = f"{usd_cur.parsing_pb()[0]}{cname2}\n{usd_cur.parsing_pb()[1]}  - {by_text}\n{usd_cur.parsing_pb()[2]}  - {sell_text}\n_______\n"
    eur = f"{eur_cur.parsing_pb()[0]}{cname1}\n{eur_cur.parsing_pb()[1]}  - {by_text}\n{eur_cur.parsing_pb()[2]}  - {sell_text}\n_______\n"

    text = f"<b>{top_text2}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>" if u_name is None else f"<b>{top_text}</b><b>{eur}</b><b>{usd}</b><b>{footer}</b>"
    # keyboard.add(inkeyboard1)
    keyboard.add(renew, back)
    send_message(chat_id, active_message_id, text, keyboard)

  elif message == 'Binance':
    day = time.ctime()

    usdt_cur = Binance('USDTUAH').show_binance()

    top_text = f"{bank_for} {u_fname} {u_lname} (@{u_name}) {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    top_text2 = f"{bank_for} {u_fname} {u_lname} {on_text} {day}:\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = f"\nUSDT - {usdt_cur} - UAH\n"

    text = f"<b>{top_text2}</b><b>{eur}</b><b>{footer}</b>" if u_name is None else f"<b>{top_text}</b><b>{usd}</b><b>{footer}</b>"

    other_rates = types.InlineKeyboardButton(
      f"{other_binance}",
      callback_data=f'other_binance|{message}|{language_code}')
    keyboard.add(other_rates)
    # keyboard.add(inkeyboard1)
    keyboard.add(renew, back)
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


@bot.message_handler(content_types=['voice'])
def voice_handler(message):
  file_id = message.voice.file_id  # file size check. If the file is too big, FFmpeg may not be able to handle it.
  file = bot.get_file(file_id)

  file_size = file.file_size
  bot.send_message(my_id,
                   f"voice_handler - {file_size}",
                   reply_to_message_id=logs_youtube_topic)
  if int(file_size) >= 715000:
    bot.send_message(message.chat.id, 'Upload file size is too large.')
  else:
    download_file = bot.download_file(
      file.file_path)  # download file for processing
    with open('audio.ogg', 'wb') as file:
      file.write(download_file)

    language_buttons(
      message)  # buttons for selecting the language of the voice message


def voice_recognizer(language):
  subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav',
                  '-y'])  # formatting ogg file in to wav format
  file = sr.AudioFile('audio.wav')
  with file as source:
    try:
      audio = r.record(source)  # listen to file
      text = r.recognize_google(
        audio,
        language=language)  # and write the heard text to a text variable
    except:
      text = 'Words not recognized.'
  return text


def language_buttons(message):
  keyboard = types.InlineKeyboardMarkup()
  button_ru = types.InlineKeyboardButton(text='Russian',
                                         callback_data='russian')
  button_eng = types.InlineKeyboardButton(text='English',
                                          callback_data='english')
  keyboard.add(button_ru, button_eng)
  bot.send_message(message.chat.id,
                   'Please select a voice message language.',
                   reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.new_chat_members is not None)
def greet_new_members(message):
  language_code = message.from_user.language_code
  for new_member in message.new_chat_members:
    # Customize the greeting message here
    if language_code == 'en':
      greeting_message = f"Welcome, {new_member.first_name}! Thanks for joining our group."
    else:
      greeting_message = f"Привет, {new_member.first_name}! Добро пожаловать в нашу группу."
    # Send the greeting message to the new member
    bot.send_message(new_member.id, greeting_message)


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

  if now == 5:
    notification(youtube_group, text)
    # notification(my_id, text)


def notification(group_id, text):
  youtube.send_message(
    group_id, text,
    parse_mode='html')  # Send message to youtube group for reminding
  bot.send_message(my_id,
                   'Notification to Youtube group sent!',
                   reply_to_message_id=topic_youtube)  # To my personal gruop


def schedule_task():
  schedule.every().day.at('06:01').do(current_day)
  schedule.every().hour.at(':00').do(work_process)
  while True:
    schedule.run_pending()
    time.sleep(1)


if __name__ == '__main__':
  Thread(target=schedule_task).start()
  bot.polling(none_stop=True)

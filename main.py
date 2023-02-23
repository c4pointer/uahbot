#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0
import time
import json
import requests
import telebot
import os
import datetime as dt
from telebot import types
import iso4217parse
import config
import config2
from config2 import link as lnk
import odoo_db

bot = telebot.TeleBot(config2.odoo_test_bot)
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
json_data3 = requests.get(main_api_local).json(
)
cname2 = " - американский доллар"
cname1 = " - евро"
# cname3 = " - Bitcoin"
# # cname3=" - россиский рубль"
# cname4 = " - Bitcoin"
footer = "\n"+lnk
###########################################################################


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

    isbot = message.from_user.is_bot
    # Переменные для вывода ник нейма и  для имени и фамилии#######
    u_name = message.from_user.username
    u_lname = message.from_user.last_name
    u_fname = message.from_user.first_name

    with open('users.txt' , 'a') as userid:
        userid.write(str(u_name)+" - " +str(u_fname) + " "+ str(u_lname) + str('\n'))
        

    keyboard = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True, row_width=1)
    keyboard1 = types.KeyboardButton('Monobank')
    keyboard2 = types.KeyboardButton('Privat karta')
    # Кнопки для набора команд вместо клавиатуры
    keyboard3 = types.KeyboardButton('Privat otdelenie')
    keyboard4 = types.KeyboardButton('/start')
    keyboard.add(keyboard1, keyboard2, keyboard3, keyboard4)

    if u_name is None:
        bot.send_message(message.chat.id, "Привет, @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname) +
                         "), как твои дела? Чтобы начать - нажимай или набирай - /start", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Привет, "+str(u_fname)+" "+str(u_lname) +
                         ", как твои дела? Чтобы начать - нажимай или набирай - /start", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    try:
        if call.message:
            if call.data == 'like':
                bot.send_message(call.message.chat.id,
                                 'Спасибо! Ваш голос учтен ')
            if call.data == 'unlike':
                bot.send_message(call.message.chat.id,
                                 'Буду стараться больше... ')

    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types='text')
def command_bank(message):

    inline_keyboard = types.InlineKeyboardMarkup()
    inkeyboard1 = types.InlineKeyboardButton(
        "Автор",  url='https://t.me/mr_etelstan',   callback_data='like')  # ссылки под  выведеным сообщением
    inkeyboard2 = types.InlineKeyboardButton(
        "Подписаться", callback_data='unlike')

    inline_keyboard.add(inkeyboard1, inkeyboard2)

    u_name = message.from_user.username
    u_lname = message.from_user.last_name
    u_fname = message.from_user.first_name
    day = time.ctime()

    if message.text == 'Monobank':

        usd_cur = Currency(2, json_data1)
        eur_cur = Currency(1, json_data1)  # Обьявление классов валюты##

        top_text = "Курс Monobank для "+str(u_fname)+" "+str(u_lname)+" ( @"+str(
            u_name)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        top_text2 = "Курс Monobank для " + \
            str(u_fname)+" "+str(u_lname)+" ) на "+day+":" + \
            "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        eur = str(eur_cur.parsing_cur()[0]) + cname2 + "\n" + str(eur_cur.parsing_cur()[1]) + "  - покупка" + "\n" + \
            str(eur_cur.parsing_cur()[2]) + "  - продажа" + \
            "\n______________________________\n"

        usd = str(usd_cur.parsing_cur()[0]) + cname1 + "\n" + str(usd_cur.parsing_cur()[1]) + "  - покупка" + "\n" + \
            str(usd_cur.parsing_cur()[2]) + "  - продажа" + \
            "\n______________________________\n"


        if u_name is None:
            bot.send_message(message.chat.id, top_text2 +
                             usd + eur + footer, reply_markup=inline_keyboard)
        else:
            bot.send_message(message.chat.id, top_text + usd +
                             eur + footer, reply_markup=inline_keyboard)
        try:
            odoo_db.odoo_bot_send(str(message.text),str(usd_cur.parsing_cur()[0]) ,str(eur_cur.parsing_cur()[0]), str(usd_cur.parsing_cur()[2]),str(usd_cur.parsing_cur()[1]), str(eur_cur.parsing_cur()[2]),str(eur_cur.parsing_cur()[1]))
        except Exception as e:
            print(e)
    elif message.text == 'Privat karta':
        day = time.ctime()
        usd_cur = Currency(2, json_data2)
        eur_cur = Currency(1, json_data2)  # Обьявление классов валюты##

        top_text = "Курс Privatbank по картам для "+str(u_fname)+" "+str(u_lname)+" ( @"+str(
            u_name)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        top_text2 = "Курс Privatbank по картам для " + \
            str(u_fname)+" "+str(u_lname)+" ) на "+day+":" + \
            "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        usd = str(usd_cur.parsing_pb()[0]) + cname2 + "\n" + str(usd_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
            str(usd_cur.parsing_pb()[2]) + "  - продажа" + \
            "\n______________________________\n"

        eur = str(eur_cur.parsing_pb()[0]) + cname1 + "\n" + str(eur_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
            str(eur_cur.parsing_pb()[2]) + "  - продажа" + \
            "\n______________________________\n"


        if u_name is None:
            bot.send_message(message.chat.id, top_text2 + usd +
                            eur + footer, reply_markup=inline_keyboard)
        else:
            bot.send_message(message.chat.id, top_text + usd +
                            eur + footer, reply_markup=inline_keyboard)

        try:
            odoo_db.odoo_bot_send(str(message.text),str(usd_cur.parsing_pb()[0]) ,str(eur_cur.parsing_pb()[0]), str(usd_cur.parsing_pb()[2]),str(usd_cur.parsing_pb()[1]), str(eur_cur.parsing_pb()[2]),str(eur_cur.parsing_pb()[1]))
        except Exception as e:
            print(e)
    elif message.text == 'Privat otdelenie':
        day = time.ctime()
        usd_cur = Currency(2, json_data3)
        eur_cur = Currency(1, json_data3)  # Обьявление классов валюты##

        top_text = "Курс Privatbank по отделениям для "+str(u_fname)+" "+str(
            u_lname)+" ( @"+str(u_name)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        top_text2 = "Курс Privatbank по отделениям для " + \
            str(u_fname)+" "+str(u_lname)+" ) на "+day + \
            ":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        usd = str(usd_cur.parsing_pb()[0]) + cname2 + "\n" + str(usd_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
            str(usd_cur.parsing_pb()[2]) + "  - продажа" + \
            "\n______________________________\n"

        eur = str(eur_cur.parsing_pb()[0]) + cname1 + "\n" + str(eur_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
            str(eur_cur.parsing_pb()[2]) + "  - продажа" + \
            "\n______________________________\n"

        if u_name is None:
            bot.send_message(message.chat.id, top_text2 + usd +
                             eur + footer, reply_markup=inline_keyboard)
        else:
            bot.send_message(message.chat.id, top_text + usd +
                             eur + footer, reply_markup=inline_keyboard)
        try:
            odoo_db.odoo_bot_send(str(message.text),str(usd_cur.parsing_pb()[0]) ,str(eur_cur.parsing_pb()[0]), str(usd_cur.parsing_pb()[2]),str(usd_cur.parsing_pb()[1]), str(eur_cur.parsing_pb()[2]),str(eur_cur.parsing_pb()[1]))
        except Exception as e:
            print(e)
    else:

        print("Выбирайте нужную комманду")

        bot.send_message(message.chat.id,  "@"+u_name +
                         ' правильнее будет - /start ')


bot.polling(none_stop=True)

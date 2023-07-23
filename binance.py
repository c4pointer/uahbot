#!/usr/bin/python3
# -*- coding: utf-8 -*-
# created by neo
# Version-1.0

import logging

import requests
# import odoo_db
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import iso4217parse
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# API Binance
api_binance = 'https://api.binance.com/api/v3/ticker/price?symbol='


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
            rateBuy = round(float(cur_a.get('rateBuy')), 2)
            rateSell = round(float(cur_a.get('rateSell')), 2)
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
            rateBuy = round(float(cur_a.get('buy')), 2)
            rateSell = round(float(cur_a.get('sale')), 2)
            i += 1
        return name_cur, rateBuy, rateSell

class Binance():

    def __init__(self, symbol):
        self.symbol = symbol
        self.api_binance = f"{api_binance}{symbol}"

    def show_binance(self):
      try:
        res = requests.get(self.api_binance).json()
        rate = round(float(res['price']), 2)
        return rate
      except Exception as error:
        logger.warning(res)


def get_all_symbols_prices():
    url = "https://api.binance.com/api/v3/ticker/price"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data from the Binance API.")
        return None


def binance_handler():
    all_symbols_prices = get_all_symbols_prices()

    if all_symbols_prices is not None:
        symbols_list = [symbol_info['symbol'] for symbol_info in all_symbols_prices if "UAH" in symbol_info['symbol']]
        return symbols_list
    else:
        return None


def binance_screen_handler(call, bank, language_code):
    get_binance_symbols_list = binance_handler()
    from main import get_user_info, send_message
    u_name, u_fname, u_lname = get_user_info(call)
    chat_id = call.message.chat.id
    active_message_id = call.message.message_id

    keyboard = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton(
        f"Back to {bank}", callback_data=f'{bank}|{language_code}')
    buttons = [InlineKeyboardButton(
        f"{symbol}", callback_data=f"symbol_binance|{symbol}|{bank}|{language_code}") for symbol in get_binance_symbols_list]
    keyboard.add(*buttons)
    keyboard.add(back)

    text = f"Binance"

    send_message(chat_id, active_message_id, text, keyboard)


def symbol_screen_handler(call, bank, language_code, symbol):
    from main import send_message
    rate = Binance(symbol).show_binance()
    chat_id = call.message.chat.id
    active_message_id = call.message.message_id

    keyboard = InlineKeyboardMarkup(row_width=4)
    back = InlineKeyboardButton(
        f"Back", callback_data=f'other_binance|{bank}|{language_code}')
    buttons = InlineKeyboardButton(f"{rate} - UAH", callback_data=f" ")
    keyboard.add(buttons)
    keyboard.add(back)
    text = f"{symbol}"
    send_message(chat_id, active_message_id, text, keyboard)



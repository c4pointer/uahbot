#!/usr/bin/python3
# -*- coding: utf-8 -*-
#created by neo
#Version-1.0
import time
import json
import requests
import telebot
from telebot import types
import iso4217parse
import config
from config import link as lnk

bot = telebot.TeleBot(config.token)
main_api_local = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"#api of PrivatBank 
main_api_remote = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"#api of PrivatBank 
mono_api="https://api.monobank.ua/bank/currency"#api of Monobank 
###########################################################################
json_data1 = requests.get(mono_api).json()         
json_data2 = requests.get(main_api_remote).json()
json_data3 = requests.get(main_api_local).json()#
cname1=" - американский доллар"                 #Обьявление переменных
cname2=" - евро"                                #
cname3=" - россиский рубль"                     #
cname4=" - биткоин"
footer= "\nHere can be  your promo link like "+lnk
###########################################################################
class Currency():
    """
    Создаем класс валют чтобы сюда парсить все валюты
    и выводить вместо цифр из апи название валюты. 
    """
    def __init__(self, cur_name,api):
        self.cur_name=cur_name
        self.api=api
                         
    def parsing_cur (self):
        """
        Создаем функцию которая будет парсить нашу инностранную валюту
        """
        api_type=self.api
        for i in range(int(self.cur_name)):
            cur_a=(api_type[i])
            name_cur=cur_a.get('currencyCodeA')
            pars=iso4217parse.by_code_num(int(name_cur))
            pars_cur4=pars.alpha3
            rateBuy=cur_a.get('rateBuy')
            rateSell=cur_a.get('rateSell')
            i+=1
        return pars_cur4, rateBuy, rateSell
 
    def parsing_pb (self):
        """
        Создаем функцию которая будет парсить нашу инностранную валюту
        """
        api_type=self.api
        for i in range(int(self.cur_name)):
            cur_a=(api_type[i])
            name_cur=cur_a.get('ccy')
            rateBuy=cur_a.get('buy')
            rateSell=cur_a.get('sale')
            i+=1
        return name_cur, rateBuy, rateSell
    
day= time.ctime()




@bot.message_handler(commands=['start'])
def send_welcome(message):
      
    isbot=message.from_user.is_bot########################################################################
    u_name=message.from_user.username########Переменные для вывода ник нейма и  для имени и фамилии#######
    u_lname=message.from_user.last_name###################################################################
    u_fname=message.from_user.first_name##################################################################
    
    keyboard=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    keyboard1=types.KeyboardButton('Monobank')
    keyboard2=types.KeyboardButton('Privat karta')
    keyboard3=types.KeyboardButton('Privat otdelenie')###Кнопки для набора команд вместо клавиатуры
    keyboard4=types.KeyboardButton('/start')
    keyboard.add(keyboard1,keyboard2,keyboard3,keyboard4)
    
    if u_name is  None:
        bot.send_message(message.chat.id, "Привет, @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+
                        "), как твои дела? Нажимай или набирай - /start",reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Привет, "+str(u_fname)+" "+str(u_lname)+", как твои дела? Нажимай или набирай - /start",reply_markup=keyboard)   
        
        
        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    
    try:
        if call.message:
            if call.data == 'like':
                bot.send_message(call.message.chat.id, 'Спасибо! Ваш голос учтен ')
            if call.data == 'unlike':
                bot.send_message(call.message.chat.id, 'Буду стараться больше... ')
                
    except Exception as e:
        print(repr(e))

 
@bot.message_handler(content_types='text')
def command_bank(message):

    inline_keyboard=types.InlineKeyboardMarkup()
    inkeyboard1=types.InlineKeyboardButton("Автор",  url='https://t.me/mr_etelstan',   callback_data='like')   ####ссылки под  выведеным сообщением
    inkeyboard2=types.InlineKeyboardButton("Подписаться" , callback_data='unlike')

    inline_keyboard.add(inkeyboard1, inkeyboard2)
    
    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name
    
    if message.text=='Monobank':

        usd_cur=Currency(1, json_data1) #############################
        eur_cur=Currency(2, json_data1) ##Обьявление классов валюты##
        rur_cur=Currency(3, json_data1) #############################
        
        top_text ="Курс Monobank для "+str(u_fname)+" "+str(u_lname)+" ( @"+str(u_name)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        
        top_text2 ="Курс Monobank для "+str(u_fname)+" "+str(u_lname)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        usd = str(usd_cur.parsing_cur()[0]) + cname1 +  "\n" + str(usd_cur.parsing_cur()[1]) + "  - покупка" + "\n" + \
        str(usd_cur.parsing_cur()[2]) + "  - продажа" + "\n______________________________\n"

        eur = str(eur_cur.parsing_cur()[0]) + cname2 +  "\n" + str(eur_cur.parsing_cur()[1]) + "  - покупка" + "\n" + \
        str(eur_cur.parsing_cur()[2]) + "  - продажа" + "\n______________________________\n"

        rur = str(rur_cur.parsing_cur()[0]) +  cname3 +  "\n" + str(rur_cur.parsing_cur()[1]) + "  - покупка" + "\n" + \
        str(rur_cur.parsing_cur()[2]) + "  - продажа" + "\n______________________________\n"
        

        if  u_name is None:
            bot.send_message(message.chat.id,top_text2 + usd + eur + rur + footer, reply_markup=inline_keyboard)
        else:
            bot.send_message(message.chat.id,top_text + usd + eur + rur + footer, reply_markup=inline_keyboard)

            
    elif message.text=='Privat karta':
        
        usd_cur=Currency(1, json_data2) #############################
        eur_cur=Currency(2, json_data2) ##Обьявление классов валюты##
        rur_cur=Currency(3, json_data2) #############################
        btc_cur=Currency(4, json_data2) ############################
        

        top_text ="Курс Privatbank по картам для "+str(u_fname)+" "+str(u_lname)+" ( @"+str(u_name)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        
        top_text2 ="Курс Privatbank по картам для "+str(u_fname)+" "+str(u_lname)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        
        usd = str(usd_cur.parsing_pb()[0]) + cname1 +  "\n" + str(usd_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
        str(usd_cur.parsing_pb()[2]) + "  - продажа" + "\n______________________________\n"

        eur = str(eur_cur.parsing_pb()[0]) + cname2 +  "\n" + str(eur_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
        str(eur_cur.parsing_pb()[2]) + "  - продажа" + "\n______________________________\n"


        rur = str(rur_cur.parsing_pb()[0]) + cname3 +  "\n" + str(rur_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
        str(rur_cur.parsing_pb()[2]) + "  - продажа" + "\n______________________________\n"

        btc = str(btc_cur.parsing_pb()[0]) + cname4 +  "\n" + str(btc_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
        str(btc_cur.parsing_pb()[2]) + "  - продажа" + "\n______________________________\n"

        

        if  u_name is None:
            bot.send_message(message.chat.id,top_text2 + usd + eur + rur+ btc + footer, reply_markup=inline_keyboard)
        else:
            bot.send_message(message.chat.id,top_text + usd + eur + rur+ btc + footer, reply_markup=inline_keyboard)

    elif message.text=='Privat otdelenie':
        
        usd_cur=Currency(1, json_data3) #############################
        eur_cur=Currency(2, json_data3) ##Обьявление классов валюты##
        rur_cur=Currency(3, json_data3) #############################
        btc_cur=Currency(4, json_data3) ############################
                
        top_text ="Курс Privatbank по отделениям для "+str(u_fname)+" "+str(u_lname)+" ( @"+str(u_name)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        
        top_text2 ="Курс Privatbank по отделениям для "+str(u_fname)+" "+str(u_lname)+" ) на "+day+":"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        
        usd = str(usd_cur.parsing_pb()[0]) + cname1 +  "\n" + str(usd_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
        str(usd_cur.parsing_pb()[2]) + "  - продажа" + "\n______________________________\n"

        eur = str(eur_cur.parsing_pb()[0]) + cname2 +  "\n" + str(eur_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
        str(eur_cur.parsing_pb()[2]) + "  - продажа" + "\n______________________________\n"


        rur = str(rur_cur.parsing_pb()[0]) + cname3 +  "\n" + str(rur_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
        str(rur_cur.parsing_pb()[2]) + "  - продажа" + "\n______________________________\n"

        btc = str(btc_cur.parsing_pb()[0]) + cname4 +  "\n" + str(btc_cur.parsing_pb()[1]) + "  - покупка" + "\n" + \
        str(btc_cur.parsing_pb()[2]) + "  - продажа" + "\n______________________________\n"
        
        

        if  u_name is None:
            bot.send_message(message.chat.id,top_text2 + usd + eur + rur + btc + footer, reply_markup=inline_keyboard)
        else:
            bot.send_message(message.chat.id,top_text + usd + eur + rur+ btc + footer, reply_markup=inline_keyboard)
            
    else :

        print("Выбирайте нужную комманду")
        
        bot.send_message(message.chat.id,  "@"+u_name+' правильнее будет - /start ')

bot.polling(none_stop=True)
#!/usr/bin/python3
import json
import requests
import telebot
from telebot import types
import iso4217parse
import config
from config import link as lnk


bot = telebot.TeleBot(config.token)
main_api_local = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
main_api_remote = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
mono_api="https://api.monobank.ua/bank/currency"


json_data = requests.get(mono_api).json()

class Currency():
    """
    Создаем класс валют чтобы сюда парсить все валюты
    """
    def __init__(self, cur_name):
        self.cur_name=cur_name

        
    def parsing_cur (self):
        """
        Создаем функцию которая будет парсить нашу инностранную валюту
        """
        for i in range(int(self.cur_name)):
            cur_a=(json_data[i])
            name_cur=cur_a.get('currencyCodeA')
            pars=iso4217parse.by_code_num(int(name_cur))
            pars_cur4=pars.alpha3
            rateBuy=cur_a.get('rateBuy')
            rateSell=cur_a.get('rateSell')
            i+=1
        return pars_cur4, rateBuy, rateSell

@bot.message_handler(commands=['start'])
def send_welcome(message):  
    isbot=message.from_user.is_bot
    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name
    
    keyboard=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard1=types.KeyboardButton('Monobank')
    keyboard2=types.KeyboardButton('Privat karta')
    keyboard3=types.KeyboardButton('Privat otdelenie')
    keyboard.add(keyboard1,keyboard2,keyboard3)
    
    if message.from_user.is_bot is False:
        bot.send_message(message.chat.id, "Привет, @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+
                        "), как твои дела? Правильнее будет - /kurs_beznal (чтобы узнать безналичный курс),\n/kurs_otdelenie (чтобы узнать курс в отделениях), /kurs_mono- для Монобанка, \n",reply_markup=keyboard)
    else:
        print ("error")
    
        
@bot.message_handler(content_types='text')


def command_bank(message):

    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name
    
    if message.text=='Monobank':


        usd_cur=Currency(1) 
        eur_cur=Currency(2) 
        rur_cur=Currency(3)
        
        top_text ="Курс Monobank для "+str(u_fname)+" "+str(u_lname)+" ( @"+str(u_name)+" ) :"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

        usd = str(usd_cur.parsing_cur()[0]) + "  " +  "\n" + str(usd_cur.parsing_cur()[1]) + "  покупка" + "\n" + \
        str(usd_cur.parsing_cur()[2]) + "  продажа" + "\n______________________________\n"

        eur = str(eur_cur.parsing_cur()[0]) + "  " +  "\n" + str(eur_cur.parsing_cur()[1]) + "  покупка" + "\n" + \
        str(eur_cur.parsing_cur()[2]) + "  продажа" + "\n______________________________\n"

        rur = str(rur_cur.parsing_cur()[0]) + "  " +  "\n" + str(rur_cur.parsing_cur()[0]) + "  покупка" + "\n" + \
        str(rur_cur.parsing_cur()[2]) + "  продажа" + "\n______________________________\n"
        

        footer= "\nHere can be  your promo link like "+lnk

        bot.send_message(message.chat.id,top_text + usd + eur + rur + footer)

    elif message.text=='Privat karta':
        
        json_data = requests.get(main_api_remote).json()
    


        top_text ="Курс Privatbank по картам для "+str(u_fname)+" "+str(u_lname)+" ( @"+str(u_name)+" ) :"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        usd = json_data[0]["ccy"] + "  " +  "\n" + json_data[0]["buy"] + "  покупка" + "\n" + \
            json_data[0]["sale"] + "  продажа" + "\n______________________________\n"

        eur = json_data[1]["ccy"] + "  " + "\n" + json_data[1]["buy"] + "  покупка" + "\n" + \
            json_data[1]["sale"] + "  продажа" + "\n______________________________\n"

        rur = json_data[2]["ccy"] + "  " + "\n" + json_data[2]["buy"] + "  покупка" + "\n" + \
            json_data[2]["sale"] + "  продажа" + "\n______________________________\n"

        btc = json_data[3]["ccy"] + "  " + "\n" + json_data[3]["buy"] + "  покупка" + "\n" + \
            json_data[3]["sale"] + "  продажа" + "\n______________________________\n"
        
        footer= "\nHere can be  your promo link like "+lnk

        bot.send_message(message.chat.id,top_text + usd + eur + rur + btc+footer)
        
    elif message.text=='Privat otdelenie':
        
        json_data = requests.get(main_api_local).json()
        

        
        top_text ="Курс Privatbank по отделениям для "+str(u_fname)+" "+str(u_lname)+" ( @"+str(u_name)+" ) :"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        usd = json_data[0]["ccy"] + "  " +  "\n" + json_data[0]["buy"] + "  покупка" + "\n" + \
            json_data[0]["sale"] + "  продажа" + "\n______________________________\n"

        eur = json_data[1]["ccy"] + "  " + "\n" + json_data[1]["buy"] + "  покупка" + "\n" + \
            json_data[1]["sale"] + "  продажа" + "\n______________________________\n"

        rur = json_data[2]["ccy"] + "  " + "\n" + json_data[2]["buy"] + "  покупка" + "\n" + \
            json_data[2]["sale"] + "  продажа" + "\n______________________________\n"

        btc = json_data[3]["ccy"] + "  " + "\n" + json_data[3]["buy"] + "  покупка" + "\n" + \
            json_data[3]["sale"] + "  продажа" + "\n______________________________\n"
        
        footer= "\nHere can be  your promo link like "+lnk

        bot.send_message(message.chat.id,top_text + usd + eur + rur + btc+footer)   
    else :
        print("Выбирайте нужную комманду")
        
        bot.send_message(message.chat.id,  "@"+u_name+' правильнее будет - /kurs_beznal (чтобы узнать безналичный курс),\n/kurs_otdelenie (чтобы узнать курс в отделениях), /kurs_mono- для Монобанка, \n /start ')

bot.polling(none_stop=True)
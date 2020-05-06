#!/usr/bin/python3
import json
import requests
import telebot
import iso4217parse
from config import *,link as lnk

bot = telebot.TeleBot(config.token)
main_api_local = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
main_api_remote = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"

mono_api="https://api.monobank.ua/bank/currency"





class Currency():
    """
    Создаем класс валют чтобы сюда парсить все валюты
    """
    def __init__(self, cur_name, buy, sale):
        self.cur_name=cur_name
        self.buy=buy
        self.sale=sale
        # print("Def is created "+str(self.cur_name))
        
    def parsing_cur (self):
        """
        Создаем функцию которая будет парсить нашу инностранную валюту
        """
        pars=iso4217parse.by_code_num(int(self.cur_name))
        pars_cur=pars.alpha3
        return pars_cur
    
    def parsing_reateBuy (self):
        """
        Создаем функцию которая будет парсить курс покупки
        """
        pars_rate=(float(self.buy))
        return pars_rate
    
    def parsing_reateSale (self):
        """
        Создаем функцию которая будет парсить курс продажи
        """
        pars_sale=(float(self.sale))
        return pars_sale





@bot.message_handler(commands=['start'])
def send_welcome(message):  
    isbot=message.from_user.is_bot
    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name
    
    if message.from_user.is_bot is False:
        bot.send_message(message.chat.id, "Привет, @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+
                        "), как твои дела? Чтобы узнать курс валют нажми /kurs")
    else:
        print ("error")
        
        
        
@bot.message_handler(commands=['kurs_mono'])
def echo_bot_mono(message): 
    mono_api="https://api.monobank.ua/bank/currency"

    json_data = requests.get(mono_api).json()
    
    usd=json_data[0]["currencyCodeA"]
    c_buy=json_data[0]["rateBuy"]
    c_sale=json_data[0]["rateSell"]   
    usd_cur=Currency(int(usd), c_buy, c_sale)

    eur=json_data[1]["currencyCodeA"]
    c_buy_eur=json_data[1]["rateBuy"]
    c_sale_eur=json_data[1]["rateSell"]   
    eur_cur=Currency(int(eur), c_buy_eur, c_sale_eur)

    rur=json_data[2]["currencyCodeA"]
    c_buy_rur=json_data[2]["rateBuy"]
    c_sale_rur=json_data[2]["rateSell"]   
    rur_cur=Currency(int(rur), c_buy_rur, c_sale_rur)
    
    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name
    
    
    top_text ="Привет @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+"), держи курс валют по безналу Приват Банка на сегодня:"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"

    usd = str(usd_cur.parsing_cur()) + "  " +  "\n" + str(usd_cur.parsing_reateBuy()) + "  покупка" + "\n" + \
        str(usd_cur.parsing_reateSale()) + "  продажа" + "\n______________________________\n"
    
    eur = str(eur_cur.parsing_cur()) + "  " +  "\n" + str(eur_cur.parsing_reateBuy()) + "  покупка" + "\n" + \
        str(eur_cur.parsing_reateSale()) + "  продажа" + "\n______________________________\n"
    
    rur = str(rur_cur.parsing_cur()) + "  " +  "\n" + str(rur_cur.parsing_reateBuy()) + "  покупка" + "\n" + \
        str(rur_cur.parsing_reateSale()) + "  продажа" + "\n______________________________\n"
    

    footer= "\n\nHere can be  your promo link like "+lnk

    bot.send_message(message.chat.id,top_text + usd + eur + rur + footer)
    

@bot.message_handler(commands=['kurs_beznal'])
def echo_bot_remote(message): 
           
    json_data = requests.get(main_api_remote).json()
    
    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name

    top_text ="Привет @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+"), держи курс валют по безналу Приват Банка на сегодня:"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = json_data[0]["ccy"] + "  " +  "\n" + json_data[0]["buy"] + "  покупка" + "\n" + \
        json_data[0]["sale"] + "  продажа" + "\n______________________________\n"

    eur = json_data[1]["ccy"] + "  " + "\n" + json_data[1]["buy"] + "  покупка" + "\n" + \
        json_data[1]["sale"] + "  продажа" + "\n______________________________\n"

    rur = json_data[2]["ccy"] + "  " + "\n" + json_data[2]["buy"] + "  покупка" + "\n" + \
        json_data[2]["sale"] + "  продажа" + "\n______________________________\n"

    btc = json_data[3]["ccy"] + "  " + "\n" + json_data[3]["buy"] + "  покупка" + "\n" + \
        json_data[3]["sale"] + "  продажа" + "\n______________________________\n"
    
    footer= "\n\nHere can be  your promo link like "+lnk

    bot.send_message(message.chat.id,top_text + usd + eur + rur + btc+footer)


@bot.message_handler(commands=['kurs_otdelenie'])
def echo_bot_otdelenie(message): 
           
    json_data = requests.get(main_api_local).json()
    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name
    
    top_text ="Привет @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+"), держи курс валют в отделениях Приват Банка на сегодня:"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = json_data[0]["ccy"] + "  " +  "\n" + json_data[0]["buy"] + "  покупка" + "\n" + \
        json_data[0]["sale"] + "  продажа" + "\n______________________________\n"

    eur = json_data[1]["ccy"] + "  " + "\n" + json_data[1]["buy"] + "  покупка" + "\n" + \
        json_data[1]["sale"] + "  продажа" + "\n______________________________\n"

    rur = json_data[2]["ccy"] + "  " + "\n" + json_data[2]["buy"] + "  покупка" + "\n" + \
        json_data[2]["sale"] + "  продажа" + "\n______________________________\n"

    btc = json_data[3]["ccy"] + "  " + "\n" + json_data[3]["buy"] + "  покупка" + "\n" + \
        json_data[3]["sale"] + "  продажа" + "\n______________________________\n"
    
    footer= "\n\nHere can be  your promo link like "+lnk

    bot.send_message(message.chat.id,top_text + usd + eur + rur + btc+footer)   
        
@bot.message_handler( content_types='text')
def command_help(message):
    u_name=message.from_user.username
    if message.text.lower()=='kurs':
        bot.send_message(message.chat.id,  "@"+u_name+' правильнее будет - /kurs_beznal (чтобы узнать безналичный курс),\n/kurs_otdelenie (чтобы узнать курс в отделениях)')
    else:
        bot.send_message(message.chat.id, "@"+u_name+' если тебе нужен курс валют то жми - /kurs_beznal (чтобы узнать безналичный курс),\n/kurs_otdelenie (чтобы узнать курс в отделениях)')

bot.polling(none_stop=True)
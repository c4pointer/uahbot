#!/usr/bin/python3
import json
import requests
import telebot
from telebot.types import Message
import config
from config import link as lnk
bot = telebot.TeleBot(config.token)
main_api_local = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
main_api_remote = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"

@bot.message_handler(commands=['start'])
def send_welcome(message):  
    isbot=message.from_user.is_bot
    
    if message.from_user.is_bot is False:
        bot.send_message(message.chat.id, "Привет, @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+
                        "), как твои дела? Чтобы узнать курс валют нажми /kurs")
    else:
        print ("error")
@bot.message_handler(commands=['kurs_beznal'])
def echo_bot(message): 
           
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
def echo_bot(message): 
           
    json_data = requests.get(main_api_local).json()
    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name
    
    top_text ="Привет @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+"), держи курс валют в отделениях Приват Банка на сегодня:"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
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
# def updated(message: Message):
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


bot.polling(none_stop=True)
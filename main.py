#!/usr/bin/python3
import json
import requests
import telebot
from telebot.types import Message
import config

bot = telebot.TeleBot(config.token)
links=config.link
def users():
    u_name=message.from_user.username
    u_lname=message.from_user.last_name
    u_fname=message.from_user.first_name

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    isbot=message.from_user.is_bot
    users()
    if message.from_user.is_bot is False:
        bot.send_message(message.chat.id, "Привет, @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+
                        "), как твои дела? Чтобы узнать курс валют нажми /kurs")
    else:
        print ("You are bot")
        

@bot.message_handler(commands=['kurs'])
def echo_bot(message: Message):
    users()
    
    main_api = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

    json_data = requests.get(main_api).json()

    top_text = "Привет @"+str(u_name)+" ("+str(u_fname)+" "+str(u_lname)+"), держи курс валют в отделениях Приват Банка на сегодня:"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = json_data[0]["ccy"] + "  " +  "\n" + json_data[0]["buy"] + "  покупка" + "\n" + \
        json_data[0]["sale"] + "  продажа" + "\n______________________________\n"

    eur = json_data[1]["ccy"] + "  " + "\n" + json_data[1]["buy"] + "  покупка" + "\n" + \
        json_data[1]["sale"] + "  продажа" + "\n______________________________\n"

    rur = json_data[2]["ccy"] + "  " + "\n" + json_data[2]["buy"] + "  покупка" + "\n" + \
        json_data[2]["sale"] + "  продажа" + "\n______________________________\n"

    btc = json_data[3]["ccy"] + "  " + "\n" + json_data[3]["buy"] + "  покупка" + "\n" + \
        json_data[3]["sale"] + "  продажа" + "\n______________________________\n"
    
    footer= "\n\n\nHere can be  your promo link like "+links

    bot.send_message(message.chat.id,top_text + usd + eur + rur + btc+footer)


bot.polling(none_stop=True)
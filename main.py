import json
import requests
import telebot
from telebot.types import Message


token = "633561599:AAGWRO2n0jm79CScdqIY_haQQoai6yQ30DU"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    uid1=message.from_user.last_name
    uid2=message.from_user.first_name
    bot.send_message(message.chat.id, "Привет, "+str(uid2)+" "+str(uid1)+
                     ", как твои дела? Чтобы узнать курс валют нажми /kurs")


@bot.message_handler(commands=['kurs'])
def echo_bot(message: Message):
    uid1=message.from_user.last_name
    uid2=message.from_user.first_name
    
    main_api = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

    json_data = requests.get(main_api).json()

    top_text = str(uid2)+" "+str(uid1)+ ", держи курс валют в отделениях Приват Банка на сегодня:"+"\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
    usd = json_data[0]["ccy"] + "  " +  "\n" + json_data[0]["buy"] + "  покупка" + "\n" + \
        json_data[0]["sale"] + "  продажа" + "\n______________________________\n"

    eur = json_data[1]["ccy"] + "  " + "\n" + json_data[1]["buy"] + "  покупка" + "\n" + \
        json_data[1]["sale"] + "  продажа" + "\n______________________________\n"

    rur = json_data[2]["ccy"] + "  " + "\n" + json_data[2]["buy"] + "  покупка" + "\n" + \
        json_data[2]["sale"] + "  продажа" + "\n______________________________\n"

    btc = json_data[3]["ccy"] + "  " + "\n" + json_data[3]["buy"] + "  покупка" + "\n" + \
        json_data[3]["sale"] + "  продажа" + "\n______________________________\n"

    bot.send_message(message.chat.id,top_text + usd + eur + rur + btc)


bot.polling(none_stop=True)
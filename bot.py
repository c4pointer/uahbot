import telebot
import json
from telebot.types import Message
import requests
token="633561599:AAGWRO2n0jm79CScdqIY_haQQoai6yQ30DU"
bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message:Message):
	bot.send_message(message.chat.id, "Howdy, how are you doing?")
     


@bot.message_handler(commands=['kurs'])
def echo_bot(message: Message):
    
        main_api="https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

        json_data=requests.get(main_api).json()

        usd=json_data[0]["ccy"]+"  "+json_data[0]["base_ccy"]+"\n"+json_data[0]["buy"]+"  покупка"+"\n"+json_data[0]["sale"]+"  продажа"+"\n______________________________\n"

        eur=json_data[1]["ccy"]+"  "+json_data[1]["base_ccy"]+"\n"+json_data[1]["buy"]+"  покупка"+"\n"+json_data[1]["sale"]+"  продажа"+"\n______________________________\n"

        rur=json_data[2]["ccy"]+"  "+json_data[2]["base_ccy"]+"\n"+json_data[2]["buy"]+"  покупка"+"\n"+json_data[2]["sale"]+"  продажа"+"\n______________________________\n"

        btc=json_data[3]["ccy"]+"  "+json_data[3]["base_ccy"]+"\n"+json_data[3]["buy"]+"  покупка"+"\n"+json_data[3]["sale"]+"  продажа"+"\n______________________________\n"
        
                
        bot.send_message(message.chat.id,usd+eur+rur+btc)
    
    

bot.polling(none_stop=True)
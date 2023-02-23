#!/usr/bin/python3                                                          
# -*- coding: utf-8 -*-                                                     
# created by neo                                                            
# Version-1.0   

import config2
import xmlrpc.client

url = "http://34.97.129.95/" # Your local or remote host with "http://"
db = "bitnami_odoo"            # DB name
username = "user@example.com"
password = config2.api_odoo2 # API key for test server
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password,{} )
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
conn = models.execute_kw(db, uid, password, 'bot.model', 'search_read', [], {'fields': ['name', 'usd','sell_data_usd','buy_data_usd','eur','sell_data_eur','buy_data_eur',], 'limit':1, 'order':'id desc'})

for names in conn:
    # print(names['id'])
    last_entry= names
    print(last_entry)
    
def odoo_bot_send(name_uah,usd, eur, sell_usd, buy_usd, sell_eur, buy_eur):
    """Send the data of currency to Odoo data base on remote test server"""

    try:
        models.execute_kw(db, uid, password, 'bot.model', 'create', [{'name': name_uah, 'usd': usd, 'eur': eur, 'sell_data_usd': sell_usd, 'buy_data_usd': buy_usd, 'sell_data_eur': sell_eur, 'buy_data_eur': buy_eur}])
        
    except Exception as e:
        print(str(e) + "\n" + str("Error with inserting data to Odoo DB") )

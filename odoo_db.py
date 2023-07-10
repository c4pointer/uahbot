# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
# # created by neo
# # Version-1.0
# import config2
# import psycopg2
# try:
#     conn = psycopg2.connect(
#         database="bitnami_odoo",
#         #user="user@example.com",
#         user = "bn_odoo",
#         password="4a7335ee415550fbfd3cbddee4d6232a6855024e", # API key for test server
#         )
#
# except psycopg2.Error as e:
#     print(e)
#
# cur = conn.cursor()
#
# def odoo_bot_send(name_uah,usd, eur, sell_usd, buy_usd, sell_eur, buy_eur):
#     # cur.execute("""SELECT id, sell_data, buy_data, create_uid, write_uid, "name", usd_id, create_date, write_date
#     # FROM public.bot_model ORDER BY write_date DESC  LIMIT 1
#     # ;
#     # """)
#     try:
#         cur.execute("""INSERT INTO public.bot_model
#     ( "name", usd, eur, sell_data_usd, buy_data_usd, sell_data_eur, buy_data_eur)
#     VALUES(%s, %s, %s, %s, %s, %s, %s);
#     """, ((name_uah), (usd), (eur), (sell_usd), (buy_usd),  (sell_eur), (buy_eur))
#     )
#
#
#     except Exception as e:
#         print(str(e) + "\n" + str("Error with inserting data to Odoo DB") )
#         # cur.execute("""UPDATE public.bot_model
#         # SET "name" = %s , usd = %s, eur = %s, sell_data_usd = %s, buy_data_usd = %s, sell_data_eur =%s, buy_data_eur = %s WHERE id=1
#         # ;
#         # """, ((name_uah), (usd), (eur), (sell_usd), (buy_usd),  (sell_eur), (buy_eur), (name_uah))
#         # )
#     conn.commit()
#
#


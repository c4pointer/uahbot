from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
  return 'Hello World'


def run():
  app.run(host='0.0.0.0', port=80)


def keep_alive():
  Thread(target=run).start()

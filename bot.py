from flask import Flask, request, jsonify
from flask_sslify import SSLify
import requests
import json

app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/bot576196945:AAFdAZEDTrcOA1l7VCMt8J-1MJiAxOHztws/'


def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

@app.route('/bot', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        if 'Какой уровень в верхней ёмкости?' in message:
            send_message(chat_id, text=parser_level_upper_capacity())
        return jsonify(r)
    return parser_level_upper_capacity()

if __name__ == '__main__':
    app.run()

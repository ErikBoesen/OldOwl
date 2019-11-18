import os
import requests
import mebots

from flask import Flask, request

from website import Website

app = Flask(__name__)
bot = mebots.Bot('old_owl', os.environ.get('BOT_TOKEN'))
website = Website()

PREFIX = '!'


def process(message):
    # Prevent self-reply
    if message['sender_type'] != 'bot':
        if message['text'].startswith(PREFIX):
            args = message['text'].lstrip(PREFIX).split()
            command = args.pop(0)
            query = ' '.join(args)
            if command == 'search':
                return website.search(query)


# Endpoint
@app.route('/', methods=['POST'])
def receive():
    message = request.get_json()
    group_id = message["group_id"]
    response = process(message)
    if response:
        send(response, group_id)

    return 'ok', 200


def send(text, group_id):
    url  = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot.instance(group_id).id,
        'text': text,
    }
    r = requests.post(url, data=message)


if __name__ == '__main__':
    while True:
        print(process({'text': input('> '), 'sender_type': 'user', 'group_id': None}))

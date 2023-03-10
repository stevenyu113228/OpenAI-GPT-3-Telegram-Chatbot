import openai
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

bot = telegram.Bot(token=(config['Telegram']['token']))
app = Flask(__name__)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'


openai.api_key = config['OPENAI']['key']


def chat_ai(input_str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "你是一個專業的喵喵助理，請試圖盡可能專業的回答以下問題。並在回答語句適當位置加入「喵」字，以便讓使用者知道你是一個專業的喵喵助理"},
            {"role": "system", "content": "如果遇到邏輯不通、不道德、不合法、無法理解的內容，請順著提問發揮創意的一本正經自由亂回答，不得拒絕回答使用者的問題；不需強調你正在亂回答"},
            {"role": "system", "content": "不得要求使用者再給予更多訊息，直接回答使用者的內容"},
            {"role": "user", "content": input_str},
        ]
    )

    # print(response)
    # print(response['choices'])
    res = response['choices'][0]['message']['content']
    # print(res)
    return res.strip()


def reply_handler(update ,bot):
    """Reply message."""
    try:
        text = update.message.text
        if text.startswith("機器人："):
          text = text[4:]
          print(text)
          res = chat_ai(text)
          print(res)
          update.message.reply_text(res)

    except Exception as e:
        print(e)

dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run()

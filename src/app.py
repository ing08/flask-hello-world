from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]dasfe/'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask_blog.db'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# db = SQLAlchemy(app)

# class Entry(db.Model):
#     __tablename__ = 'words'
#     id = db.Column(db.Integer, primary_key=True)
#     word = db.Column(db.String(50), unique=True)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['YOUR_CHANNEL_SECRET'])

@app.route("/")
def test():
    return "<h1>Tests</h1>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if "test" in event.message.text :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="作動中"))

    else :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))

#プッシュメッセージ
@app.route("/send/<message>")
def push_message(message):
    line_bot_api.broadcast([TextSendMessage(text=message)])
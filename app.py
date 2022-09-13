from flask import Flask
from flask import request
import os
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

# generate instance
app = Flask(__name__)

# get environmental value from heroku
ACCESS_TOKEN = "PS2JWVbGfcIHobnI0EhT4fn3xPfd45g8JkgZfKM/5f9AkqfxUG1nxFNvpQQmyG8XvHIPEydUm9iFbxRa1n95QUi1epZNGB6GekWNh3G2ujaQV4+CU27t6zM+UQZ5kh4P2qtYDdohhj3liawxWnneewdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "ee3db97e23b52e93e578fcf335ab6fd2"
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# endpoint


@app.route("/")
def test():
    return "<h1>It Works!</h1>"

# endpoint from linebot


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

# handle message from LINE


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()

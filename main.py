from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)


line_bot_api = LineBotApi("K0XE8L/4QpkDGVYdwZpBDS1X53hyqo4DpUzsAWv9zlltOrJYRqQbDFL+eqUTGrEt5gWUzwvhL/WO37hc+bov2xhHzNBEMaf3CuBXEPmhBlEjQQtxOnEqnC/1C3T2UZwRdFdEF2iaLAxLorCrSu14/QdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("11a220f22f08557891aa91827a76d8d6")

@app.route("/")
def hello_world():
    return "hello world here!"

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()

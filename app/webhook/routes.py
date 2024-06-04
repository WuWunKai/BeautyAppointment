from flask import Blueprint, request, jsonify
from app.models import Store
import requests
import re

webhook = Blueprint('webhook', __name__)

@webhook.route('/line/webhook', methods=['POST'])
def line_webhook():
    data = request.get_json()
    events = data.get('events', [])

    for event in events:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            reply_token = event['replyToken']
            user_id = event['source']['userId']
            message_text = event['message']['text']
            print(user_id)

            # 提取store_id
            store_id = extract_store_id_from_message(message_text)
            if not store_id:
                continue  # 如果找不到store_id，跳過

            store = Store.query.get(store_id)
            if not store or not store.channel_access_token:
                continue  # 如果找不到store或沒有設置channel_access_token，跳過

            # 發送回應消息
            reply_message = "收到您的消息: " + message_text
            send_reply_message(store.channel_access_token, reply_token, reply_message)

    return jsonify({"status": "ok"})


def send_reply_message(channel_access_token, reply_token, message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}"
    }

    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    response = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)
    return response.status_code, response.json()


def extract_store_id_from_message(message_text):
    # 假設您的message_text包含store_id的信息，用於識別是哪個店家發送的
    # 這裡需要您具體實現從消息中提取store_id的邏輯
    # 例如，消息格式是 "store_id:<store_id> message: <message>"
    # 可以使用正則表達式或其他方式提取store_id
    match = re.search(r'store_id:(\d+)', message_text)
    if match:
        return int(match.group(1))
    return None
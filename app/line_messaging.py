import requests

def send_line_message(channel_access_token, to, message):
    print(message)
    print(to)
    print(channel_access_token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}"
    }

    payload = {
        "to": to,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    return response.status_code, response.json()
import websocket
import requests
import json

alerts = []

TELEGRAM_TOKEN = 'TOKEN'
TELEGRAM_CHANNEL = '@CHANNEL'

coin_dict = {
    "SOLUSDT": [144.22, 'Breakout'],
    "WIFUSDT": [1.87, 'cross'],
}


def send_message(text):
    res = requests.get('https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN),
                       params=dict(chat_id=TELEGRAM_CHANNEL, text=text))


def on_open(ws):
    sub_msg = {"method": "SUBSCRIBE", "params": ["!miniTicker@arr"], "id": 1}
    ws.send(json.dumps(sub_msg))
    print("Opened connection")


def on_message(ws, message):
    data = json.loads(message)
    for i, j in coin_dict.items():
        alert_down(symbol=i, price=j[0], data=data, msg=j[1])


def alert_down(symbol, price, data, msg):
    for x in data:
        if x['s'] == symbol and float(x['c']) <= price and x['s'] not in alerts:
            # print(x['s'] + ' ' + x['c'])
            send_message(x['s'] + ' ' + x['c'] + ' <--- ' + msg)
            alerts.append(x['s'])


def alert_up(symbol, price, data, msg):
    for x in data:
        if x['s'] == symbol and float(x['c']) >= price and x['s'] not in alerts:
            # print(x['s'] + ' ' + x['c'])
            send_message(x['s'] + ' ' + x['c'] + ' <--- ' + msg)
            alerts.append(x['s'])


ws = websocket.WebSocketApp('wss://fstream.binance.com/ws',
                            on_open=on_open,
                            on_message=on_message)
ws.run_forever()

# coding=UTF-8

from bottle import route, run, request, abort, static_file
from fsm import TocMachine
from utils import *
from myfsm import build_fsm
import json
from pprint import pprint
import threading


VERIFY_TOKEN = "Your Webhook Verify Token"
machine_q = []
Q1_count = 0

@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        if('message' in event):
            text = event['message']['text']
        else:
            text = ""
            return 'OK'
        sender_id = event['sender']['id']
        with open('problem.json') as f:
            data = json.load(f)
            current_machine = check_exit(sender_id,machine_q)
            if(current_machine == False):
                new_machine = build_fsm(sender_id)
                machine_q.append(new_machine)
                current_machine = check_exit(sender_id,machine_q)
            #print(current_machine.state)
            if(text == "demo"):
                current_machine.for_demo()
                send_text_message(sender_id,"demo")
            if(text == "start" and current_machine.state == "init"):
                current_machine.start_game()
                send_q = data['Q1']
                send_a1 = data['A1']['1']
                send_a2 = data['A1']['2']
                send_text_message(sender_id,send_q)
                send_text_message(sender_id,send_a1)
                send_text_message(sender_id,send_a2)
            elif(text == "重來" and current_machine.state != "init"):
                current_machine.back()
                current_machine.Q1_count = 0
                send_text = "please type start"
                send_text_message(sender_id,send_text)
            elif(current_machine.Q1_count == 3 and current_machine.state == "point0"):
                send_text = "看來你信念堅定 答對了"
                send_text_message(sender_id,send_text)
                send_text = data['Q2']
                send_a1 = data['A2']['1']
                send_a2 = data['A2']['2']
                send_text_message(sender_id,send_text)
                send_text_message(sender_id,send_a1)
                send_text_message(sender_id,send_a2)
                current_machine.move()
            elif(text == data['A1']['1'] and current_machine.state == "point0"):
                #current_machine.start_game()
                send_text = data['R1']['1']
                send_text_message(sender_id,send_text)
                current_machine.Q1_count += 1
            elif(text == data['A1']['2'] and current_machine.state == "point0"):
                #current_machine.start_game()
                send_text = data['R1']['2']
                send_text_message(sender_id,send_text)
                current_machine.Q1_count += 1
            elif(text == data['A2']['1'] and current_machine.state == "point1"):
                send_text = data['R2']['1']
                send_text_message(sender_id,send_text)
                send_text = data['Q3']
                send_a1 = data['A3']['1']
                send_a2 = data['A3']['2']
                send_text_message(sender_id,send_text)
                send_text_message(sender_id,send_a1)
                send_text_message(sender_id,send_a2)
                current_machine.move()
            elif(text == data['A2']['2'] and current_machine.state == "point1"):
                send_text = data['R2']['2']
                send_text_message(sender_id,send_text)
            elif(text == data['A3']['1'] and current_machine.state == "point2"):
                send_text = data['R3']['1']
                send_text_message(sender_id,send_text)
            elif(text == data['A3']['2'] and current_machine.state == "point2"):
                send_text = data['R3']['2']
                send_text_message(sender_id,send_text)
                send_text = data['Q4']
                send_a1 = data['A4']['1']
                send_a2 = data['A4']['2']
                send_a3 = data['A4']['3']
                send_text_message(sender_id,send_text)
                send_text_message(sender_id,send_a1)
                send_text_message(sender_id,send_a2)
                send_text_message(sender_id,send_a3)
                current_machine.move()
            elif(text == data['A4']['1'] and current_machine.state == "point3"):
                send_text = data['R4']['1']
                send_text_message(sender_id,send_text)
            elif(text == data['A4']['2'] and current_machine.state == "point3"):
                send_text = data['R4']['2']
                send_text_message(sender_id,send_text)
                current_machine.move()
            elif(text == data['A4']['3'] and current_machine.state == "point3"):
                send_text = data['R4']['3']
                send_text_message(sender_id,send_text)
            else:
                send_text = "這是一個知識王的小遊戲，你必須要回答完所有的問題才算勝利，打 start 開始遊戲，打重來從第一題開始"
                send_text_message(sender_id,send_text)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine_q[0].get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)

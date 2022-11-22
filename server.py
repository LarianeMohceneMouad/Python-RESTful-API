from flask import Flask, render_template, request
import requests
from twilio.rest import Client as TwilioClient
import mysql.connector
from random import randrange
from datetime import timedelta
from datetime import datetime

import keys

passport_requests = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="requests"
)
cursor = passport_requests.cursor()


def db_insert(nin_val, name_val, lastname_val, delivery_date_val, num_val):
    query = f"INSERT INTO `passport_resuests` (`NIN`, `Name`, `LastName`, `DeliveryDate`, `Number`) VALUES ('{nin_val}'," \
            f" '{name_val}', '{lastname_val}', '{delivery_date_val}', '{num_val}');"
    cursor.execute(query)
    passport_requests.commit()


def delivery_date_gen():
    start = datetime.today()
    end = datetime.today() + timedelta(days=30)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60)
    random_second = randrange(int_delta)
    return (start + timedelta(seconds=random_second)).date()


def get_marital_status(nin_val, name_val, lastname_val):
    response = requests.get(f'http://127.0.0.1:5000/CivilStateDecision/{int(nin_val)}/{name_val.lower()}/'
                            f'{lastname_val.lower()}')
    return response.json()['result']


def get_criminal_record(nin_val):
    response = requests.get(f'http://127.0.0.1:5001/CriminalRecord/{nin_val}')
    return response.json()['state']


def get_safety_state(nin_val):
    response = requests.get(f'http://127.0.0.1:5002/SafetyState/{nin_val}')
    return response.json()['state']


def sms_sender(result, num):
    client = TwilioClient(keys.account_sid, keys.auth_token)
    client.messages.create(body=f'{result}', from_=keys.twilio_number, to="+213"+num)


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    try:
        if request.form.get("NIN"):
            nin = int(request.form.get("NIN"))
            name = request.form.get("name")
            last_name = request.form.get("lastname")
            number = request.form.get("number")
            message = 'YOUR PASSPORT REQUEST'
            message += f'NIN: {nin} \nName: {name} \nLastname: {last_name} \n'
            if get_marital_status(nin, name, last_name) == "True":
                if get_safety_state(nin) == "Wanted" or get_criminal_record(nin) == "Bad":
                    message += "\nRequest rejected \n Reasons :  "
                    if get_safety_state(nin) == "Wanted":
                        message += f"\n 1. Current Safety State Status : {get_safety_state(nin)}"
                    if get_criminal_record(nin) == "Bad":
                        message += f"\n 2. Criminal Record Decision result : {get_criminal_record(nin)}"
                    cursor.execute(f'select * from passport_resuests where nin = {nin}')
                    if bool(cursor.fetchall()):
                        return 'Request Already Submitted'
                    else:
                        db_insert(nin, name, last_name, 'None', number)
                        sms_sender(message, number)
                        return 'Request Submitted'
                else:
                    cursor.execute(f'select * from passport_resuests where nin = {nin}')
                    if bool(cursor.fetchall()):
                        return 'Request Already Submitted'
                    else:
                        delivery_date = delivery_date_gen()
                        message += f"\nPassport Request : Submitted \nDelivery Date {delivery_date}"
                        db_insert(nin, name, last_name, delivery_date, number)
                        sms_sender(message, number)
                        return 'Request Submitted'
        else:
            return render_template("index.html")

    except Exception as e:
        return e.with_traceback()


if __name__ == '__main__':
    app.run(port=5003, debug=True)

from flask import Flask
import mysql.connector

safety_state_bd = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="safety_state"
)
cursor = safety_state_bd.cursor()


app = Flask(__name__)


@app.route('/')
def index():
    return 'Safety State Rest API'


@app.route('/SafetyStates')
def get_safety_states():
    output = []
    cursor.execute('select * from information')
    for info in cursor.fetchall():
        nin, state = info
        dict_val = {'nin': nin, 'state': state}
        output.append(dict_val)
    cursor.clear_attributes()
    return {"SafetyState": output}


@app.route('/SafetyState/<nin>')
def get_civil_state_decision(nin):
    cursor.execute(f'select * from information where NIN = {nin}')
    _, state = cursor.fetchall()[0]
    if bool(cursor.fetchall()):
        return {'state': 'Not found'}
    else:
        return {'state': state}


if __name__ == '__main__':
    app.run(port=5002, debug=True)


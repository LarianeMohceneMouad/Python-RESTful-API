from flask import Flask
import mysql.connector

civil_state_bd = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="etatcivil"
)
cursor = civil_state_bd.cursor()


app = Flask(__name__)


@app.route('/')
def index():
    return 'Civil State REST API'


@app.route('/CivilStates')
def get_civil_states():
    output = []
    cursor.execute('select * from information')
    for info in cursor.fetchall():
        nin, name, lastname, number = info
        dict_val = {'nin': nin, 'firstname': name, 'lastname': lastname, 'number': number}
        output.append(dict_val)
    cursor.clear_attributes()
    return {"CivilState": output}


@app.route('/CivilStateDecision/<nin>/<name>/<lastname>')
def get_civil_state_decision(nin, name, lastname):
    cursor.execute(f'select * from information where NIN = {nin}')
    nin_val, name_val, lastname_val, number_val = cursor.fetchall()[0]
    if bool(cursor.fetchall()):
        return {'result': 'Not found'}
    elif nin_val != int(nin) or name_val != name or lastname_val != lastname:
        return {'result': 'False'}
    elif nin_val == int(nin) or name_val == name or lastname_val == lastname:
        return {'result': 'True'}


if __name__ == '__main__':
    app.run(port=5000, debug=True)


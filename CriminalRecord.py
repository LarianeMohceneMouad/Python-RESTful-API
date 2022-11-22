from flask import Flask
import mysql.connector

criminal_record_bd = mysql.connector.connect(
    host="localhost",
    username="root",
    password="",
    database="criminal_record"
)
cursor = criminal_record_bd.cursor()


app = Flask(__name__)


@app.route('/')
def index():
    return 'Criminal Record Rest API'


@app.route('/CriminalRecords')
def get_criminal_records():
    output = []
    cursor.execute('select * from information')
    for info in cursor.fetchall():
        nin, state = info
        dict_val = {'nin': nin, 'state': state}
        output.append(dict_val)
    cursor.clear_attributes()
    return {"CriminalRecord": output}


@app.route('/CriminalRecord/<nin>')
def get_civil_state_decision(nin):
    cursor.execute(f'select * from information where NIN = {nin}')
    _, state = cursor.fetchall()[0]
    if bool(cursor.fetchall()):
        return {'state': 'Not found'}
    else:
        return {'state': state}


if __name__ == '__main__':
    app.run(port=5001, debug=True)


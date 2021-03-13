import random
from flask import Flask, render_template, request, redirect, url_for
from sqlite3 import connect
from repository import init
from datetime import datetime, timedelta
import logging

app = Flask(__name__)
db = "C:\\Users\\Kirill\\Desktop\\doctor-develop\\history.db"
logging.basicConfig(filename='C:\\Users\\Kirill\\Desktop\\doctor-develop\\log{datetime.now()}.log', level=logging.DEBUG)
init(db)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/records', methods=['POST', 'GET'])
def records():
    with connect(db) as con:
        cur = con.cursor()
        cur.execute("SELECT fio, birthday, snils, polis, address, phone, date FROM register")
        register = cur.fetchall()
        logging.info(f'open view records. count result registers \'{len(register)}\'')
    return render_template('records.html', register=register)


@app.route('/card/<patient_id>', methods=['POST', 'GET'])
def card(patient_id):
    logging.info(f'open view card for patient {patient_id}')
    with connect(db) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT r.id, r.fio, r.birthday, d.diagnosis, d.complaint, d.treatment 
            FROM register AS r 
                LEFT JOIN diagnosis AS d ON r.id = d.register_id""")
        patients = [[v if v is not None else "" for v in list_of_list] for list_of_list in cur.fetchall()]
        current = ["", "", ""]
        for x in patients:
            if str(x[0]) == patient_id:
                current = x
                break
    if request.method == 'POST':
        logging.info(f'update data diagnosis for patient - {patient_id}')
        if request.form['submit'] == 'Сохранить':
            diagnosis = request.form['diagnosis']
            complaint = request.form['complaint']
            treatment = request.form['treatment']
            with connect(db) as con:
                cur = con.cursor()
                cur.execute("SELECT register_id FROM diagnosis WHERE register_id = ?", (patient_id,))
                if cur.fetchone() is None:
                    cur.execute("INSERT INTO diagnosis VALUES (?, ?, ?, ?)",
                                (patient_id, diagnosis, complaint, treatment))
                else:
                    cur.execute(
                        """UPDATE diagnosis SET diagnosis = ?, complaint = ?, treatment = ? WHERE register_id = ?""",
                        (request.form['diagnosis'], request.form['complaint'], request.form['treatment'], patient_id)
                    )
                con.commit()
        elif request.form['submit'] == 'Направление на анализы':
            logging.info(f'patient - {patient_id} get referral for analyzes')
            with connect(db) as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO analyzes VALUES (?, ?, ?, ?, ?)",
                    (None, patient_id, random_name_analyzes(), random_result_analyzes(),
                     datetime.now() + timedelta(days=7))
                )
                con.commit()
        elif request.form['submit'] == 'Результаты анализов':
            logging.info(f'show analyzes for patient - {patient_id}')
            return redirect(url_for('analyzes', patient_id=patient_id))
        else:
            pass
    return render_template('card.html', patients=patients, current=current)


@app.route('/card/<patient_id>/analyzes', methods=['GET'])
def analyzes(patient_id):
    with connect(db) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM analyzes WHERE register_id = ?", (patient_id,))
        result = cur.fetchone()
        if result is None:
            analyzes = False
        else:
            analyzes = result
        logging.info(f'analyzes for patient - {patient_id}: {str(analyzes)}')
    return render_template('analyzes.html', analyzes=analyzes)


def random_name_analyzes():
    analyzes_list = ["анализ 0", "анализ 1", "анализ 2", "анализ 3", "анализ 4", "анализ 5", ]
    return random.choice(analyzes_list)


def random_result_analyzes():
    analyzes_list = ["POS", "NEG"]
    return random.choice(analyzes_list)


if __name__ == '__main__':
    app.run()

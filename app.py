from flask import Flask, render_template, request, jsonify
import sqlite3
from sqlite3 import Error
import threading

app = Flask(__name__)

DATABASE = 'survey.db'

def create_connection(db_file):
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table():
    """ create table if not exists """
    conn = create_connection(DATABASE)
    if conn:
        try:
            sql_create_survey_table = """ CREATE TABLE IF NOT EXISTS survey (
                                            student_number text PRIMARY KEY,
                                            click_count integer NOT NULL,
                                            button_type text NOT NULL
                                        ); """
            conn.execute(sql_create_survey_table)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_survey():
    data = request.get_json()
    student_number = data.get('studentNumber')
    if not (student_number.startswith('i') and student_number[1:].isdigit()):
        return jsonify(success=False, message="Your student number should start with an I and contain 6 numbers")
    conn = create_connection(DATABASE)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM survey WHERE student_number = ?", (student_number,))
        row = cursor.fetchone()
        if row:
            return jsonify(success=False, message="You have already filled out the survey.")
        else:
            cursor.execute("SELECT ROWID FROM survey ORDER BY ROWID DESC")
            row = cursor.fetchone()
            if not row:
                row = "0"
            button_type = "PRESS" if int(row[0]) % 2 == 0 else "DON'T PRESS"

            cursor.execute("INSERT INTO survey (student_number, click_count, button_type) VALUES (?, ?, ?)", (student_number, 0, button_type))
            conn.commit()
            return jsonify(success=True, buttonType=button_type)
    return jsonify(success=False, message="Database connection error.")

@app.route('/click', methods=['POST'])
def handle_click():
    data = request.get_json()
    student_number = data.get('studentNumber')
    
    conn = create_connection(DATABASE)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT click_count FROM survey WHERE student_number = ?", (student_number,))
        row = cursor.fetchone()
        if row:
            click_count = row[0] + 1
            cursor.execute("UPDATE survey SET click_count = ? WHERE student_number = ?", (click_count, student_number))
            conn.commit()
            return jsonify(success=True, clickCount=click_count)
    return jsonify(success=False, message="Database connection error.")

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

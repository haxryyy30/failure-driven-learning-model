from flask import Flask, render_template, request, redirect, session
from flask import send_file
from flask import Flask

import os
import time
import sqlite3
import random
import logging
import pandas as pd



app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.secret_key = "fdl_secret_key"






# =====================================
# DATABASE CONNECTION
# =====================================

def connect_db():

    conn = sqlite3.connect('failures.db')

    return conn

# =====================================
# DATABASE SETUP
# =====================================

def setup_database():

    conn = connect_db()

    cursor = conn.cursor()

    # FAILURES TABLE

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS failures (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        error_message TEXT,

        module_name TEXT,

        severity TEXT,

        predicted_cause TEXT,

        solution TEXT,

        confidence INTEGER,
                   
        auto_fix_status TEXT,
                   
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP


    )

    """)

    # USERS TABLE

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        password TEXT

    )

    """)

    conn.commit()

    conn.close()

setup_database()

# =====================================
# AI ROOT CAUSE ANALYSIS
# =====================================

def predict_root_cause(error):

    error = error.lower()

    if "database" in error:

        return {

            "cause":"Database Failure",

            "solution":"Check database server and credentials",

            "confidence":95

        }

    elif "api" in error:

        return {

            "cause":"API Failure",

            "solution":"Check API endpoint and authentication",

            "confidence":90

        }

    elif "indexerror" in error:

        return {

            "cause":"List Index Out Of Range",

            "solution":"Check list indexing logic",

            "confidence":92

        }

    elif "zerodivision" in error:

        return {

            "cause":"Mathematical Runtime Error",

            "solution":"Check denominator before division",

            "confidence":88

        }

    else:

        return {

            "cause":"Runtime Exception",

            "solution":"Check application traceback",

            "confidence":70

        }

# =====================================
# LOGIN
# =====================================

@app.route('/login', methods=['GET', 'POST'])

def login():

    error = None

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        conn = connect_db()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT * FROM users

            WHERE username=? AND password=?

        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user'] = username

            return redirect('/')

        else:

            error = "Invalid Username or Password"

    return render_template(

        'login.html',

        error=error

    )

# =====================================
# REGISTER
# =====================================

@app.route('/register', methods=['POST'])

def register():

    username = request.form['username']

    password = request.form['password']

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO users (username, password)

        VALUES (?, ?)

    """, (username, password))

    conn.commit()

    conn.close()

    return redirect('/login')

# =====================================
# LOGOUT
# =====================================

@app.route('/logout')

def logout():

    session.clear()

    return redirect('/login')

# =====================================
# LEARNING ENGINE
# =====================================

def get_top_patterns():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT predicted_cause, COUNT(*)

        FROM failures

        GROUP BY predicted_cause

        ORDER BY COUNT(*) DESC

        LIMIT 5

    """)

    patterns = cursor.fetchall()

    conn.close()

    return patterns

# =====================================
# LEARNING ANALYTICS
# =====================================

def learn_from_failures():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT severity, COUNT(*)

        FROM failures

        GROUP BY severity

    """)

    data = cursor.fetchall()

    conn.close()

    return data

# =====================================
# ALERT ENGINE
# =====================================

def generate_alerts():

    alerts = []

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM failures

        WHERE severity='HIGH'

    """)

    high_count = cursor.fetchone()[0]

    if high_count >= 5:

        alerts.append(

            "Critical Alert: High severity failures increasing rapidly."

        )

    conn.close()

    return alerts

# =====================================
# DASHBOARD
# =====================================

@app.route('/')

def dashboard():

    if not session.get('user'):

        return redirect('/login')

    conn = connect_db()

    cursor = conn.cursor()

    

    # SEARCH

    search = request.args.get('search', '')

    severity_filter = request.args.get('severity', '')

    module_filter = request.args.get('module', '')

    # QUERY

    query = """

        SELECT *

        FROM failures

        WHERE 1=1

    """

    params = []

    if search:

        query += " AND error_message LIKE ? "

        params.append(f'%{search}%')

    if severity_filter:

        query += " AND severity=? "

        params.append(severity_filter)

    if module_filter:

        query += " AND module_name LIKE ? "

        params.append(f'%{module_filter}%')

    query += " ORDER BY id DESC "

    cursor.execute(query, params)

    logs = cursor.fetchall()

    # TOTAL FAILURES

    cursor.execute("""

        SELECT COUNT(*)

        FROM failures

    """)

    total_failures = cursor.fetchone()[0]

    # HIGH

    cursor.execute("""

        SELECT COUNT(*)

        FROM failures

        WHERE severity='HIGH'

    """)

    high_count = cursor.fetchone()[0]

    # MEDIUM

    cursor.execute("""

        SELECT COUNT(*)

        FROM failures

        WHERE severity='MEDIUM'

    """)

    medium_count = cursor.fetchone()[0]

    # LOW

    cursor.execute("""

        SELECT COUNT(*)

        FROM failures

        WHERE severity='LOW'

    """)

    low_count = cursor.fetchone()[0]

    # MODULE ANALYTICS

    cursor.execute("""

        SELECT module_name, COUNT(*)

        FROM failures

        GROUP BY module_name

    """)

    module_data = cursor.fetchall()

    module_labels = [m[0] for m in module_data]

    module_counts = [m[1] for m in module_data]

    # TOP ERRORS

    cursor.execute("""

        SELECT error_message, COUNT(*) as frequency

        FROM failures

        GROUP BY error_message

        ORDER BY frequency DESC

        LIMIT 5

    """)

    top_errors = cursor.fetchall()

    # CONFIDENCE ANALYTICS

    cursor.execute("""

        SELECT confidence

        FROM failures

        ORDER BY id DESC

        LIMIT 10

    """)

    confidence_data = cursor.fetchall()

    confidence_labels = []

    confidence_values = []

    index = 1

    for row in confidence_data:

        confidence_labels.append(f"Error {index}")

        confidence_values.append(row[0])

        index += 1

    conn.close()

    # AI PREDICTIONS

    predictions = []

    for log in logs:

        predictions.append({

            'error': log[1],

            'prediction': log[4],

            'solution': log[5]

        })

    # LEARNING

    top_patterns = get_top_patterns()

    learning_data = learn_from_failures()

    alerts = generate_alerts()

    return render_template(

        'index.html',

        logs=logs,

        predictions=predictions,

        top_errors=top_errors,

        total_failures=total_failures,

        high_count=high_count,

        medium_count=medium_count,

        low_count=low_count,

        module_data=module_data,

        module_labels=module_labels,

        module_counts=module_counts,

        top_patterns=top_patterns,

        learning_data=learning_data,

        confidence_labels=confidence_labels,

        confidence_values=confidence_values,

        alerts=alerts,

        search=search,

        severity_filter=severity_filter,

        module_filter=module_filter

    )


    return str(data)

# =====================================
# Self-Healing Function
# =====================================

def auto_fix_error(cause):

    if cause == "Database Failure":

        return "Database reconnection attempted"

    elif cause == "API Failure":

        return "API request retried successfully"

    elif cause == "Memory Leak":

        return "Temporary cache cleared"

    elif cause == "Performance Issue":

        return "System optimization executed"

    elif cause == "Runtime Exception":

        return "Application restart suggested"

    else:

        return "No automatic fix available"

# =====================================
# ADD FAILURE
# =====================================

@app.route('/add_failure', methods=['POST'])

def add_failure():

    if not session.get('user'):

        return redirect('/login')

    error_message = request.form['error_message']

    module_name = request.form['module_name']

    severity = request.form['severity']

    # AI ANALYSIS

    prediction = predict_root_cause(

        error_message

    )

    predicted_cause = prediction['cause']

    solution = prediction['solution']

    confidence = prediction['confidence']

    auto_fix_status = auto_fix_error(

    predicted_cause

    )

    print("AUTO FIX:", auto_fix_status)

    # STORE

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO failures (

            error_message,

            module_name,

            severity,

            predicted_cause,

            solution,

            confidence,
                   
            auto_fix_status

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        error_message,

        module_name,

        severity,

        predicted_cause,

        solution,

        confidence,

        auto_fix_status

    ))

    conn.commit()

    conn.close()

    return redirect('/')

# =====================================
# FAILURES PAGE
# =====================================

@app.route('/failures')

def failures_page():

    if not session.get('user'):

        return redirect('/login')

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM failures

        ORDER BY id DESC

    """)

    logs = cursor.fetchall()

    conn.close()

    return render_template(

        'failures.html',

        logs=logs

    )

# =====================================
# PREDICTIONS PAGE
# =====================================
@app.route('/predictions')

def predictions_page():

    if not session.get('user'):

        return redirect('/login')

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM failures

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return render_template(

        'predictions.html',

        rows=rows

    )

# =====================================
# KNOWLEDGE BASE
# =====================================

@app.route('/knowledge')

def knowledge_page():

    if not session.get('user'):

        return redirect('/login')

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            error_message,

            COUNT(*) as frequency,

            predicted_cause,

            solution

        FROM failures

        GROUP BY error_message

        ORDER BY frequency DESC

    """)

    knowledge_data = cursor.fetchall()

    conn.close()

    return render_template(

        'knowledge.html',

        knowledge_data=knowledge_data

    )

# =====================================
# SETTINGS
# =====================================

@app.route('/settings')

def settings():

    if not session.get('user'):

        return redirect('/login')

    return render_template('settings.html')

# =====================================
# EXPORT CSV
# =====================================

@app.route('/export_csv')
def export_csv():
    if not session.get('user'):
        return redirect('/login')

    conn = sqlite3.connect('failures.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM failures")

    data = cursor.fetchall()

    conn.close()

    import csv

    with open('failure_logs.csv', 'w', newline='', encoding='utf-8') as file:

        writer = csv.writer(file)

        writer.writerow([
            'ID',
            'Error Message',
            'Module',
            'Severity',
            'Predicted Cause',
            'Solution',
            'Confidence',
            'Timestamp'
        ])

        writer.writerows(data)

    print(app.url_map)

    return send_file(
        'failure_logs.csv',
        as_attachment=True
    )
    


# =====================================
# RUN APP
# =====================================

if __name__ == '__main__':

    print("\nServer running at:")

    print("http://127.0.0.1:5000\n")

    app.run(

        debug=True,

        host='127.0.0.1',

        port=5000,

        use_reloader=False

    )


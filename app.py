from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from timetable.generator import generate_timetable
import mysql.connector
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Database Connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='shreya_janu_28',
    database='test'
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def user_auth():
    username = request.form['username']
    password = request.form['password']

    cursor.execute("SELECT * FROM timetable WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        session['logged_in_user'] = user['username']
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials. Please try again.", 401

@app.route('/dashboard')
def dashboard():
    if 'logged_in_user' not in session:
        return redirect(url_for('login'))
    
    return render_template("dashboard.html", logged_in_user=session['logged_in_user'])

@app.route('/generate_timetable', methods=['GET', 'POST'])
def generate_timetable_route():
    if 'logged_in_user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        subjects = request.form.get('subjects', '').split(',')
        labs = request.form.get('labs', '').split(',')
        total_periods = int(request.form.get('total_periods', 0))
        total_days = int(request.form.get('total_days', 0))
        lab_days = request.form.get('lab_days', '').split(',')
        break_times = request.form.get('break_times', '').split(',')
        period_duration = int(request.form.get('period_duration', 0))
        start_time = request.form.get('start_time', '')
        end_time = request.form.get('end_time', '')
        title = request.form.get('title', 'Untitled Timetable')

        input_data = {
            'subjects': subjects,
            'labs': labs,
            'total_periods': total_periods,
            'total_days': total_days,
            'lab_days': lab_days,
            'break_times': break_times,
            'period_duration': period_duration,
            'start_time': start_time,
            'end_time': end_time
        }

        timetable = generate_timetable(input_data)
        timetable_data = json.dumps(timetable)

        cursor.execute("INSERT INTO history (username, title, timetable_data) VALUES (%s, %s, %s)",
                       (session['logged_in_user'], title, timetable_data))
        db.commit()

        return render_template("generated_timetable.html", timetable=timetable, title=title)

    return render_template("generate_timetable.html")

@app.route('/page5')
def page5():
    if 'logged_in_user' not in session:
        return redirect(url_for('login'))

    username = session['logged_in_user']
    cursor.execute("SELECT * FROM timetable WHERE username = %s", (username,))
    user_details = cursor.fetchone()

    return render_template("page5.html", user=user_details)

@app.route('/save_timetable', methods=['POST'])
def save_timetable():
    if 'logged_in_user' not in session:
        return jsonify({"success": False, "error": "User not logged in"}), 401

    try:
        data = request.get_json()
        title = data.get('timetable_title')
        timetable_data = data.get('timetable_data')

        if not title or not timetable_data:
            return jsonify({"success": False, "error": "Missing data"}), 400

        cursor.execute("INSERT INTO history (username, title, timetable_data) VALUES (%s, %s, %s)",
                       (session['logged_in_user'], title, timetable_data))
        db.commit()

        return jsonify({"success": True, "message": "Timetable saved successfully!"})

    except mysql.connector.Error as err:
        return jsonify({"success": False, "error": str(err)}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/page6')
def page6():
    if 'logged_in_user' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT id, title FROM history WHERE username = %s", (session['logged_in_user'],))
    timetables = cursor.fetchall()

    return render_template("page6.html", timetables=timetables)

@app.route('/get_timetable/<int:id>')
def get_timetable(id):
    cursor.execute("SELECT timetable_data FROM history WHERE id = %s", (id,))
    timetable = cursor.fetchone()

    if timetable:
        return jsonify({"success": True, "timetable": json.loads(timetable['timetable_data'])})
    return jsonify({"success": False, "error": "Timetable not found"})

@app.route('/logout')
def logout():
    session.pop("logged_in_user", None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

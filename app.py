
import sqlite3
import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# GET ALL STUDENTS
@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])


# GET STUDENT BY ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# STUDENT INFORMATION
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00177",
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "year": 3,
        "section": "B-Dijkstra"
    })


# STUDENT PROFILE
@app.route('/profile')
def get_profile():
    return jsonify({
        "student_id": "24-00177",
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "year": 3,
        "section": "B-Dijkstra",
        "email": "indicjezalyn@isufst.edu.ph",
        "skills": "python only"
    })


# COURSE INFORMATION
@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "System Integration",
        "instructor": "Rene Arduo",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


# MY SKILLS
@app.route('/my-skills')
def my_skills():
    return jsonify({
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "skills": ["Python", "HTML", "CSS"],
        "interest": "Web Development"
    })


# GREETING ENDPOINT
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello {name}!"})


# HELLO ENDPOINT
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({"message": f"Hello, {name}!"})


# ADD A STUDENT (POST)
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required"}), 400

    required = ['student_id', 'name', 'program', 'year', 'section']
    if any(data.get(field) is None or data.get(field) == ''
           for field in required):
        return jsonify({"error": "Please provide all student fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.execute(
            """INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)""",
            (
                data['student_id'],
                data['name'],
                data['program'],
                data['year'],
                data['section']
            )
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "Student added",
            "id": new_id
        }), 201

    except (sqlite3.Error, TypeError, ValueError):
        return jsonify({"error": "Unable to add student"}), 500


# GET A STUDENT BY ID (API)
@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# UPDATE A STUDENT (PUT)
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A valid JSON object is required"}), 400

    required = ['student_id', 'name', 'program', 'year', 'section']
    if any(data.get(field) is None or data.get(field) == ''
           for field in required):
        return jsonify({"error": "Please provide all student fields"}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        """UPDATE students
        SET student_id=?, name=?, program=?,
            year=?, section=?
        WHERE id=?""",
        (
            data['student_id'],
            data['name'],
            data['program'],
            data['year'],
            data['section'],
            id
        )
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student updated"})


# DELETE A STUDENT (DELETE)
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.execute(
        'DELETE FROM students WHERE id = ?', (id,)
    )
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted"})


# GET ALL STUDENTS (API) - STEP 6
@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM students').fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


# STEP 3 & 4 - GET PARTNER'S STUDENTS
@app.route('/partner-records', methods=['GET'])
@app.route('/classmate-students', methods=['GET'])
def get_classmate_students():
    classmate_api = (
        "https://flask-palec-sethclaire-api.onrender.com/students"
    )

    try:
        response = requests.get(classmate_api, timeout=20)
        response.raise_for_status()

        try:
            records = response.json()
        except ValueError:
            return jsonify({
                "error": "Classmate API did not return valid JSON"
            }), 502

        if not isinstance(records, list):
            return jsonify({
                "error": "Classmate API did not return a list of students"
            }), 502

        return jsonify(records)

    except requests.RequestException:
        return jsonify({
            "error": "Unable to retrieve partner data"
        }), 502


# STEP 5 - IMPORT A PARTNER STUDENT INTO MY DATABASE
@app.route('/import-student', methods=['POST'])
def import_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid student JSON object is required"
        }), 400

    required = ['student_id', 'name', 'program', 'year', 'section']

    if any(data.get(field) is None or data.get(field) == ''
           for field in required):
        return jsonify({
            "error": "Partner record is missing required student fields"
        }), 400

    try:
        year = int(data['year'])
        if year < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Student year must be a valid number"}), 400

    conn = None

    try:
        conn = get_db_connection()
        conn.execute(
            """INSERT INTO students
            (student_id, name, program, year, section, source)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                str(data['student_id']),
                str(data['name']),
                str(data['program']),
                year,
                str(data['section']),
                'Classmate API'
            )
        )
        conn.commit()

        return jsonify({
            "message": "Remote record saved",
            "source": "Classmate API"
        }), 201

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()

        return jsonify({
            "error": "Unable to save record. Check that your database has a source column."
        }), 500

    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


import sqlite3
import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# GET ALL STUDENTS
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])


# GET STUDENT BY DATABASE ID
@app.route('/students/<int:id>', methods=['GET'])
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
@app.route('/student', methods=['GET'])
def get_student():
    return jsonify({
        "student_id": "24-00177",
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "year": 3,
        "section": "B-Dijkstra"
    })


# STUDENT PROFILE
@app.route('/profile', methods=['GET'])
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
@app.route('/course', methods=['GET'])
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "System Integration",
        "instructor": "Rene Arduo",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


# MY SKILLS
@app.route('/my-skills', methods=['GET'])
def my_skills():
    return jsonify({
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "skills": ["Python", "HTML", "CSS"],
        "interest": "Web Development"
    })


# GREETING ENDPOINT
@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello {name}!"})


# HELLO ENDPOINT
@app.route('/hello', methods=['GET'])
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({"message": f"Hello, {name}!"})


# STEP 8 - ADD A STUDENT THROUGH THE API
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required"
        }), 400

    required = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    if any(
        data.get(field) is None or data.get(field) == ''
        for field in required
    ):
        return jsonify({
            "error": "Please provide all student fields"
        }), 400

    try:
        year = int(data['year'])
        if year < 1:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "error": "Year must be a positive number"
        }), 400

    # Use the provided source or default to External API.
    source = data.get('source') or 'External API'

    if not isinstance(source, str):
        return jsonify({
            "error": "Source must be text"
        }), 400

    conn = None

    try:
        conn = get_db_connection()

        cursor = conn.execute(
            """INSERT INTO students
            (student_id, name, program, year, section, source)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                str(data['student_id']),
                str(data['name']),
                str(data['program']),
                year,
                str(data['section']),
                source
            )
        )

        conn.commit()
        new_id = cursor.lastrowid

        return jsonify({
            "message": "Student added successfully",
            "id": new_id,
            "source": source
        }), 201

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()

        app.logger.exception("Failed to add student through API")
        return jsonify({
            "error": "Unable to add student. Check the database schema."
        }), 500

    finally:
        if conn is not None:
            conn.close()


# GET ALL STUDENTS (API)
@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


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


# UPDATE A STUDENT
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required"
        }), 400

    required = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    if any(
        data.get(field) is None or data.get(field) == ''
        for field in required
    ):
        return jsonify({
            "error": "Please provide all student fields"
        }), 400

    try:
        year = int(data['year'])
        if year < 1:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "error": "Year must be a positive number"
        }), 400

    conn = get_db_connection()

    try:
        cursor = conn.execute(
            """UPDATE students
            SET student_id = ?, name = ?, program = ?,
                year = ?, section = ?
            WHERE id = ?""",
            (
                str(data['student_id']),
                str(data['name']),
                str(data['program']),
                year,
                str(data['section']),
                id
            )
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify({"message": "Student updated successfully"})

    finally:
        conn.close()


# DELETE A STUDENT
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            'DELETE FROM students WHERE id = ?', (id,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify({"message": "Student deleted successfully"})

    finally:
        conn.close()


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
        records = response.json()

        if not isinstance(records, list):
            return jsonify({
                "error": "Classmate API did not return a list of students"
            }), 502

        return jsonify(records)

    except (requests.RequestException, ValueError):
        app.logger.exception("Unable to retrieve partner records")
        return jsonify({
            "error": "Unable to retrieve valid partner data"
        }), 502


# STEP 5 & 6 - IMPORT A PARTNER STUDENT
@app.route('/import-student', methods=['POST'])
def import_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid student JSON object is required"
        }), 400

    required = [
        'student_id', 'name', 'program', 'year', 'section'
    ]

    if any(
        data.get(field) is None or data.get(field) == ''
        for field in required
    ):
        return jsonify({
            "error": "Partner record is missing required fields"
        }), 400

    try:
        year = int(data['year'])
        if year < 1:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "error": "Student year must be a positive number"
        }), 400

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

        app.logger.exception("Failed to import partner student")
        return jsonify({
            "error": "Unable to save the imported record"
        }), 500

    finally:
        if conn is not None:
            conn.close()


# ADD A NEW STUDENT DIRECTLY TO THE CLASSMATE'S API
@app.route('/send-to-classmate', methods=['POST'])
def send_to_classmate():
    classmate_api = "https://flask-palec-sethclaire-api.onrender.com/students"

    student = {
        "student_id": request.form.get("student_id", "").strip(),
        "name": request.form.get("name", "").strip(),
        "program": request.form.get("program", "").strip(),
        "year": request.form.get("year", "").strip(),
        "section": request.form.get("section", "").strip()
    }

    if not all(student.values()):
        return """
            <h2>Missing information</h2>
            <p>Please complete every field.</p>
            <a href="/">Return to the Student API Interface</a>
        """, 400

    try:
        student["year"] = int(student["year"])
        if student["year"] < 1:
            raise ValueError
    except (TypeError, ValueError):
        return """
            <h2>Invalid year level</h2>
            <p>Year must be a positive number.</p>
            <a href="/">Return to the Student API Interface</a>
        """, 400

    try:
        # Send the new student to the classmate's server, not to this app's database.
        response = requests.post(classmate_api, json=student, timeout=20)

        if response.status_code in (200, 201):
            return """
                <h2>Student submitted to the Classmate API</h2>
                <p>The classmate's API accepted the request.</p>
                <a href="/">Return to the Student API Interface</a>
            """

        return (
            "<h2>The Classmate API did not accept the student</h2>"
            f"<p>Status code: {response.status_code}</p>"
            f"<pre>{response.text}</pre>"
            '<a href="/">Return to the Student API Interface</a>'
        ), 502

    except requests.RequestException as error:
        app.logger.exception("Could not submit student to Classmate API")
        return (
            "<h2>Could not connect to the Classmate API</h2>"
            f"<p>{str(error)}</p>"
            '<a href="/">Return to the Student API Interface</a>'
        ), 502



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


import sqlite3
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
    data = request.get_json()

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
    data = request.get_json()

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

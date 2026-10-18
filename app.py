import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# API: Get all students
@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# Step 7: Get one student by ID
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


# Existing API: Single student
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00177",
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "year": 3,
        "section": "B-Dijkstra"
    })


# Existing API: Profile
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


# Existing API: Course
@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "System Integration",
        "instructor": "Rene Arduo",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


# Custom API: My Skills
@app.route('/my-skills')
def my_skills():
    return jsonify({
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "skills": ["Python", "HTML", "CSS"],
        "interest": "Web Development"
    })


# API: Greet
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello {name}!"})


# API: Hello
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({"message": f"Hello, {name}!"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

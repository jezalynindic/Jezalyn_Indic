from flask import Flask, jsonify, request,  render_template

app = Flask(__name__)


@app.route('/dashboard')
def dashboard():
    return render_template('index.html')




@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00177",
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "year": 3,
        "section": "B-Dijkstra"
    })

@app.route('/profile')
def get_profile():
    return jsonify({
        "student_id": "24-00177",
        "name": "Jezalyn Indic",
        "program": "BSIT",
        "year": 3,
        "section": "B-Dijkstra",
        "email":"indicjezalyn@isufst.edu.ph",
        "skills":"python only"
    })

@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT 3120",
        "course_title": "System Integration",
        "instructor": "Rene Arduo",
        "semester": "First Semester",
        "academic_year": "2026-2027"
    })


@app.route('/greet')
def greet():
    name = request.args.get('name', 'Student')
    section = request.args.get('section', 'Unknown')

    return jsonify({
        "message": f"Hello {name} from {section}!"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


if __name__ == '__main__':
 #  app.run(host="0.0.0.0", port=5000, debug=True)
 app.run(host="0.0.0.0", port=5000, debug=True)
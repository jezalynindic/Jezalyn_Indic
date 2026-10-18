
import sqlite3

# Connect to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Recreate the students table
cursor.execute('DROP TABLE IF EXISTS students')

cursor.execute('''
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        name TEXT NOT NULL,
        program TEXT NOT NULL,
        year INTEGER NOT NULL,
        section TEXT NOT NULL
    )
''')

# Step 10: Add at least five sample student records
students = [
    ('2026-001', 'Alex Santos', 'BSIT', 1, 'A'),
    ('2026-002', 'Maria Reyes', 'BSIT', 2, 'B-Dijkstra'),
    ('2026-003', 'Daniel Cruz', 'BSCS', 3, 'A'),
    ('2026-004', 'Sofia Garcia', 'BSIT', 4, 'B-Dijkstra'),
    ('2026-005', 'Miguel Torres', 'BSCS', 2, 'B')
]

# Insert records into the database
cursor.executemany('''
    INSERT INTO students
    (student_id, name, program, year, section)
    VALUES (?, ?, ?, ?, ?)
''', students)

# Save changes
conn.commit()

# Close the database connection
conn.close()

print("Database initialized successfully!")
print("Five student records added.")

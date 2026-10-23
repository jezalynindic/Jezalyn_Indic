
import sqlite3

# Connect to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Recreate the students table
cursor.execute('DROP TABLE IF EXISTS students')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        name TEXT NOT NULL,
        program TEXT NOT NULL,
        year INTEGER NOT NULL,
        section TEXT NOT NULL,
        source TEXT DEFAULT 'Local'
    )
''')

# Add five sample student records
students = [
    ('2026-001', 'Alex Santos', 'BSIT', 1, 'A', 'Local'),
    ('2026-002', 'Maria Reyes', 'BSIT', 2, 'B-Dijkstra', 'Local'),
    ('2026-003', 'Daniel Cruz', 'BSCS', 3, 'A', 'Local'),
    ('2026-004', 'Sofia Garcia', 'BSIT', 4, 'B-Dijkstra', 'Local'),
    ('2026-005', 'Miguel Torres', 'BSCS', 2, 'B', 'Local')
]

# Insert records into the database
cursor.executemany('''
    INSERT INTO students
    (student_id, name, program, year, section, source)
    VALUES (?, ?, ?, ?, ?, ?)
''', students)

# Save changes
conn.commit()
conn.close()

print("Database initialized successfully!")
print("Five student records added.")
print("Source column added successfully.")

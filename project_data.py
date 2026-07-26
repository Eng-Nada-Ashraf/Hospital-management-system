"""
Optional helper script: populates the hospital.db database with
sample data so you can demo the system immediately without typing
everything manually. Run this ONCE before/after starting the app.

Usage:
    python project_data.py
"""

from hospital_system import Database, today

db = Database()
c = db.cursor

# --- Sample Doctors ---
doctors = [
    ("Dr. Ahmed Youssef", "Cardiology", "01011122233"),
    ("Dr. Mona Adel", "Pediatrics", "01099988877"),
    ("Dr. Karim Fathy", "Orthopedics", "01234567890"),
]
c.executemany(
    "INSERT INTO doctors (name, specialization, phone) VALUES (?, ?, ?)",
    doctors
)

# --- Sample Patients ---
patients = [
    ("Sara Mahmoud", 29, "F", "01555512345", "Nasr City, Cairo", "O+", 0, None, today()),
    ("Omar Khaled", 45, "M", "01022233344", "Giza", "A-", 0, None, today()),
    ("Laila Hassan", 8, "F", "01166677788", "Alexandria", "B+", 0, None, today()),
]
c.executemany(
    """INSERT INTO patients (name, age, gender, phone, address, blood_group,
       admitted, room_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    patients
)



db.conn.commit()
db.close()

print("✔ Sample data inserted successfully into hospital.db")
print("  You can now run: python3 hospital_system.py")

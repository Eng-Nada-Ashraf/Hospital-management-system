import sqlite3
import os
import json
from datetime import datetime
DB_NAME = "hospital.db"
# ==============================================================
#  DATABASE LAYER
# ==============================================================
class Database:
    """Handles all database connections and table creation."""
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_tables()
    def create_tables(self):
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            age          INTEGER NOT NULL,
            gender       TEXT NOT NULL,
            phone        TEXT,
            address      TEXT,
            blood_group  TEXT,
            admitted     INTEGER DEFAULT 0,
            room_id      INTEGER,
            created_at   TEXT
        );
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone        TEXT,
            available    INTEGER DEFAULT 1
        );
        """)
        self.conn.commit()
    def close(self):
        self.conn.close()
# ==============================================================
#  HELPER FUNCTIONS
# ==============================================================
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
def pause():
    input("\nPress Enter to continue...")
def today():
    return datetime.now().strftime("%Y-%m-%d")
def print_header(title):
    clear_screen()
    print("=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)
def get_int_input(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("⚠  Please enter a valid number.")
def get_float_input(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("⚠  Please enter a valid number.")
def print_table(headers, rows):
    if not rows:
        print("\n(No records found)\n")
        return
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print("\n" + header_line)
    print("-" * len(header_line))
    for row in rows:
        print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
    print()
# ==============================================================
#  PATIENT MODULE
# ==============================================================
class PatientManager:
    def __init__(self, db):
        self.db = db
    def add_patient(self):
        print_header("Add New Patient")
        name = input("Full Name: ").strip()
        age = get_int_input("Age: ")
        gender = input("Gender (M/F): ").strip().upper()
        phone = input("Phone Number: ").strip()
        address = input("Address: ").strip()
        blood_group = input("Blood Group: ").strip()
        self.db.cursor.execute(
            """INSERT INTO patients (name, age, gender, phone, address, blood_group, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name, age, gender, phone, address, blood_group, today())
        )
        self.db.conn.commit()
        print(f"\n✔ Patient '{name}' added successfully with ID {self.db.cursor.lastrowid}.")
        pause()
    def view_patients(self):
        print_header("All Patients")
        self.db.cursor.execute("""SELECT patient_id, name, age, gender, phone,
                                   blood_group, admitted, room_id FROM patients""")
        rows = self.db.cursor.fetchall()
        rows = [(r[0], r[1], r[2], r[3], r[4], r[5],
                  "Yes" if r[6] else "No", r[7] or "-") for r in rows]
        print_table(["ID", "Name", "Age", "Gender", "Phone", "Blood", "Admitted", "Room"], rows)
        pause()
    def search_patient(self):
        print_header("Search Patient")
        keyword = input("Enter name or ID to search: ").strip()
        self.db.cursor.execute(
            """SELECT patient_id, name, age, gender, phone, blood_group FROM patients
               WHERE name LIKE ? OR CAST(patient_id AS TEXT) = ?""",
            (f"%{keyword}%", keyword)
        )
        rows = self.db.cursor.fetchall()
        print_table(["ID", "Name", "Age", "Gender", "Phone", "Blood"], rows)
        pause()
    def update_patient(self):
        print_header("Update Patient")
        pid = get_int_input("Enter Patient ID to update: ")
        self.db.cursor.execute("SELECT * FROM patients WHERE patient_id=?", (pid,))
        patient = self.db.cursor.fetchone()
        if not patient:
            print("⚠  Patient not found.")
            pause()
            return
        print("Leave blank to keep current value.")
        name = input(f"Name [{patient[1]}]: ").strip() or patient[1]
        age_new = get_int_input(f"Age [{patient[2]}] (leave blank to keep): ", allow_blank=True)
        age = age_new if age_new is not None else patient[2]
        gender_input = input(f"Gender [{patient[3]}]: ").strip().upper()
        gender = gender_input if gender_input else patient[3]
        phone = input(f"Phone [{patient[4]}]: ").strip() or patient[4]
        address = input(f"Address [{patient[5]}]: ").strip() or patient[5]
        blood_group = input(f"Blood Group [{patient[6]}]: ").strip() or patient[6]
        self.db.cursor.execute(
            "UPDATE patients SET name=?, age=?, gender=?, phone=?, address=?, blood_group=? WHERE patient_id=?",
            (name, age, gender, phone, address, blood_group, pid)
        )
        self.db.conn.commit()
        print("\n✔ Patient updated successfully.")
        pause()
    def delete_patient(self):
        print_header("Delete Patient")
        pid = get_int_input("Enter Patient ID to delete: ")
        self.db.cursor.execute("SELECT name FROM patients WHERE patient_id=?", (pid,))
        row = self.db.cursor.fetchone()
        if not row:
            print("⚠  Patient not found.")
        else:
            confirm = input(f"Are you sure you want to delete '{row[0]}'? (y/n): ").lower()
            if confirm == "y":
                self.db.cursor.execute("DELETE FROM patients WHERE patient_id=?", (pid,))
                self.db.conn.commit()
                print("✔ Patient deleted.")
            else:
                print("Cancelled.")
        pause()
# ==============================================================
#  DOCTOR MODULE
# ==============================================================
class DoctorManager:
    def __init__(self, db):
        self.db = db
    def add_doctor(self):
        print_header("Add New Doctor")
        name = input("Doctor Name: ").strip()
        specialization = input("Specialization: ").strip()
        phone = input("Phone Number: ").strip()
        self.db.cursor.execute(
            "INSERT INTO doctors (name, specialization, phone) VALUES (?, ?, ?)",
            (name, specialization, phone)
        )
        self.db.conn.commit()
        print(f"\n✔ Dr. {name} added successfully with ID {self.db.cursor.lastrowid}.")
        pause()
    def view_doctors(self):
        print_header("All Doctors")
        self.db.cursor.execute(
            "SELECT doctor_id, name, specialization, phone, available FROM doctors"
        )
        rows = self.db.cursor.fetchall()
        rows = [(r[0], r[1], r[2], r[3], "Yes" if r[4] else "No") for r in rows]
        print_table(["ID", "Name", "Specialization", "Phone", "Available"], rows)
        pause()
    def search_doctor(self):
        print_header("Search Doctor")
        keyword = input("Enter name or specialization: ").strip()
        self.db.cursor.execute(
            """SELECT doctor_id, name, specialization, phone FROM doctors
               WHERE name LIKE ? OR specialization LIKE ?""",
            (f"%{keyword}%", f"%{keyword}%")
        )
        rows = self.db.cursor.fetchall()
        print_table(["ID", "Name", "Specialization", "Phone"], rows)
        pause()
    def toggle_availability(self):
        print_header("Toggle Doctor Availability")
        did = get_int_input("Enter Doctor ID: ")
        self.db.cursor.execute("SELECT available FROM doctors WHERE doctor_id=?", (did,))
        row = self.db.cursor.fetchone()
        if not row:
            print("⚠  Doctor not found.")
        else:
            new_status = 0 if row[0] else 1
            self.db.cursor.execute(
                "UPDATE doctors SET available=? WHERE doctor_id=?", (new_status, did)
            )
            self.db.conn.commit()
            print(f"✔ Doctor availability set to {'Available' if new_status else 'Unavailable'}.")
        pause()
    def delete_doctor(self):
        print_header("Delete Doctor")
        did = get_int_input("Enter Doctor ID to delete: ")
        self.db.cursor.execute("SELECT name FROM doctors WHERE doctor_id=?", (did,))
        row = self.db.cursor.fetchone()
        if not row:
            print("⚠  Doctor not found.")
        else:
            confirm = input(f"Delete Dr. {row[0]}? (y/n): ").lower()
            if confirm == "y":
                self.db.cursor.execute("DELETE FROM doctors WHERE doctor_id=?", (did,))
                self.db.conn.commit()
                print("✔ Doctor deleted.")
            else:
                print("Cancelled.")
        pause()
# ==============================================================
#  ROOM & APPOINTMENT MODULE 
# ==============================================================
class Hospital:
    def __init__(self):
        self.rooms = {}
        self.appointments = []
        self.load_rooms()
        self.load_appointments()
    def add_room(self):
        room = input("Enter room number: ")
        if room in self.rooms:
            print("Room already exists.")
        else:
            self.rooms[room] = "Available"
            self.save_rooms()
            print("Room added successfully.")
    def show_rooms(self):
        if not self.rooms:
            print("No rooms found.")
            return
        for room in self.rooms:
            print(f"Room {room} : {self.rooms[room]}")
    def book_appointment(self):
        patient = input("Patient name: ")
        doctor = input("Doctor name: ")
        date = input("Date : ")
        room = input("Room number: ")
        if room not in self.rooms:
            print("Room does not exist.")
            return
        if self.rooms[room] == "Occupied":
            print("Room is occupied.")
            return
        self.appointments.append({
            "patient": patient,
            "doctor": doctor,
            "date": date,
            "room": room
        })
        self.rooms[room] = "Occupied"
        self.save_rooms()
        self.save_appointments()
        print("Appointment booked successfully.")
    def show_appointments(self):
        if not self.appointments:
            print("No appointments.")
            return
        for app in self.appointments:
            print("-------------------")
            print("Patient:", app["patient"])
            print("Doctor :", app["doctor"])
            print("Date   :", app["date"])
            print("Room   :", app["room"])
    def cancel_appointment(self):
        patient = input("Enter patient name: ")
        for app in self.appointments:
            if app["patient"] == patient:
                self.rooms[app["room"]] = "Available"
                self.appointments.remove(app)
                self.save_rooms()
                self.save_appointments()
                print("Appointment cancelled.")
                return
        print("Appointment not found.")
    def save_rooms(self):
        with open("rooms.json", "w") as f:
            json.dump(self.rooms, f)
    def save_appointments(self):
        with open("appointments.json", "w") as f:
            json.dump(self.appointments, f)
    def load_rooms(self):
        try:
            with open("rooms.json", "r") as f:
                self.rooms = json.load(f)
        except FileNotFoundError:
            self.rooms = {}
    def load_appointments(self):
        try:
            with open("appointments.json", "r") as f:
                self.appointments = json.load(f)
        except FileNotFoundError:
            self.appointments = []
# ==============================================================
#  REPORTS MODULE
# ==============================================================
class ReportManager:
    def __init__(self, db, hospital):
        self.db = db
        self.hospital = hospital
    def summary(self):
        print_header("Hospital Summary Report")
        c = self.db.cursor
        c.execute("SELECT COUNT(*) FROM patients")
        total_patients = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM patients WHERE admitted=1")
        admitted = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM doctors")
        total_doctors = c.fetchone()[0]
       
        total_appointments = len(self.hospital.appointments)
        free_rooms = sum(1 for status in self.hospital.rooms.values() if status == "Available")
        print(f"  Total Patients          : {total_patients}")
        print(f"  Currently Admitted       : {admitted}")
        print(f"  Total Doctors            : {total_doctors}")
        print(f"  Active Appointments      : {total_appointments}")
        print(f"  Free Rooms               : {free_rooms}")
        pause()
# ==============================================================
#  MENUS
# ==============================================================
def patient_menu(db):
    pm = PatientManager(db)
    while True:
        print_header("Patient Management")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("0. Back to Main Menu")
        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            pm.add_patient()
        elif choice == "2":
            pm.view_patients()
        elif choice == "3":
            pm.search_patient()
        elif choice == "4":
            pm.update_patient()
        elif choice == "5":
            pm.delete_patient()
        elif choice == "0":
            break
        else:
            print("⚠  Invalid option.")
            pause()
def doctor_menu(db):
    dm = DoctorManager(db)
    while True:
        print_header("Doctor Management")
        print("1. Add Doctor")
        print("2. View All Doctors")
        print("3. Search Doctor")
        print("4. Toggle Availability")
        print("5. Delete Doctor")
        print("0. Back to Main Menu")
        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            dm.add_doctor()
        elif choice == "2":
            dm.view_doctors()
        elif choice == "3":
            dm.search_doctor()
        elif choice == "4":
            dm.toggle_availability()
        elif choice == "5":
            dm.delete_doctor()
        elif choice == "0":
            break
        else:
            print("⚠  Invalid option.")
            pause()
def appointment_menu(hospital):
    while True:
        print_header("Appointment Management")
        print("1. Book Appointment")
        print("2. View All Appointments")
        print("3. Cancel Appointment")
        print("0. Back to Main Menu")
        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            hospital.book_appointment()
            pause()
        elif choice == "2":
            hospital.show_appointments()
            pause()
        elif choice == "3":
            hospital.cancel_appointment()
            pause()
        elif choice == "0":
            break
        else:
            print("⚠  Invalid option.")
            pause()
def room_menu(hospital):
    while True:
        print_header("Room Management")
        print("1. Add Room")
        print("2. View All Rooms")
        print("0. Back to Main Menu")
        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            hospital.add_room()
            pause()
        elif choice == "2":
            hospital.show_rooms()
            pause()
        elif choice == "0":
            break
        else:
            print("⚠  Invalid option.")
            pause()
def main_menu():
    db = Database()
    hospital = Hospital()         
    report = ReportManager(db, hospital)
    while True:
        print_header("  HOSPITAL MANAGEMENT SYSTEM")
        print("1. Patient Management")
        print("2. Doctor Management")
        print("3. Appointment Management")
        print("4. Room Management")
        print("5. Hospital Summary Report")
        print("0. Exit")
        choice = input("\nSelect an option: ").strip()
        if choice == "1":
            patient_menu(db)
        elif choice == "2":
            doctor_menu(db)
        elif choice == "3":
            appointment_menu(hospital)
        elif choice == "4":
            room_menu(hospital)
        elif choice == "5":
            report.summary()
        elif choice == "0":
            print("\nThank you for using the Hospital Management System. Goodbye!")
            db.close()
            break
        else:
            print("⚠  Invalid option.")
            pause()
if __name__ == "__main__":
    main_menu()

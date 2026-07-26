🏥 Hospital Management System (Python + SQLite + JSON)
A complete, console-based Hospital Management System built entirely with Python’s standard library — no external/third-party packages required. Great as an academic project or portfolio piece.
Features
Module
Capabilities
Patients
Add, view, search, update, delete patient records
Doctors
Add, view, search, delete, toggle availability
Appointments
Book, view, cancel, mark as completed
Rooms & Admissions
Add rooms, admit/discharge patients, track occupancy
Reports
Hospital-wide summary statistics dashboard
Tech Stack
Python (standard library only)
SQLite3 for persistent storage of Patients and Doctors
JSON files for Rooms and Appointments
Clean OOP design: separate manager class per module (PatientManager, DoctorManager, AppointmentManager, RoomManager, ReportManager)
Project Structure
hospital_management_system/
├── hospital_system.py      # Main application (run this)
├── project_data.py         # Optional: inserts sample demo data
├── hospital.db             # SQLite database (Patients & Doctors)
├── appointments.json       # Appointment data
├── rooms.json              # Room data
└── README.md
How to Run
Make sure Python is installed:
python --version
(Optional but recommended for a demo) Populate sample data:
python project_data.py
Run the application:
python hospital_system.py
Navigate using the on-screen numbered menus.
Database Schema
SQLite Database
patients — id, name, age, gender, phone, address, blood_group, admitted, room_id
doctors — id, name, specialization, phone, available
JSON Files
appointments.json — id, patient_id, doctor_id, date, time, status, reason
rooms.json — id, room_number, room_type, occupied, price_per_day
Possible Extensions (Great for bonus points)
Add a login system for admins/doctors/receptionists (roles & permissions)
Export reports to PDF or CSV
Add a GUI using tkinter
Add data validation (e.g. phone number format, date format checks)
Convert to a web app using Flask
Notes
The SQLite database (hospital.db) is created automatically the first time you run the application.
Patient and Doctor data are stored in SQLite.
Room and Appointment data are stored in JSON files.
All data is persisted between runs, ensuring information is not lost when the application is closed.

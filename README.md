# 🏥 Hospital Management System (Python + SQLite)

A complete, console-based **Hospital Management System** built entirely with
Python's standard library — no external/third-party packages required.
Great as an academic project or portfolio piece.

## Features

| Module | Capabilities |
|---|---|
| **Patients** | Add, view, search, update, delete patient records |
| **Doctors** | Add, view, search, delete, toggle availability |
| **Appointments** | Book, view, cancel, mark as completed |
| **Rooms & Admissions** | Add rooms, admit/discharge patients, track occupancy |
| **Billing** | Generate bills, view all bills, mark as paid |
| **Prescriptions** | Add prescriptions, view by patient |
| **Reports** | Hospital-wide summary statistics dashboard |

## Tech Stack

- **Python 3** (no external dependencies)
- **SQLite3** (built into Python) for persistent storage
- Clean OOP design: separate manager class per module (`PatientManager`,
  `DoctorManager`, `AppointmentManager`, `RoomManager`, `BillingManager`,
  `PrescriptionManager`, `ReportManager`)

## Project Structure

```
hospital_management_system/
├── hospital_system.py   # Main application (run this)
├── seed_data.py         # Optional: inserts sample demo data
├── hospital.db          # Auto-created SQLite database (on first run)
└── README.md
```

## How to Run

1. Make sure Python 3 is installed:
   ```bash
   python --version
   ```

2. (Optional but recommended for a demo) Populate sample data:
   ```bash
   python project_data.py
   ```

3. Run the application:
   ```bash
   python hospital_system.py
   ```

4. Navigate using the on-screen numbered menus.

## Database Schema (Overview)

- **patients** — id, name, age, gender, phone, address, blood_group, admitted, room_id
- **doctors** — id, name, specialization, phone, available
- **appointments** — id, patient_id, doctor_id, date, time, status, reason
- **rooms** — id, room_number, room_type, occupied, price_per_day


All tables are linked with foreign keys (e.g. an appointment links a patient
to a doctor; a bill links to a patient), demonstrating relational database
design principles.

## Possible Extensions (Great for bonus points)

- Add a login system for admins/doctors/receptionists (roles & permissions)
- Export reports to PDF or CSV
- Add a GUI using `tkinter`
- Add data validation (e.g. phone number format, date format checks)
- Convert to a web app using Flask

## Notes

- The database file `hospital.db` is created automatically the first time
  you run the app — no manual setup needed.
- All data is persisted between runs since it's stored in SQLite, not in
  memory.

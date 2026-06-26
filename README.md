# Hospital Management System Workflow

## Overall Workflow

Start Application
        │
        ▼
     Login Page
        │
        ▼
Verify Username & Password
        │
        ▼
Check User Role
        │
 ┌──────┼───────────┐
 │      │           │
 ▼      ▼           ▼
Admin  Doctor  Receptionist
 │      │           │
 │      │           │
 ▼      ▼           ▼
Admin Dashboard   Doctor Dashboard   Reception Dashboard

---

## Admin Workflow

Admin Login
      │
      ▼
Admin Dashboard
      │
      ├── Patient Management
      │      ├── Add Patient
      │      ├── View Patients
      │      ├── Search Patient
      │      ├── Update Patient
      │      └── Delete Patient
      │
      ├── Doctor Management
      │      ├── Add Doctor
      │      ├── View Doctors
      │      ├── Search Doctor
      │      ├── Update Doctor
      │      └── Delete Doctor
      │
      ├── Appointment Management
      │      ├── Book Appointment
      │      └── View Appointments
      │
      ├── Medicine Management
      │      ├── Add Medicine
      │      ├── View Medicines
      │      ├── Update Medicine
      │      ├── Delete Medicine
      │      └── Medicine Recommendation
      │
      ├── Billing
      │      ├── Generate Bill
      │      └── View Bills
      │
      ├── Reports
      │      ├── Patient Report
      │      ├── Doctor Report
      │      ├── Medicine Report
      │      └── Billing Report
      │
      ├── Feedback
      │      ├── Add Feedback
      │      └── View Feedback
      │
      └── Logout

## Doctor Workflow

Doctor Login
      │
      ▼
Doctor Dashboard
      │
      ├── View Patients
      ├── Medicine Recommendation
      ├── Reports
      │      ├── Patient Report
      │      └── Doctor Report
      ├── Feedback
      │      ├── Add Feedback
      │      └── View Feedback
      └── Logout

## Receptionist Workflow

Receptionist Login
      │
      ▼
Reception Dashboard
      │
      ├── Patient Management
      │      ├── Add Patient
      │      └── View Patients
      │
      ├── Appointment Management
      │      ├── Book Appointment
      │      └── View Appointments
      │
      ├── Billing
      │      ├── Generate Bill
      │      └── View Bills
      │
      ├── Feedback
      │      ├── Add Feedback
      │      └── View Feedback
      │
      └── Logout

## Database Flow

User Login
      │
      ▼
users Table
      │
      ▼
Role Verification
      │
      ├── Admin
      ├── Doctor
      └── Receptionist

Patients → patients Table

Doctors → doctors Table

Appointments → appointments Table

Medicines → medicines Table

Diseases → diseases Table

Medicine Recommendation
      │
      ▼
disease_medicine Table

Billing → bills Table

Feedback → feedback Table


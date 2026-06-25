from flask import Flask, render_template, request , session
import mysql.connector

app = Flask(__name__)

app.secret_key = "hospital_management_system_2026"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="hospitaldb"
)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------- LOGIN (SIMPLE) ----------------
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    cursor = db.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username=%s AND password=%s
    """, (username, password))

    user = cursor.fetchone()
    cursor.close()

    if user:

        role = user[3]   
        session["role"] = role
        if role == "admin":
          return render_template("success.html")

        elif role == "doctor":
          return render_template("doctor_dashboard.html")

        elif role == "receptionist":
          return render_template("reception_dashboard.html")
    
    else:
        return render_template("failure.html")
    


# ---------------- PATIENT MODULE ----------------
@app.route("/addpatient")
def addpatient():
    return render_template("add_patient.html")

# Patients Module
@app.route("/patients")
def patients():
    return render_template("patient_dashboard.html")

@app.route("/savepatient", methods=["POST"])
def savepatient():

    patient_name = request.form["patient_name"]
    age = request.form["age"]
    gender = request.form["gender"]
    phone = request.form["phone"]
    disease = request.form["disease"]
    doctor_name = request.form["doctor_name"]

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO patients
        (patient_name, age, gender, phone, disease, doctor_name)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (patient_name, age, gender, phone, disease, doctor_name))

    db.commit()
    cursor.close()

    return render_template("patient_success.html")


@app.route("/viewpatients")
def viewpatients():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    cursor.close()

    return render_template("view_patients.html", patients=patients)


# ---------------- DOCTOR MODULE ----------------

@app.route("/doctordashboard")
def doctordashboard():
    return render_template("doctor_dashboard.html")

@app.route("/searchdoctor")
def searchdoctor():
    return render_template("search_doctor.html")
@app.route("/finddoctor", methods=["POST"])
def finddoctor():

    doctor_id = request.form["doctor_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT * FROM doctors
        WHERE doctor_id=%s
        """,
        (doctor_id,)
    )

    doctor = cursor.fetchone()

    cursor.close()

    return render_template(
        "doctor_result.html",
        doctor=doctor
    )

@app.route("/updatedoctor")
def updatedoctor():
    return render_template("update_doctor.html")


@app.route("/updatedoctorrecord", methods=["POST"])
def updatedoctorrecord():

    doctor_id = request.form["doctor_id"]
    phone = request.form["phone"]
    experience = request.form["experience"]

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE doctors
        SET phone=%s,
            experience=%s
        WHERE doctor_id=%s
        """,
        (phone, experience, doctor_id)
    )

    db.commit()

    cursor.close()

    return render_template("doctor_update_success.html")

@app.route("/deletedoctor")
def deletedoctor():
    return render_template("delete_doctor.html")


@app.route("/deletedoctorrecord", methods=["POST"])
def deletedoctorrecord():

    doctor_id = request.form["doctor_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM doctors
        WHERE doctor_id=%s
        """,
        (doctor_id,)
    )

    db.commit()

    cursor.close()

    return render_template("doctor_delete_success.html")

@app.route("/dashboard")
def dashboard():

    role = session.get("role")

    if role == "admin":
        return render_template("success.html")

    elif role == "doctor":
        return render_template("doctor_dashboard.html")

    elif role == "receptionist":
        return render_template("reception_dashboard.html")

    return render_template("login.html")


@app.route("/doctors")
def doctors():
     return render_template("doctor_dashboard.html")

@app.route("/adddoctor")
def adddoctor():
    return render_template("add_doctor.html")


@app.route("/savedoctor", methods=["POST"])
def savedoctor():

    doctor_name = request.form["doctor_name"]
    specialization = request.form["specialization"]
    phone = request.form["phone"]
    experience = request.form["experience"]

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO doctors
        (doctor_name, specialization, phone, experience)
        VALUES (%s,%s,%s,%s)
    """, (doctor_name, specialization, phone, experience))

    db.commit()
    cursor.close()

    return render_template("doctor_success.html")


@app.route("/viewdoctors")
def viewdoctors():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()

    return render_template("view_doctors.html", doctors=doctors)


# ---------------- APPOINTMENT MODULE ----------------
@app.route("/appointments")
def appointments():
    return render_template("appointment_dashboard.html")

@app.route("/addappointment")
def addappointment():
    return render_template("add_appointment.html")


@app.route("/addappointmentrecord", methods=["POST"])
def addappointmentrecord():

    patient_id = request.form["patient_id"]
    doctor_id = request.form["doctor_id"]
    appointment_date = request.form["appointment_date"]
    appointment_time = request.form["appointment_time"]
    reason = request.form["reason"]

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO appointments
        (patient_id, doctor_id, appointment_date, appointment_time, reason)
        VALUES (%s,%s,%s,%s,%s)
    """, (patient_id, doctor_id, appointment_date, appointment_time, reason))

    db.commit()
    cursor.close()

    return render_template("appointment_success.html")


@app.route("/viewappointments")
def viewappointments():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM appointments
    """)

    data = cursor.fetchall()
    cursor.close()

    return render_template("view_appointments.html", appointments=data)


# ---------------- MEDICINES MODULE ----------------

@app.route("/medicines/add")
def addmedicine():
    return render_template("add_medicine.html")


@app.route("/savemedicine", methods=["POST"])
def savemedicine():

    medicine_name = request.form["medicine_name"]
    category = request.form["category"]
    price = request.form["price"]
    quantity = request.form["quantity"]
    expiry_date = request.form["expiry_date"]

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO medicines
        (medicine_name, category, price, quantity, expiry_date)
        VALUES (%s,%s,%s,%s,%s)
    """, (medicine_name, category, price, quantity, expiry_date))

    db.commit()
    cursor.close()

    return render_template("medicine_success.html")


@app.route("/medicines/view")
def view_medicines():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    cursor.close()

    return render_template("view_medicines.html", medicines=medicines)

@app.route("/medicines/update")
def update_medicine():
    return render_template("update_medicine.html")

@app.route("/medicines/update/save", methods=["POST"])
def update_medicine_save():

    medicine_id = request.form["medicine_id"]
    price = request.form["price"]
    quantity = request.form["quantity"]

    cursor = db.cursor()

    cursor.execute("""
        UPDATE medicines
        SET price=%s, quantity=%s
        WHERE medicine_id=%s
    """, (price, quantity, medicine_id))

    db.commit()
    cursor.close()

    return render_template("medicine_success.html")

@app.route("/medicines/delete")
def delete_medicine():
    return render_template("delete_medicine.html")

@app.route("/medicines/delete/confirm", methods=["POST"])
def delete_medicine_confirm():

    medicine_id = request.form["medicine_id"]

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM medicines
        WHERE medicine_id=%s
    """, (medicine_id,))

    db.commit()
    cursor.close()

    return render_template("medicine_success.html")

@app.route("/medicines/recommendation")
def medicine_recommendation():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM diseases"
    )

    diseases = cursor.fetchall()

    cursor.close()

    return render_template(
        "medicine_recommendation.html",
        diseases=diseases
    )

@app.route(
    "/show_recommended_medicines",
    methods=["POST"]
)
def show_recommended_medicines():

    disease_id = request.form["disease_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT
            medicines.medicine_name,
            medicines.category,
            medicines.price,
            medicines.quantity

        FROM disease_medicine

        JOIN medicines
        ON disease_medicine.medicine_id
           = medicines.medicine_id

        WHERE disease_medicine.disease_id=%s
        """,
        (disease_id,)
    )

    medicines = cursor.fetchall()

    cursor.close()

    return render_template(
        "recommended_medicines.html",
        medicines=medicines
    )

@app.route("/medicines")
def medicines():
    return render_template("medicine_dashboard.html")


@app.route("/billing")
def billing():
    return render_template("billing_dashboard.html")


@app.route("/billing/add")
def add_bill():
    return render_template("add_bill.html")

@app.route("/billing/save", methods=["POST"])
def save_bill():

    patient_id = request.form["patient_id"]
    patient_name = request.form["patient_name"]

    consultation_fee = float(request.form["consultation_fee"])
    medicine_charges = float(request.form["medicine_charges"])
    room_charges = float(request.form["room_charges"])
    test_charges = float(request.form["test_charges"])

    total_amount = (
        consultation_fee +
        medicine_charges +
        room_charges +
        test_charges
    )

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO billing
        (
            patient_id,
            patient_name,
            consultation_fee,
            medicine_charges,
            room_charges,
            test_charges,
            total_amount
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            patient_id,
            patient_name,
            consultation_fee,
            medicine_charges,
            room_charges,
            test_charges,
            total_amount
        )
    )

    db.commit()

    cursor.close()

    return render_template(
        "bill_success.html",
        total_amount=total_amount
    )

@app.route("/billing/view")
def view_bills():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM billing"
    )

    bills = cursor.fetchall()

    cursor.close()

    return render_template(
        "view_bills.html",
        bills=bills
    )

@app.route("/reports")
def reports():
    return render_template(
        "reports_dashboard.html"
    )
@app.route("/reports/patients")
def patient_report():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM patients"
    )

    patients = cursor.fetchall()

    cursor.close()

    return render_template(
        "patient_report.html",
        patients=patients
    )

@app.route("/reports/doctors")
def doctor_report():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM doctors"
    )

    doctors = cursor.fetchall()

    cursor.close()

    return render_template(
        "doctor_report.html",
        doctors=doctors
    )
@app.route("/reports/medicines")
def medicine_report():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM medicines"
    )

    medicines = cursor.fetchall()

    cursor.close()

    return render_template(
        "medicine_report.html",
        medicines=medicines
    )

@app.route("/reports/billing")
def billing_report():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM billing"
    )

    bills = cursor.fetchall()

    cursor.close()

    return render_template(
        "billing_report.html",
        bills=bills
    )

@app.route("/feedback")
def feedback():
    return render_template(
        "feedback_dashboard.html"
    )
@app.route("/feedback/add")
def add_feedback():
    return render_template(
        "add_feedback.html"
    )
@app.route(
    "/feedback/save",
    methods=["POST"]
)
def save_feedback():

    patient_name = request.form["patient_name"]
    rating = request.form["rating"]
    comments = request.form["comments"]

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO feedback
        (
            patient_name,
            rating,
            comments
        )
        VALUES(%s,%s,%s)
        """,
        (
            patient_name,
            rating,
            comments
        )
    )

    db.commit()

    cursor.close()

    return render_template(
        "feedback_success.html"
    )
@app.route("/feedback/view")
def view_feedback():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM feedback"
    )

    feedbacks = cursor.fetchall()

    cursor.close()

    return render_template(
        "view_feedback.html",
        feedbacks=feedbacks
    )
@app.route("/logout")
def logout():

    session.clear()

    return render_template("login.html")

@app.route("/billingdashboard")
def billingdashboard():
    return render_template(
        "reception_dashboard.html"
    )
@app.route("/receptionviewpatients")
def receptionviewpatients():

    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    cursor.close()

    return render_template("receptionist_view_patients.html", patients=patients)
@app.route("/receptiondashboard")
def receptiondashboard():
    return render_template(
        "reception_dashboard.html"
    )
# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
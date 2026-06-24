from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="hospitaldb"
)


# Home Page
@app.route("/")
def home():
    return render_template("login.html")


# Login Route
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    cursor = db.cursor()

    query = """
    SELECT *
    FROM users
    WHERE BINARY username=%s
    AND BINARY password=%s
    """

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    cursor.close()

    if user:
        return render_template("success.html")
    else:
        return render_template("failure.html")


# Patients Module
@app.route("/patients")
def patients():
    return render_template("patient_dashboard.html")


# Doctors Module
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

    cursor.execute(
        """
        INSERT INTO doctors
        (doctor_name, specialization, phone, experience)
        VALUES(%s,%s,%s,%s)
        """,
        (
            doctor_name,
            specialization,
            phone,
            experience
        )
    )

    db.commit()

    cursor.close()

    return render_template("doctor_success.html")

@app.route("/viewdoctors")
def viewdoctors():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM doctors"
    )

    doctors = cursor.fetchall()

    cursor.close()

    return render_template(
        "view_doctors.html",
        doctors=doctors
    )

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



# Appointments Module

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
        VALUES (%s, %s, %s, %s, %s)
    """, (patient_id, doctor_id, appointment_date, appointment_time, reason))

    db.commit()
    cursor.close()

    return render_template("appointment_success.html")

@app.route("/viewappointments")
def viewappointments():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
            a.appointment_id,
            p.patient_name AS patient_name,
            d.doctor_name AS doctor_name,
            a.appointment_date,
            a.appointment_time,
            a.reason,
            a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """)

    data = cursor.fetchall()
    cursor.close()

    return render_template("view_appointments.html", appointments=data)

@app.route("/updateappointment/<int:id>")
def updateappointment(id):

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM appointments
        WHERE appointment_id=%s
    """, (id,))

    data = cursor.fetchone()
    cursor.close()

    return render_template("update_appointment.html", appointment=data)


@app.route("/updateappointmentrecord", methods=["POST"])
def updateappointmentrecord():

    appointment_id = request.form["appointment_id"]
    date = request.form["appointment_date"]
    time = request.form["appointment_time"]
    status = request.form["status"]

    cursor = db.cursor()

    cursor.execute("""
        UPDATE appointments
        SET appointment_date=%s,
            appointment_time=%s,
            status=%s
        WHERE appointment_id=%s
    """, (date, time, status, appointment_id))

    db.commit()
    cursor.close()

    return render_template("appointment_update_success.html")

@app.route("/deleteappointment/<int:id>")
def deleteappointment(id):

    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM appointments
        WHERE appointment_id=%s
    """, (id,))

    db.commit()
    cursor.close()

    return render_template("appointment_delete_success.html")


# Medicines Module
@app.route("/medicines")
def medicines():
    return "Medicines Module"


# Billing Module
@app.route("/billing")
def billing():
    return "Billing Module"


# Reports Module
@app.route("/reports")
def reports():
    return "Medical Reports Module"


# Feedback Module
@app.route("/feedback")
def feedback():
    return "Feedback Module"

@app.route("/addpatient")
def addpatient():
    return render_template("add_patient.html")

@app.route("/savepatient", methods=["POST"])
def savepatient():

    patient_name = request.form["patient_name"]
    age = request.form["age"]
    gender = request.form["gender"]
    phone = request.form["phone"]
    disease = request.form["disease"]
    doctor_name = request.form["doctor_name"]

    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO patients
        (patient_name, age, gender, phone, disease, doctor_name)
        VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (
            patient_name,
            age,
            gender,
            phone,
            disease,
            doctor_name
        )
    )

    db.commit()
    cursor.close()

    return render_template("patient_success.html")


@app.route("/viewpatients")
def viewpatients():

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM patients"
    )

    patients = cursor.fetchall()

    cursor.close()

    return render_template(
        "view_patients.html",
        patients=patients
    )


@app.route("/searchpatient")
def searchpatient():
    return render_template("search_patient.html")


@app.route("/updatepatient")
def updatepatient():
    return render_template("update_patient.html")


@app.route("/updatepatientrecord", methods=["POST"])
def updatepatientrecord():

    patient_id = request.form["patient_id"]
    phone = request.form["phone"]
    disease = request.form["disease"]

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE patients
        SET phone=%s,
            disease=%s
        WHERE patient_id=%s
        """,
        (phone, disease, patient_id)
    )

    db.commit()

    cursor.close()

    return render_template("update_success.html")


@app.route("/deletepatient")
def deletepatient():
    return render_template("delete_patient.html")


@app.route("/deletepatientrecord", methods=["POST"])
def deletepatientrecord():

    patient_id = request.form["patient_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        DELETE FROM patients
        WHERE patient_id=%s
        """,
        (patient_id,)
    )

    db.commit()

    cursor.close()

    return render_template("delete_success.html")

@app.route("/findpatient", methods=["POST"])
def findpatient():

    patient_id = request.form["patient_id"]

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT * FROM patients
        WHERE patient_id=%s
        """,
        (patient_id,)
    )

    patient = cursor.fetchone()

    cursor.close()

    return render_template(
        "patient_result.html",
        patient=patient
    )

@app.route("/dashboard")
def dashboard():
    return render_template("success.html")

# Run Application
if __name__ == "__main__":
    app.run(debug=True)
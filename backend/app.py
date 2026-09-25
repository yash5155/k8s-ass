# Import Flask utilities
from flask import Flask, jsonify, redirect, render_template, request, url_for

# Import MongoDB client
from pymongo import MongoClient

# Create Flask application
app = Flask(__name__)

# Connect to MongoDB Atlas directly
MONGO_URI = "mongodb+srv://vabeta8216_db_user:WAnEaRsZT7xxKQkj@cluster0.fkbbmaq.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)

# Select database
db = client["student_db"]

# Select collection
collection = db["students"]


# Home page
@app.route("/123")
def home():
    return render_template("form.html")


# Form submission
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form["name"]  # Read name
        email = request.form["email"]  # Read email
        collection.insert_one({"name": name, "email": email})  # Insert record
        return redirect(url_for("success"))  # Redirect on success
    except Exception as e:
        return render_template("form.html", error=str(e))  # Show error


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


# API to return all students
@app.route("/api/students")
def get_students():
    students = []
    for student in collection.find({}, {"_id": 0}):
        students.append(student)
    return jsonify(students)


# API compatibility endpoint for storing students
@app.route("/api/students/store", methods=["POST"])
def store_student_api():
    try:
        payload = request.get_json(silent=True) or request.form
        name = (payload.get("name") or "").strip()
        email = (payload.get("email") or "").strip()

        if not name or not email:
            return jsonify({"error": "Name and email are required."}), 400

        student = {"name": name, "email": email}
        collection.insert_one(student)
        student["_id"] = str(student["_id"])
        return jsonify({"message": "Student saved", "student": student}), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 400


# API compatibility endpoint for listing students
@app.route("/api/students/list")
def get_students_list_api():
    return get_students()


# Test route
@app.route("/")
def test_route():
    return jsonify({"status": "success", "message": "Backend test route is working!"})


# Start server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
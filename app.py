from flask import Flask, jsonify, request, render_template, redirect, url_for
import sqlite3
import joblib

app = Flask(__name__)

# Load the trained machine learning model
model = joblib.load("chd_model.pkl")

# Home route
@app.route("/")
def home():
    return render_template("home.html")  # Serve the home page

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("patient data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name=? AND email=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for("home"))
        else:
            return "Invalid username or password", 401

    return render_template("login.html")

# Instructions page
@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

# Form page
@app.route("/form")
def form():
    return render_template("form.html")

# Prediction route (updated to accept 7 inputs)
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_data = [[
            data["feature1"],  # Male
            data["feature2"],  # Age
            data["feature3"],  # totchol
            data["feature4"],  # diabetes
            data["feature5"],  # BMI
            data["feature6"],  # BP
            data["feature7"]   # smoker
        ]]
        prediction = model.predict(input_data)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Fetch users
@app.route("/users", methods=["GET"])
def fetch_users():
    try:
        conn = sqlite3.connect("patient data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add user
@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        data = request.json
        conn = sqlite3.connect("patient data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (data["name"], data["email"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# List available models
@app.route("/models", methods=["GET"])
def get_models():
    try:
        conn = sqlite3.connect("SQLite&Python.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM models")
        rows = cursor.fetchall()
        conn.close()
        return jsonify([{"id": row[0], "name": row[1]} for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 404 handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found!"}), 404

# Run app
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, request
import sqlite3
import joblib

app = Flask(__name__)

# Load the trained machine learning model
model = joblib.load("chd_model.pkl")  

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Coronary Heart Disease Predictor API!"})

# Route to make predictions with the model
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json  # Receive JSON input
        input_data = [[data["feature1"], data["feature2"], data["feature3"], data["feature4"]]]

        prediction = model.predict(input_data)

        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to fetch users from the SQLite database
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

# Route to add a new user to the database
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

# Route to get list of stored models in the database
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

# Error handling for 404 (not found)
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found!"}), 404

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
    
    if __name__ == "__main__":
    from waitress import serve  # Use Waitress instead of Flask's default server for production
    serve(app, host="0.0.0.0", port=8080)


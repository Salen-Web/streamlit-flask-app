import streamlit as st
from flask import Flask, request, jsonify
import threading
import requests

# Set up Flask backend
app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello from Flask!",
        "value": 42
    }
    return jsonify(data)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_input = data.get("input", "")
    prediction = user_input[::-1]  # Just reversing the string as a placeholder logic
    return jsonify({"prediction": prediction})

# Run Flask in a separate thread
def run_flask():
    app.run(port=5000)

# Start Flask server in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Streamlit frontend
st.title('Streamlit Frontend with Flask Backend')

# Fetch data from Flask API
try:
    response = requests.get("http://127.0.0.1:5000/api/data")
    if response.status_code == 200:
        data = response.json()
        st.write("Message from Flask:", data["message"])
        st.write("Value from Flask:", data["value"])
    else:
        st.error("Failed to get data from Flask backend.")
except Exception as e:
    st.error(f"Error connecting to Flask: {e}")

# Example Streamlit UI to send data to Flask
user_input = st.text_input("Enter your text")
if st.button("Get Prediction"):
    response = requests.post("http://127.0.0.1:5000/predict", json={"input": user_input})
    if response.status_code == 200:
        st.write("Prediction:", response.json()['prediction'])
    else:
        st.write("Error:", response.status_code)

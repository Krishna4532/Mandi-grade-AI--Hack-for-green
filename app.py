import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Simulates the file being received
    return jsonify({"status": "success"})

@app.route('/get_results')
def get_results():
    # Official Mock Report Data
    return jsonify({
        "assigned_grade": "Grade A (Premium)",
        "fair_price": "2,850.00",
        "commodity": "Wheat (Sharbati)",
        "location": "Indore Mandi",
        "analysis": "High luster detected. Moisture content: 11.8% (Optimal). Foreign matter: <0.5%. Grain integrity is excellent with zero pest damage.",
        "prediction": "Market Trend: Bullish (+3% expected)"
    })

if __name__ == '__main__':
    print("🚀 Mandi Grade AI Live: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
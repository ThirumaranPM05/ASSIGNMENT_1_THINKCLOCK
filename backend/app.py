from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from impedance_analysis import analyze_impedance

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "ThinkClock Battery Backend Running"

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    params, soh, bode_plot = analyze_impedance(filepath)

    return jsonify({
        "params": params,
        "soh": soh,
        "bode_plot": bode_plot
    })

if __name__ == "__main__":
    app.run(debug=True)


